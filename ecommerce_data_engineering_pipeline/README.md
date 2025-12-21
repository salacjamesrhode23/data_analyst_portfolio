## E-commerce Data Engineering Pipeline

**Role:** Data Engineer <br>
**Tools Used:** Airflow, Docker, Google Cloud Platform (Cloud Storage, Compute Engine, CloudSQL), Snowflake <br>
                SQL-based transformation (dbt), Python scripts and DAGs

### 🔍 Problem (TAKE REFERENCE TO SOME JOB POSTS AND JOB DESCRIPTIONS)
In today’s data-driven eCommerce landscape, businesses must manage rapidly growing volumes of transactional, customer, and product data. Efficiently collecting, processing, and analyzing this diverse data is challenging due to inconsistent formats, disparate sources, and the need for real-time updates. Without a robust and scalable data engineering pipeline, organizations struggle to transform raw data into actionable insights for decision-making, operational optimization, and customer experience enhancement.


### 🎯 Objectives
- Design and implement a scalable and automated ELT pipeline to ingest, process, and centralize data from multiple dynamic and static sources.
- Transform raw data into clean, standardized, and analytics-ready tables suitable for BI reporting and machine learning applications.
- Establish a reproducible, containerized environment using Docker and Airflow to facilitate collaboration, monitoring, and deployment.


### ⚙️ Solution Approach

**Datasets:** <br>
The objective of this project is to extract data from multiple sources and unify them in a centralized data warehouse. Since no single public dataset can fully satisfy the requirement, a custom synthetic dataset was created using the Faker library.

Several Python scripts were developed to simulate realistic data sources:

For dimensions data sources:
A Flask-based RESTful API is created to load customers and product data from csv files then exposes endpoints for queries to retrived the data.

For transactions data sources:
Fake order generator scripts are created to generate multiple logical sources:

Email source: Generates daily confirmation emails containing order transaction details for selected locations for the most recent month (December 2025).

Database source: Generates daily orders data then ingest to CloudSQL Postgres database for selected location for the most recent month (December 2025)

Static historical data: Generates Big Data (10 years of historical orders data) stored as repartitioned parquet files.



**Docker Containers:** <br>
To make the pipeline works the same way in any environment making it scallable and easier to collaborate with. Docker container were used. Two Docker containers were provisioned for this project:

Fake Data Generator Container:
The Docker cotnainer that runs the python scripts to generate synthetic data . This container uses a lightweight Docker setup only as data generation is not the primary focus of this project and also to avoid conflict with port mapping with the other container.

Airflow Container:
The docker container that runs the main orchestration layer (extracting data from sources to loading to data warehouse then perform data transformation). Astro CLI was used to scaffold the environment for this container, a platform that simplifies the deployment, monitoring, and management of Apache Airflow workflows.


**Data Ingestion** <br>
Custom python functions/scripst were create to ingest data from dynamic sources:
For api data source the scripts fetch customer and products by requesting data to the api then convert the json response to csv which will be uploaded to Google Cloud Storage bucket and then load it to Snowflake data warehouse

For email data sources, the scripts incrementally extract order details by tracking the last processed email timestamp in cloud storage, fetching only new email confirmations, parsing them into structured data, then upload the results as CSV files to a Google Cloud Storage bucket and then load it to Snowflake data warehouse

For database sources, the scripts incrementally extracts new order records from a Cloud SQL PostgreSQL database by tracking the last processed row ID in Google Cloud Storage, fetches only unseen rows, then upload the results as CSV files to a Google Cloud Storage bucket and then load it to Snowflake data warehouse

Lastly, for the parquet files considering it is a statics data source it is just simply uploaded to Google Cloud Storage bucket and loaded directly to Snowflake 

**Snowflake Setup** <br>
Before data can be loaded to Snowflake. It must have a destination first so first Database and schema must be created.After that setup an external stage pointing to the GCS bucket using a storage integration that securely connects Snowflake to GCS bucket. Once everything is setup you can now create the target tables, inspect the dataset in the stage thorougly to know the data structure (column types) before loading data to it. For statics files you can create a quesry to directly load data to it but for dynamic files loading is executed via Airflow Dags

**dbt Transformation** <br>
dbt is used to perform in-warehouse transformations within Snowflake, converting loaded raw data into analytics-ready datasets.

The dataset is processed throughout different layers to make it usable:
Staging - Clean and standardize raw source data usually (One-to-one with raw source tables)
Intermediate - Perform complex transformations by applying calculations, deduplications, and combining multiple staging models either by performing joins or union
Marts - Dataset exposed to end-users, business-focused models (facts & dimensions), aggregated, and optimized for BI tools and analysts.

For development the dbt project exists at the repository root allowing testing without running the whole pipeline. A duplicate copy of the dbt project must be then included inside the Airflow DAGs directory so it can be executed as part of the ELT pipeline.


**Data Serving (Next Projects)** <br>
The transformed and aggregated datasets are designed for downstream consumption, including:

Business Intelligence:
Data marts can be visualized using tools such as Power BI or Tableau to support self-service analytics and dashboards.

Machine Learning:
Processed datasets can be used as inputs to machine learning models for advanced analytics and predictive use cases.


![Data Architecture](https://github.com/salacjamesrhode77/portfolio_assets/blob/main/images/ecommerce_data_engineering_pipeline/data_architecture.png?raw=true)

### 📈 Key Results

✅ Built a scalable ELT pipeline to collect and centralize 6 million rows of synthetic data from APIs, emails, database and parquet files into Snowflake data warehouse.  <br>
✅ Automated data ingestion and processing using Python scripts and SQL/dbt models, transforming raw datasets into analytics-ready tables for BI and data analytics. <br>

This project draws inspiration from: 
Build an End-to-End Data Engineering Pipeline for eCommerce with the Modern Data-Stack by sclauguico
Data Engineering Zoomcamp: A Free 9-Week Course on Data Engineering Fundamentals


