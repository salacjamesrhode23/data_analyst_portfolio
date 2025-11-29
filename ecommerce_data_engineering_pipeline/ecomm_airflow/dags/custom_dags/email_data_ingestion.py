import os
import csv
import imaplib
import email
from email import policy
from bs4 import BeautifulSoup
from google.cloud import storage

from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

subject_filter = '"[demo-store] Order Confirmation for"'

email_bodies = fetch_email_bodies(
    user=Variable.get("EMAIL_USER"),
    password=Variable.get("EMAIL_PASSWORD"),
    subject_filter=subject_filter
)

print(f"Fetched {len(email_bodies)} emails.")
