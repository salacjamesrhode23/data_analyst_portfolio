import csv
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime

def parse_order_email(body):

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
    for tr in soup.find_all('tr')[1:-1]:
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

def email_orders_to_gcs(email_bodies: list):

    all_rows = []

    for body in email_bodies:
        extracted_rows = parse_order_email(body)
        all_rows.extend(extracted_rows)

    df = pd.DataFrame(all_rows)

    # Create a timestamped file name
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_path = f"/opt/airflow/data/email_orders_{timestamp}.csv"

    # Save to csv 
    df.to_csv(file_path, index=False, encoding="utf-8-sig", quoting=csv.QUOTE_ALL)

    print(f"Saved parsed email orders to: {file_path}")
