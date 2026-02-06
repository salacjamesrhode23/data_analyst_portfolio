### Project Overview
[![Dashboard Preview](https://raw.githubusercontent.com/salacjamesrhode77/portfolio_assets/main/images/pharmacy_sales_and_profitability_dashboard/onyx_data_challenge_thumbnail_1.png)](https://app.powerbi.com/view?r=eyJrIjoiYzFhNWQ4N2EtYzNlYS00NDg3LWFhYTctMjY4YTZmMzk2ZDJlIiwidCI6IjUzYzdjMDZlLWM1ODgtNDhjNC1hZjc0LTk2Mjg1MDdhM2NkMSIsImMiOjEwfQ%3D%3D)


## Pharmacy Sales and Profitability Dashboard

**Role:** Data Analyst | BI Developer <br>
**Tools Used:** Power BI Service, Dataflow, DAX 

### 🔍 Problem
In this challenge, you will analyze a dataset representing a European pharmacy chain distributor operating across multiple European countries. The dataset includes daily sales transactions by pharmacy and product, with supporting dimensions for time, geography, and product hierarchy.

### 🎯 Objectives <br>
Your task is to build a Power BI report that helps stakeholders understand:  
- How sales and profitability vary across countries, regions, and individual pharmacies.
- How different product categories and brands perform in different locations.
- How regional performance contributes to overall business results.

Additionally, this project is guided by key business questions and analytical challenges, which are detailed [in this document](https://docs.google.com/document/d/1T973twFhLPFYHE2yWMfu1OIrpF6c2j1j/edit?usp=sharing).

### ⚙️ Solution Approach

The approach for this challenge is straightforward: address all key questions and analytical challenges by focusing on three critical areas—**Geography, Trends, and Products**—resulting in a three-page report.

**Filters:**  
On the first two pages, filters allow users to select which products to include and whether to include high-volume, low-margin items or exclude them to avoid distorting the performance report. On the third page, users can choose to include or exclude discontinued products.

Additional filters vary depending on the page focus:

- **Geography page:** filters for date and products are available.  
- **Trends page:** filters for location and products are available.  
- **Products page:** filters for location and date can be applied.

All filters are accessible via a bookmark button in the upper-right corner, along with a reset button and report guide.

**KPI Cards:**  
KPI cards are optimized not just to display key metrics but also to act as interactive filters for the entire report. This is achieved by overlaying an invisible button slicer on the cards, creating the illusion that the card itself is selectable.

---

### Page 1: Geography

From an executive or manager perspective, it is important to see how countries and regions perform across different KPIs, be able to drill down from country to region, and view the top-ranked pharmacies based on selected KPIs. To support this:

- A **bar chart with Pareto analysis** highlights top-performing countries and regions and their contribution to overall results, complemented by a **map** to show geographic patterns.  
- A **matrix table** displays pharmacy-level details, including pharmacy count and KPI contribution by type and size, along with a **performance ranking table**.  
- A **decomposition chart** allows stakeholders to explore KPIs by product categories, brands, and individual products.

---

### Page 2: Trends

Trend analysis can be overwhelming and noisy if done at the individual product level. To simplify:

- Visualizations focus on **product categories**, with tooltips showing top brands and products when hovering over line charts.  
- Charts compare **current-year vs previous-year performance**, highlight overall trend direction, and identify peak and low points.

---

### Page 3: Product Analysis

This page visualizes products classified into four quadrants:

- **Q1:** Low Volume, Low Margin  
- **Q2:** Low Volume, High Margin  
- **Q3:** High Volume, High Margin  
- **Q4:** High Volume, Low Margin  

KPI cards show the number of products in each quadrant, their percentage contribution to total profit, and normalized values for profit and volume for easier comparison.

Supporting visuals include:

- **Units Sold vs Profit Margin scatterplot:** Color gradients indicate promotional effectiveness and highlight which promotions drive volume.  
- **Promoted vs Non-Promoted Sales bar charts:** Show trade-offs between profit per unit and transaction volume.  
- **Promotion comparison YoY:** Displays whether an increase in promotions correlates with changes in profit margin.






