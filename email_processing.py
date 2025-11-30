import os
import csv
import imaplib
import email
from email import policy
import pandas as pd
from bs4 import BeautifulSoup
import time
from google.cloud import storage
from datetime import datetime

# ---------------------------
# Airflow Environment Variables
# ---------------------------
EMAIL_USER = 'salacjamesrhode23@gmail.com'
EMAIL_PASSWORD = 'dR4m%T6nb&G+k#F'
IMAP_URL = 'imap.gmail.com'
BATCH_SIZE = 100
BATCH_DELAY = 1

# ---------------------------
# Helper Functions
# ---------------------------
def connect_to_mailbox(user, password, imap_url='imap.gmail.com'):
    """Connect to the Gmail inbox via IMAP and return the mailbox object."""
    mail = imaplib.IMAP4_SSL(imap_url)
    mail.login(user, password)
    mail.select('Inbox')
    return mail

def fetch_email_ids(mail, subject_filter):
    """Fetch all email IDs filtered by subject."""
    status, data = mail.search(None, 'SUBJECT', subject_filter)
    return data[0].split()

def get_email_body(message):
    """Extract the plain text or HTML body from an email message."""
    if message.is_multipart():
        for part in message.iter_parts():
            content_type = part.get_content_type()
            if content_type in ["text/plain", "text/html"]:
                return part.get_content()
    else:
        return message.get_content()

def parse_order_email(body):
    """Parse an order confirmation email and return extracted data."""
    soup = BeautifulSoup(body, 'html.parser')

    # Extract common order information
    customer = soup.find(text="Customer:").parent.next_sibling.strip()
    order_date = soup.find(text="Order Date:").parent.next_sibling.strip()
    total_amount = soup.find_all('tr')[-1].find_all('td')[-1].text.strip()

    # Extract payment details
    payment_method = soup.find(text="Payment Method:").parent.next_sibling.strip()
    payment_ref = soup.find(text="Payment Reference:").parent.next_sibling.strip()
    payment_date = soup.find(text="Payment Date:").parent.next_sibling.strip()

    # Extract line items
    line_items = []
    for tr in soup.find_all('tr')[1:-1]:  # Skip header and total row
        tds = [td.text.strip() for td in tr.find_all('td')]
        line_items.append({
            'customer': customer,
            'product': tds[0],
            'sku': tds[1],
            'qty': tds[2],
            'price': tds[3],
            'line_total': tds[4],
            'total_amount': total_amount,
            'payment_method': payment_method,
            'payment_reference': payment_ref,
            'order_date': order_date,
            'payment_date': payment_date
        })
    return line_items

# ---------------------------
# Main Script
# ---------------------------
# Connect to mailbox
mailbox = connect_to_mailbox(EMAIL_USER, EMAIL_PASSWORD)

# Fetch all email IDs matching the subject
subject_filter = '"[demo-store] Order Confirmation for"'
email_ids = fetch_email_ids(mailbox, subject_filter)

# Process emails in batches
all_orders = []

for i in range(0, len(email_ids), BATCH_SIZE):
    batch_ids = email_ids[i:i + BATCH_SIZE]
    print(f"Processing batch {i // BATCH_SIZE + 1} ({len(batch_ids)} emails)...")

    for email_id in batch_ids:
        status, data = mailbox.fetch(email_id, '(RFC822)')
        for _, raw_msg in (part for part in data if isinstance(part, tuple)):
            msg = email.message_from_bytes(raw_msg, policy=policy.default)
            body = get_email_body(msg)
            all_orders.extend(parse_order_email(body))
    
    time.sleep(BATCH_DELAY)  # Pause between batches

# Convert collected data to DataFrame
orders_df = pd.DataFrame(all_orders)

# Initialize GCS client and bucket
client = storage.Client()
bucket = client.get_bucket('ecomm_bucket001')

# Generate a unique filename with timestamp
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
file_name = f'output_files/from_emails/email_orders_{timestamp}.csv'

bucket.blob(file_name).upload_from_string(
    orders_df.to_csv(
        index=False,
        quoting=csv.QUOTE_ALL,
        encoding="utf-8-sig"
    ),
    content_type='text/csv'
)

