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
In real-world scenarios, datasets are dynamic and continuously updated. However, the datasets used in this project are static CSV files. To simulate a live data environment, the transaction data (sales_pipeline.csv) was converted into a public CSV export from Google Sheets, allowing it to function as a dynamic, continuously updating data source.

**PostgreSQL Database:** <br>
For this project, a PostgreSQL database was created using Docker Compose. The database serves both as OLTP (handling continuous insertion of sales pipeline transactions) and OLAP (executing analytical queries to prepare business-ready datasets).

**Workflow Orchestation (Data Ingestion):** <br>
A Kestra instance was deployed using Docker Compose, with the PostgreSQL database as its backend database. For data ingestion, both the static CSV files and the Google Sheets CSV export are directly loaded into the database.Since the data is assumed to be continuously updated, the Kestra workflow is scheduled to run weekly via cron jobs to ensure data freshness.

**dbt Transformation** <br>
After all the data resides in the public (default) schema of the database, two additional schemas are created: <br>
- **Staging Schema:** Used for cleaning and standardizing raw data. <br>
- **Marts Schema:** Used for generating business-ready datasets for analysis. <br>
Models are created within these schemas, and tests are implemented to validate business logic and ensure high data quality.

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


