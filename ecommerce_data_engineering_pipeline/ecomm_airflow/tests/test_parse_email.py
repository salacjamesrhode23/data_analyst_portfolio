# tests/test_parse_emails_to_df.py

import pandas as pd
from custom_functions.emails.process_email import parse_emails_to_df

# Sample fake email body (HTML)
SAMPLE_EMAIL = """
<html>
<body>
<table>
<tr><th>Product</th><th>SKU</th><th>Qty</th><th>Price</th><th>Line Total</th></tr>
<tr><td>Widget A</td><td>W123</td><td>2</td><td>10.00</td><td>20.00</td></tr>
<tr><td>Widget B</td><td>W456</td><td>1</td><td>15.00</td><td>15.00</td></tr>
<tr><td>Total</td><td></td><td></td><td></td><td>35.00</td></tr>
</table>
<p>Customer:</p>John Doe
<p>Order Date:</p>2025-12-09
<p>Payment Method:</p>Credit Card
<p>Payment Reference:</p>REF123
<p>Payment Date:</p>2025-12-08
</body>
</html>
"""

def test_parse_emails_to_df():
    # Call function with list of one fake email
    df = parse_emails_to_df([SAMPLE_EMAIL])

    # Assertions
    assert isinstance(df, pd.DataFrame)
    assert df.shape[0] == 2  # 2 line items
    assert df.loc[0, "product"] == "Widget A"
    assert df.loc[1, "line_total"] == "15.00"
    assert df.loc[0, "customer"] == "John Doe"
    assert df.loc[1, "total_amount"] == "35.00"
    assert df.loc[0, "payment_method"] == "Credit Card"
