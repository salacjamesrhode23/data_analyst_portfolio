# Standard library
import csv
import email
from email import policy
from email.utils import parsedate_to_datetime
import imaplib
from io import StringIO
import pandas as pd
import json

# Third-party libraries
from bs4 import BeautifulSoup
# from google.cloud import storage
from airflow.providers.google.cloud.hooks.gcs import GCSHook
import pendulum

# ---------------------------
# GCS STATE MANAGEMENT
# ---------------------------
def read_state(
        bucket_name: str,
        state_file: str,
        gcp_conn_id : str = "gcp_connection"
    ) -> dict:
    """
    Reads last processed email timestamp from GCS.
    Returns default earliest timestamp if state doesn’t exist.
    """
    hook = GCSHook(gcp_conn_id=gcp_conn_id)

    # Check if the object exists
    exists = hook.exists(
        bucket_name=bucket_name,
        object_name=state_file,
    )

    if not exists:
        # First run
        return {"last_email_timestamp": "1970-01-01T00:00:00Z"}

    # Download file content as string
    content = hook.download(bucket_name=bucket_name, object_name=state_file).decode("utf-8")

    return json.loads(content)

    # client = storage.Client()
    # bucket = client.bucket(bucket_name)
    # blob = bucket.blob(state_file)

    # if not blob.exists():
    #     # First run, start from a very early date
    #     return {"last_email_timestamp": "1970-01-01T00:00:00Z"}

    # content = blob.download_as_text()
    # return json.loads(content)

def write_state(bucket_name: str, state_file: str, state_dict: dict, gcp_conn_id : str = "gcp_connection"):
    """
    Writes last processed email timestamp to GCS.
    """
    hook = GCSHook(gcp_conn_id=gcp_conn_id)

    hook.upload(
        bucket_name=bucket_name,
        object_name=state_file,
        data=json.dumps(state_dict),
        mime_type="application/json"
    )

    # client = storage.Client()
    # bucket = client.bucket(bucket_name)
    # blob = bucket.blob(state_file)

    # blob.upload_from_string(
    #     json.dumps(state_dict),
    #     content_type="application/json"
    # )

# -----------------------------
# FETCH EMAIL FUNCTION
# -----------------------------
def fetch_email_bodies(
    user: str,
    password: str,
    last_timestamp: pendulum.DateTime,
    subject_filter='[demo-store] Order Confirmation for',
    imap_url='imap.gmail.com'
) -> list:

    """
    Fetch only new emails (using email header Date field)
    """

    def get_email_body(message):
        if message.is_multipart():
            for part in message.iter_parts():
                content_type = part.get_content_type()
                if content_type in ["text/plain", "text/html"]:
                    return part.get_content()
        else:
            return message.get_content()

    mail = imaplib.IMAP4_SSL(imap_url)
    mail.login(user, password)
    mail.select('Inbox')

    status, data = mail.search(
        None,
        'SUBJECT', f'"{subject_filter}"'
    )
    email_ids = data[0].split()[:5]

    results = []

    for email_id in email_ids:
        status, data = mail.fetch(email_id, '(RFC822)')
        for _, raw_msg in (part for part in data if isinstance(part, tuple)):

            msg = email.message_from_bytes(raw_msg, policy=policy.default)

            header_date = msg.get("Date")
            email_ts = parsedate_to_datetime(header_date)
            email_ts = pendulum.instance(email_ts)

            if email_ts <= last_timestamp:
                continue

            body = get_email_body(msg)

            results.append({
                "body": body,
                "email_timestamp": email_ts.to_iso8601_string()
            })

    mail.logout()
    return results

