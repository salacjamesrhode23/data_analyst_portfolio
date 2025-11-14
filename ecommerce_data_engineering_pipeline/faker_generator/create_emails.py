import warnings
warnings.filterwarnings("ignore")

import os
import pandas as pd

# Read csv files to dataframes
project_path = os.getenv("ecomm")

customer_csv_path = os.path.join(project_path, "faker_dataset", "faker_csv", "fake_customers.csv")
product_csv_path = os.path.join(project_path, "faker_dataset", "faker_csv", "fake_products.csv")
output_path = os.path.join(project_path, "faker_dataset", "faker_csv", "fake_email_orders.csv")

df_customers = pd.read_csv(customer_csv_path) 
df_products = pd.read_csv(product_csv_path)

import random
import time
from datetime import datetime, timedelta
from faker import Faker
from faker.providers import DynamicProvider

# Define the number of rows
number_of_rows = 400

# Define a function to generate random number for order number and payment reference
def random_number():
    return f"#{random.randint(100000000000, 999999999999)}"

# Define the list for customers, products, and payment methods
customers_list = df_customers['Full Name'].tolist()
products_list = df_products['Title'].tolist()
payment_methods = ["PayPal","Digital Wallet","Cash on Delivery","Bank Transfer"]

# Get yesterdays date 
yesterday = datetime.now().date() - timedelta(days=1)

data = []

for _ in range(number_of_rows): 
    order_number = random_number()
    order_date = datetime.combine(yesterday, datetime.min.time()) + timedelta(seconds=random.randint(0, 86399))
    billing_name = random.choice(customers_list)
    payment_method = random.choice(payment_methods)
    payment_reference = random_number()

    # Each order has 1–3 products (line items)
    for _ in range(random.randint(1, 3)):
        lineitem_name = random.choice(products_list)
        lineitem_qty = random.randint(1, 3)

        # Merge customer info
        customer_info = df_customers.loc[df_customers['Full Name'] == billing_name].to_dict('records')[0]
        # Merge product info
        product_info = df_products.loc[df_products['Title'] == lineitem_name].to_dict('records')[0]

        order_dict = {
            'order_number': order_number,
            'order_date': order_date,
            'billing_name': billing_name,
            'lineitem_name': lineitem_name,
            'lineitem_qty': lineitem_qty,
            'payment_method': payment_method,
            'payment_reference': payment_reference,
            'payment_date': order_date + timedelta(days=random.uniform(0, 1)),
            'fulfillment_date': order_date + timedelta(days=random.uniform(1, 2)),
        }

        # Merge additional customer & product fields, standardizing column names
        order_dict.update({k.lower().replace(' ', '_'): v for k, v in customer_info.items() if k != 'Full Name'})
        order_dict.update({k.lower().replace(' ', '_'): v for k, v in product_info.items() if k != 'Title'})

        data.append(order_dict)

# Convert to DataFrame
orders_df = pd.DataFrame(data)

# Drop any unnecessary columns if needed
columns_to_drop = ['first_name', 'last_name', 'product_description', 'product_category', 'image_src']
orders_df = orders_df.drop(columns=[col for col in columns_to_drop if col in orders_df.columns])


import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# -- Email Configuration --
email_sender = 'salac.jamesrhode77@gmail.com'
email_password = os.getenv('EMAIL_APP_PASSWORD')
email_recipient = 'salacjamesrhode23@gmail.com'


# -- Ensure payment_date is read as datetime --
orders_df['payment_date'] = pd.to_datetime(orders_df['payment_date'], errors='coerce')

# -- Create SSL context --
context = ssl.create_default_context()

# -- Group orders by customer name --
grouped = orders_df.groupby('billing_name')

# -- Connect once to SMTP server --
with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
    smtp.login(email_sender, email_password)

    for customer_name, orders in grouped:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = f"[demo-store] Order Confirmation for {customer_name}"
        msg["From"] = email_sender
        msg["To"] = email_recipient

        first_order = orders.iloc[0]
        order_date_display = first_order['order_date'] if 'order_date' in orders.columns else ''

        # -- Build order table --
        rows_html = ""
        total_amount = 0
        for _, row in orders.iterrows():
            line_total = row['lineitem_qty'] * row['unit_price']
            total_amount += line_total
            rows_html += f"""
            <tr>
                <td>{row['lineitem_name']}</td>
                <td>{row['product_sku']}</td>
                <td>{row['lineitem_qty']}</td>
                <td>₱{row['unit_price']}</td>
                <td>₱{line_total:.2f}</td>
            </tr>
            """

        rows_html += f"""
        <tr style="font-weight:bold; background-color:#f2f2f2;">
            <td colspan="4" style="text-align:right;">Total Amount</td>
            <td>₱{total_amount:.2f}</td>
        </tr>
        """

        # Use current timestamp when email is created
        current_timestamp = datetime.now()
        payment_date_display = current_timestamp.strftime("%Y-%m-%d %H:%M:%S")


        html_content = f"""
        <html>
        <body>
            <h2>Order Confirmation</h2>
            <p><b>Customer:</b> {customer_name}</p>
            <p><b>Order Date:</b> {order_date_display}</p>

            <h3>Order Summary</h3>
            <table border="1" cellpadding="5" cellspacing="0">
                <tr><th>Product</th><th>SKU</th><th>Qty</th><th>Price</th><th>Line Total</th></tr>
                {rows_html}
            </table>

            <h3>Payment Details</h3>
            <p><b>Payment Method:</b> {first_order['payment_method']}</p>
            <p><b>Payment Reference:</b> {first_order['payment_reference']}</p>
            <p><b>Payment Date:</b> {payment_date_display}</p>

            <hr>
            <p>This is a demo confirmation email for testing purposes only.</p>
        </body>
        </html>
        """

        msg.attach(MIMEText(html_content, "html"))

        smtp.sendmail(email_sender, email_recipient, msg.as_string())
        print(f"Sent consolidated email for {customer_name} to {email_recipient}")

        # <-- Add 2-second delay here -->
        import time
        time.sleep(2)