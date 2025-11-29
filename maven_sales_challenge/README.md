## Maven Sales Challenge

**Role:** Data Analyst | BI Developer <br>
**Tools Used:** Power BI (DAX, Visualization), PostgreSQL, SQL-based tranformation (dbt) <br>
                Airflow (Workflow Orchestration), Docker 

### 🔍 Problem
In an effort to become a data-driven organization, MavenTech, a company that specializes in selling computer hardware to large businesses, aims to create an interactive dashboard that allows sales managers to monitor their team’s quarterly performance and identify areas for improvement. The company has been using a new CRM system to track sales opportunities but currently lacks visibility into the data outside the platform.

### 🎯 Objectives  
- Create an interactive dashboard for sales manager to track their team and agents quarterly performance.
- Highlight key focus areas to help sales managers maximize opportunities and improve team performance.
- Support sales managers in understanding how well their team is performing against other teams and business averages.

### ⚙️ Solution Approach

**Datasets:** <br>
In real-world environments, datasets are continuously updated. However, this project initially used static CSV files. To simulate a dynamic, real-time data source, each dataset was uploaded to Google Sheets and converted into a public CSV export link. This approach allowed Airflow to pull updated data automatically, mimicking a live production scenario.

**Docker Containers:** <br>
Two Docker containers were provisioned for this project, one for Airflow and another for dbt + PostgreSQL. Both containers are connected through an external Docker network, enabling communication and shared volumes so Airflow can execute dbt commands.<br>

- Container 1: PostgreSQL + pgAdmin + dbt-core<br>
This container hosts the PostgreSQL database, which serves as the project’s data warehouse. To simplify database exploration and debugging, pgAdmin is also included for GUI-based access. The container also includes dbt-core, which performs data modeling and transformation tasks inside the warehouse to prepare business-ready datasets.

- Container 2: Custom Airflow Image<br>
This container runs Airflow using a custom image that includes additional providers specified in the requirements.txt. Airflow orchestrates the weekly ingestion workflow, scheduled to run every Monday at 12:00 AM, pulling fresh data from the public CSV export links into the PostgreSQL database.<br>
After ingestion, Airflow triggers dbt commands (dbt debug, dbt deps, and dbt run) to validate connections, install dependencies, and apply transformations.


**dbt Transformation** <br>
The dbt project files remain on the local machine, but the project directory is mounted as a shared volume inside the dbt container. This setup allows dbt to run transformations directly within the Docker environment while keeping the code version-controlled locally. Dbt generates a dedicated schema for transformed, analysis-ready datasets. Models are structured within this schema, and built-in dbt tests are applied to enforce business rules and maintain data quality throughout the pipeline.

**PowerBI dashboard** <br>
The interactive Power BI dashboard is divided into three sections aligned with the project objectives: <br>
- **First Page (Landing Page):** Focuses on visuals that provide managers with instant insights into how their teams are tracking against KPIs and how individual agents are performing. <br>
- **Second Page:** Highlights the products, sectors, and accounts the team should focus on, as they contribute the most to sales. It also provides suggested markup percentages for the strategic selling of products. <br>
- **Third Page:** Highlights the team’s performance compared to other sales teams across various metrics. Managers can see how their teams rank within the overall business and whether they are performing above or below average.

![Data Architecture](https://github.com/salacjamesrhode77/portfolio_assets/blob/main/images/maven_sales_challenge/data_architecture.png?raw=true)

### 📈 Key Results

✅ Highlighted underperforming sales agents and tracked team performance against KPIs. <br>
✅ Identified top products, sectors, and accounts driving 80% of sales and determined optimal markup strategies. <br>
✅ Enabled Sales Managers to benchmark team performance against other sales teams and overall business averages. <br>

### 📊 Final Deliverables

[![Watch the demo](https://img.youtube.com/vi/suQ2LIrzfYU/hqdefault.jpg)](https://www.youtube.com/watch?v=suQ2LIrzfYU)