# -----------------------------
# PARSE EMAIL FUNCTION
# -----------------------------
def parse_emails_to_df(emails: list[dict]) -> pd.DataFrame:
    """
    Parse list of email dicts (with body + timestamp) into a DataFrame.
    """

    all_rows = []

    for e in emails:
        body = e["body"]
        email_timestamp = e["email_timestamp"]

        soup = BeautifulSoup(body, 'html.parser')

        # Extract fields from HTML
        customer = soup.find(text="Customer:").parent.next_sibling.strip()
        order_date = soup.find(text="Order Date:").parent.next_sibling.strip()
        total_amount = soup.find_all('tr')[-1].find_all('td')[-1].text.strip()

        payment_method = soup.find(text="Payment Method:").parent.next_sibling.strip()
        payment_reference = soup.find(text="Payment Reference:").parent.next_sibling.strip()
        payment_date = soup.find(text="Payment Date:").parent.next_sibling.strip()

        # Extract line items
        for tr in soup.find_all('tr')[1:-1]:
            tds = [td.text.strip() for td in tr.find_all('td')]

            all_rows.append({
                'customer': customer,
                'product': tds[0],
                'sku': tds[1],
                'qty': tds[2],
                'price': tds[3],
                'line_total': tds[4],
                'total_amount': total_amount,
                'payment_method': payment_method,
                'payment_reference': payment_reference,
                'order_date': order_date,
                'payment_date': payment_date,
                'email_timestamp': email_timestamp  # important!
            })

    return pd.DataFrame(all_rows)

# ---------------------------
# UPLOAD TO GCS FUNCTION
# ---------------------------
def upload_df_to_gcs(
        df: pd.DataFrame,
        bucket_name: str,
        file_name: str,
        gcp_conn_id : str = "gcp_connection"
    ) -> None:

    """
    Convert Dataframe to csv then upload to GCS bucket
    """

    csv_buffer = StringIO()
    df.to_csv(csv_buffer, index=False, quoting=csv.QUOTE_ALL, encoding="utf-8-sig")
    csv_data = csv_buffer.getvalue()

    hook = GCSHook(gcp_conn_id=gcp_conn_id)
    hook.upload(
        bucket_name=bucket_name,
        object_name=file_name,
        data=csv_buffer.getvalue(),
        mime_type="text/csv"
    )

    # client = storage.Client()
    # bucket = client.bucket(bucket_name)
    # blob = bucket.blob(file_name)
    # blob.upload_from_string(csv_data, content_type="text/csv")
    
    # print(f"Uploaded CSV to: gs://{bucket_name}/{file_name}")

# ---------------------------
# ORCHESTRATION FUNCTION
# ---------------------------
def process_email_orders(
    user: str,
    password: str,
    bucket_name: str,
    subject_filter='[demo-store] Order Confirmation for',
    imap_url='imap.gmail.com',
    gcp_conn_id : str = "gcp_connection"
) -> str:

    """
    Main orchestration function: fetch emails → parse → upload CSV.
    Returns file name uploaded to GCS.
    """

    state_file = "idempotency_keys/email_orders_state.json"

    # Step 1: Load last timestamp
    state = read_state(bucket_name, state_file, gcp_conn_id=gcp_conn_id)
    last_ts = pendulum.parse(state["last_email_timestamp"])

    # Step 2: Fetch only new emails
    emails = fetch_email_bodies(
        user, password, last_ts, subject_filter, imap_url
    )

    if not emails:
        print("No new emails to process.")
        return None

    # Step 3: Parse emails to DataFrame
    df = parse_emails_to_df(emails)

    # Step 4: Upload DataFrame to CSV in GCS
    now = pendulum.now()
    file_name = f"from_emails/orders_{now.to_datetime_string().replace(':','').replace(' ','_')}.csv"
    upload_df_to_gcs(df, bucket_name, file_name, gcp_conn_id=gcp_conn_id)

    # Step 5: Update state using the max email timestamp
    new_last_ts = max(pendulum.parse(e["email_timestamp"]) for e in emails)
    write_state(bucket_name, state_file, {"last_email_timestamp": new_last_ts.to_iso8601_string()}, gcp_conn_id=gcp_conn_id)

    print(f"Processed {len(df)} rows. Latest timestamp: {new_last_ts}")

    return file_name