## Maven Sales Challenge

Role: Data Analyst | BI Developer
Tools Used : Power BI (DAX, Visualization), CloudSQL-PostgreSQL Instance, SQL-based tranformation (dbt) 

🔍 Problem
 In an effort to become a data-driven organization. MavenTech, a company that specializes in selling computer hardware to large businesses wants to create an interactive dashboard that enables sales manger to track their team's quarterly performance and understand how they can still improve their sales performance. They been using a new CRM system to track the sales opportuniteis but they have no visibility of the data outside the platform.

🎯 Objectives  
- Create an interactive dashboard for sales manager's to track their team quarterly performance
- Suggest sales manager areas to focus for their teams effort to maximize opportunites and improve sales performance
- Create a visualization for sales manager to understand how well their team is performing compared to their peers.

⚙️ Solution Approach

Datasets:
In real world scenarios, the dataset is dynamic and continuously updated. However, the datasets used in this project are CSV files, which are static in nature. For the purpose of this project, it is assumed that new data is continuously added to simulate a dynamic environment.

CloudSQL PostgreSQL Instance:
For this project a PostgreSQL instance is spinned up in CloudSQL in GCP. The database will serve both as OLAP (tranformation from staging data to analytics ready data) and as OLTP (managing realtime task logs and execution metadata from kestra workflow orchetration)

Workflow Orchestation (Data Ingestion):
Kestra instance is spinned up with docker compose using the PostgreSQl as its database. For data ingestion, as assumed data is conitnuosly added so kestra workflow is run every week with cron jobs. The workflow orchestration is shown below 

[Add screenshot here]

dbt Transformation
data is transformed from staging to analytics ready with SQL-based tranformation

📈 Key Results
✅ Highlighted underperforming sales agents and recommended targeted areas for improvement.
✅ Identified top products, sectors, and accounts driving 80% of sales and determined optimal markup strategies.
✅ Enabled Sales Managers to benchmark team performance against peers and overall business averages.



📊 Final Deliverables

[![Watch the demo](https://img.youtube.com/vi/A4ATo3WMl-U/maxresdefault.jpg)](https://www.youtube.com/watch?v=A4ATo3WMl-U)


