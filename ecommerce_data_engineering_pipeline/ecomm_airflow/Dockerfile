FROM astrocrpublic.azurecr.io/runtime:3.1-7

# install dbt into a virtual environment
RUN python -m venv dbt_venv && source dbt_venv/bin/activate && \
    pip install --no-cache-dir dbt-snowflake && deactivate

# Set GOOGLE_APPLICATION_CREDENTIALS environment variable
ENV GOOGLE_APPLICATION_CREDENTIALS="/opt/airflow/include/gcp_key/gcp_sa.json"
