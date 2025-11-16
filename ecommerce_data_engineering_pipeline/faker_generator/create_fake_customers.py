import os
import pandas as pd
import random
from faker import Faker
from faker.providers import DynamicProvider

# Suppress Warnings
import warnings
warnings.filterwarnings("ignore")

fake = Faker('en_PH')

# Define paths for CSV files input and output
project_path = os.environ.get('ecomm')
csv_path = os.path.join(project_path, "faker_dataset", "faker_csv", "ph_cities.csv")
output_path = os.path.join(project_path, "faker_dataset", "faker_csv", "fake_customers.csv")

# Read ph_cities.csv to get list of cities in the Philippines
df_city = pd.read_csv(csv_path)

# Define accepted values for city using DynamicProvider
city_provider = DynamicProvider(
    provider_name="city",
    elements=df_city['City'].tolist()
)

fake.add_provider(city_provider)

# Define a function to create phone number in Philippines format
def ph_phone():
    return f"+63 9{random.randint(100000000, 999999999)}"

# Generate the initial fake customer data
data = [{
    'First Name': fake.first_name(),
    'Last Name': fake.last_name(),
    'Full Name': None,
    'Email': None,
    'Address Company': fake.street_address(),
    'Address City': fake.city(),
    'Address Province': None,
    'Address Zip': None,
    'Phone': ph_phone()
} for _ in range(10)]

# Convert data to DataFrame
customers_df = pd.DataFrame(data)

# Concatenate First Name and Last Name to create full name and email column
customers_df['Full Name'] = customers_df.apply(lambda x: f"{x['First Name']} {x['Last Name']}" if pd.isna(x['Full Name']) else x['Full Name'], axis=1)
customers_df['Email'] = customers_df.apply(lambda x: f"{x['Last Name'].lower()}.{x['First Name'].lower()}@gmail.com" if pd.isna(x['Email']) else x['Email'], axis=1)

# Lookup Province Values to replace None
customers_df['Address Province'] = customers_df['Address Province'].fillna(customers_df['Address City'].map(df_city.set_index('City')['Province']))

# Lookup ZipCode Values to replace None
customers_df['Address Zip'] = customers_df['Address Zip'].fillna(customers_df['Address City'].map(df_city.set_index('City')['ZipCode']))

customers_df.to_csv("sample1-dag.csv", index=False)
print(f"Saved {len(customers_df)} fake customers to {output_path}")