import os
import pandas as pd
from flask import Flask, request, jsonify

app = Flask(__name__)

# Get project root from environment variable
project_path = os.getenv("ecomm")

# Build file paths relative to project root
customer_csv_path = os.path.join(project_path, "faker_dataset", "faker_csv", "fake_customers.csv")
product_csv_path = os.path.join(project_path, "faker_dataset", "faker_csv", "fake_products.csv")

customer_df = pd.read_csv(customer_csv_path)
product_df = pd.read_csv(product_csv_path)

# Define route and endpoint -- retrieves all the customers data
@app.route("/api/customers", methods=["GET"])
def get_all_customers():
    data = customer_df.to_dict(orient="records")
    return jsonify(data), 200

# Define route and endpoint -- retrieves specific customer data by name
@app.route("/api/customers/<customer_name>", methods=["GET"])
def get_customer(customer_name):
    customer_data = customer_df[customer_df['Full Name'] == customer_name]
    if customer_data.empty:
        return jsonify({"error": "Customer not found"}), 404
    else:
        return jsonify(customer_data.to_dict(orient="records")[0]), 200

# Define route and endpoint -- retrieves all the products data
@app.route("/api/products", methods=["GET"])
def get_all_products():
    page = int(request.args.get('page', 1))
    limit = int(request.args.get('limit', 50))

    if limit > 50:
        return jsonify({"error": "Maximum limit is 50"}), 400

    start = (page - 1) * limit
    end = start + limit
    data = product_df.iloc[start:end].to_dict(orient="records")
    return jsonify(data), 200

# Define route and endpoint -- retrieves specific product data by name
@app.route("/api/products/<product_sku>", methods=["GET"])
def get_product(product_sku):
    product_data = product_df[product_df['Product SKU'] == product_sku]
    if product_data.empty:
        return jsonify({"error": "Product not found"}), 404
    else:
        return jsonify(product_data.to_dict(orient="records")[0]), 200

if __name__ == "__main__":
    app.run(debug=True)