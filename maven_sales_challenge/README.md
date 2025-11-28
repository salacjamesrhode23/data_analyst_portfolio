## Maven Sales Challenge

**Role:** Data Analyst | BI Developer <br>
**Tools Used:** Power BI (DAX, Visualization), PostgreSQL, SQL-based tranformation (dbt) <br>
                Workflow Orchestration (kestra) 

### 🔍 Problem
In an effort to become a data-driven organization, MavenTech, a company that specializes in selling computer hardware to large businesses, aims to create an interactive dashboard that allows sales managers to monitor their team’s quarterly performance and identify areas for improvement. The company has been using a new CRM system to track sales opportunities but currently lacks visibility into the data outside the platform.

### 🎯 Objectives  
- Create an interactive dashboard for sales manager to track their team and agents quarterly performance.
- Highlight key focus areas to help sales managers maximize opportunities and improve team performance.
- Support sales managers in understanding how well their team is performing against other teams and business averages.

### ⚙️ Solution Approach

**Datasets:** <br>
In real-world scenarios, datasets are dynamic and continuously updated. However, the datasets used in this project are static CSV files. To simulate a live data environment, the dataset was converted into a public CSV export in Google Sheets, allowing it to function as a dynamic, continuously updating data source.

**Docker Container:** <br>
There are 2 containers created for this project which are connected via docker network external to both containers. the purpose of these network is for both containers to share volumes so that airflow can run dbt the containers are the following: <br>

Docker Container 1 - this container contains PostgreSQL database instance which serves as datawarehouse. For convenience Pgadmin is also included in the container for viewing the database with graphical interface instead of typing command in the terminal. Additionally dbt-core is included in this container to perform transformation in the database to prepare business-ready datasets

Docker Container 2 - this container contains a custom image for airflow build with additional custom providers packages from the requirements.txt. Data ingestion tasks is run weekly to ingest weekly data from the public csv export to the database via cron jobs. After data is ingested it triggers dbt to run dbt debug, deps, an run.

**dbt Transformation** <br>
The dbt models and configuration files reside on the local machine, but the project directory is mounted as a volume in the Docker container, making it accessible inside the container. After all data is ingested into the database’s default public schema, dbt performs the transformations and creates an additional schema for generating business-ready datasets for analysis.

Models are defined within these schemas, and tests are implemented to validate business logic and ensure high data quality.


**PowerBI dashboard** <br>
The interactive Power BI dashboard is divided into three sections aligned with the project objectives: <br>
- **First Page (Landing Page):** Focuses on visuals that provide managers with instant insights into how their teams are tracking against KPIs and how individual agents are performing. <br>
- **Second Page:** Highlights the products, sectors, and accounts the team should focus on, as they contribute the most to sales. It also provides suggested markup percentages for the strategic selling of products. <br>
- **Third Page:** Highlights the team’s performance compared to other sales teams across various metrics. Managers can see how their teams rank within the overall business and whether they are performing above or below average.

![Data Architecture](https://github.com/salacjamesrhode77/portfolio_assets/blob/main/images/maven_sales_challenge/data_architecture.jpg?raw=true)

### 📈 Key Results

✅ Highlighted underperforming sales agents and tracked team performance against KPIs. <br>
✅ Identified top products, sectors, and accounts driving 80% of sales and determined optimal markup strategies. <br>
✅ Enabled Sales Managers to benchmark team performance against other sales teams and overall business averages. <br>

### 📊 Final Deliverables

[![Watch the demo](https://img.youtube.com/vi/suQ2LIrzfYU/hqdefault.jpg)](https://www.youtube.com/watch?v=suQ2LIrzfYU)


