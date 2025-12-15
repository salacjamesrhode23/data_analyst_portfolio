FROM astrocrpublic.azurecr.io/runtime:3.1-7

# install dbt into a virtual environment
RUN python -m venv dbt_venv && source dbt_venv/bin/activate && \
    pip install --no-cache-dir dbt-snowflake && deactivate

# COPY gcp_key/gcp_sa.json /usr/local/airflow/gcp_sa.json
# ENV GOOGLE_APPLICATION_CREDENTIALS=/usr/local/airflow/gcp_sa.json
