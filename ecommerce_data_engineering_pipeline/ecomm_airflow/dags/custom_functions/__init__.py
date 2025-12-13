# Expose email functions at the package level
from .emails.process_email import process_email_orders
from .database.process_database import process_database_orders
from .snowflake.gcs_to_snowflake import load_csv_to_snowflake
from .api.process_api_customers import process_api_customers
from .api.process_api_products import process_api_products

# # Optional: define __all__ for cleaner wildcard imports
# __all__ = ["fetch_email_bodies", "email_orders_to_gcs"]
