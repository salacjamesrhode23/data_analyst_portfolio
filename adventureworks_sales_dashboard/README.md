## AdventureWorks Sales Dashboard

**Role:** Data Analyst | Excel Specialist <br>
**Tools Used:** Microsoft Excel (PowerQuery, Formulas, Pivot Tables, Charts, Slicers)

### 🔍 Challenge  
AdventureWorks, a fictional global company selling bicycles and bicycle parts, needs a way to track quarterly KPIs and growth from the previous quarter. You are provided with a folder of raw CSV files containing information on customers, products, product categories and subcategories, territories, and transactions. As a data analyst, you are tasked with creating an interactive dashboard. Since no other software is available, the solution must be built entirely in Excel.

### 🎯 Objectives  
- Design a one page interactive dashboard using only Microsoft Excel.
- Visualize changes in sales performance from the previous quarter to the current quarter.

### ⚙️ Solution Approach

**ELT (Extract, Load, Transform):** <br>
Power Query is connected to the raw CSV files. Once extracted, the data is loaded into the Power Query Editor, where it is cleaned and reshaped using step-based transformations such as changing data types, removing duplicates, and adding calculated columns. After transformation, the data is loaded into the Data Model, implementing a star schema for table relationships.

**Data Analysis:** <br>
The analysis phase involves simultaneous data exploration and visualization, supporting an iterative analytical process. Pivot Tables are primarily used to group and summarize data from the Data Model. Formulas are applied to aggregate values and calculate metrics and KPIs. Logical and lookup functions are also used when needed to enhance calculations.


**Data Visualization** <br>
- **Data Interactivity:** Slicers allow end-users to explore sales performance across different regions and product categories.
- **Charts:** Bar charts show detailed changes in sales from the previous to the current quarter for each subcategory. Multiple line charts display cumulative sales per quarter, highlighting both current and previous trends. A single line chart illustrates the current sales performance trend with a linear regression forecast.
- **KPI Cards:** Highlight key performance indicators such as Customer Count, QTD Sales, QTD Units Sold, QTD Sales Growth, Sales Forecast, and Remaining Days Before Quarter End, giving management a quick overview of overall performance.


### 📈 Key Results

✅Developed an interactive Excel Sales Dashboard using only native Excel tools, reducing analysis time for management. <br>
✅Enabled data-driven decision-making by allowing management to compare quarter-over-quarter performance and strategically plan based on forecasted sales.


### 📊 Final Deliverables

[![Watch the demo](https://img.youtube.com/vi/kjZOHPX76xE/maxresdefault.jpg)](https://www.youtube.com/watch?v=kjZOHPX76xE)

