import random
from datetime import datetime, timedelta
from typing import List, Dict

def generate_line_items_for_order(
    order_number: str,
    order_date: datetime,
    billing_name: str,
    payment_method: str,
    payment_reference: str,
    products: List[str],
    customer_lookup: Dict[str, dict],
    product_lookup: Dict[str, dict],
) -> List[Dict]:
    """
    Generate line items for a single order.

    Each order can have 1-3 line items. Payment info is shared across all items.
    
    Args:
        order_number (str): Unique order number.
        order_date (datetime): Date of the order.
        billing_name (str): Customer's billing name.
        payment_method (str): Payment method.
        payment_reference (str): Payment reference number.
        products (List[str]): List of available product names.
        customer_lookup (Dict[str, dict]): Dictionary mapping customer names to details.
        product_lookup (Dict[str, dict]): Dictionary mapping product names to details.

    Returns:
        List[Dict]: List of line item records for the order.
    """
    records = []

    for _ in range(random.randint(1, 3)):
        product_name = random.choice(products)

        record = {
            "order_number": order_number,
            "order_date": order_date,
            "billing_name": billing_name,
            "lineitem_name": product_name,
            "lineitem_qty": random.randint(1, 3),
            "payment_method": payment_method,
            "payment_reference": payment_reference,
            "payment_date": order_date + timedelta(days=random.uniform(0, 1)),
            "fulfillment_date": order_date + timedelta(days=random.uniform(1, 2)),
        }

        # Merge customer and product details
        record.update(customer_lookup.get(billing_name, {}))
        record.update(product_lookup.get(product_name, {}))

        records.append(record)

    return records
