### Project Overview
[![Watch the demo](https://img.youtube.com/vi/suQ2LIrzfYU/hqdefault.jpg)](https://www.youtube.com/watch?v=suQ2LIrzfYU)

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
In real-world application, datasets are continuously updated. However, this challenge gives a static source of data (CSV files). To simulate a dynamic, real-time data source, all csv files were uploaded to Google Sheets and converted into a public CSV export link. This approach allowed Airflow to pull updated data automatically, mimicking a live production scenario.

**Docker:** <br>
Two docker compose projects were provisioned for this project, one for Airflow services and another for dbt + PostgreSQL + pgAdmin setup. Both docker compose projects are connected via an external Docker network which enables communication and shared volumes so Airflow services can execute dbt commands.<br>

**Pipeline** <br>
Tables were created in PostgreSQL to set up the database for incoming data from CSV files. Data from public CSV exports were then downloaded as temporary files to enable the COPY command in Postgres to load them into the database. After loading, the temporary CSV files were deleted. Finally, a series of dbt commands transformed the data within the database, producing datasets ready for analysis and visualization.

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


**Acknowledgements/References:** <br  >

This dashboard was inspired by the insights and design recommendations shared during the **Maven Sales Challenge – Winner Selection Voting**.

In particular, I’d like to acknowledge the work of:
- **Kerryn Gresswell**
- **Gerard Duggan**
- **Vince McSkimmings**

Their dashboards influenced the analytical focus, KPI selection, and storytelling approach used in this project.  
All implementation, data modeling, and visual design decisions are my own.



