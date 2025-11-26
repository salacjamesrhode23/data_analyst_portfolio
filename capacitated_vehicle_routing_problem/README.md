## Capacitated Vehicle Routing Problem with Time Windows

**Role:** Data Scientist | Supply Chain Analyst<br>
**Tools Used:** Python (pandas, numpy,matplotlib, seaborn) | Geospatial Analysis (geopandas, osmnx, networkx) | Google OR-Tools

### 🔍 Problem
A logistics company in Cagayan de Oro City aims to reduce operational costs by minimizing delivery time and fuel consumption, while ensuring that all customer orders are delivered within their specified service time windows. The challenge is to solve this vehicle routing problem using any methods or tools at your disposal.

### 🎯 Objectives
Determine the optimal routes for the company's fleet of vehicles ensuring that:
- Each vehicle visits every assigned customer exactly once. 
- Deliveries are completed within each customer’s designated time window.
- Vehicle capacities are not exceeded during delivery operations.

### ⚙️ Solution Approach

**Import Libraries and Data Collection:** <br>
Necessary libraries for data processing, geospatial analysis, optimization, and visualization are imported. Depot and customer data are loaded from the provided JSON file, and the relevant network data are extracted and loaded from OpenStreetMap using the OSMnx library.

**Data Cleaning and Preprocessing:** <br>
**Roads:** Relevant columns from the edges dataset are selected to be part of road data. The data is then filtered to include only roads suitable for trucks, since the fleet consists of truck vehicles. Columns are checked for multiple values, if a cell contains multiple values, only the first one is kept. For columns with missing data, imputation is performed to fill in the gaps. To decide for the appropriate values, a distribution is plotted, visualized, and analyzed <br>
**Nodes:** The nodes are filtered to include only those that are connected to the selected edges. <br>
**Cost Matrix:** A cost matrix is created using the location points from the JSON data. Each value in the matrix represents the shortest path length (i.e., travel time) between two locations, calculated using the Haversine function.

**Optimization Model and Solution:** <br>
Using Google OR-Tools, set up a route planner to find the best routes. Define functions to specify the demand at each customer location and the travel time between locations, including service time. Set the rules, such as time windows and capacity constraints, and ensure that the truck departs from the warehouse at the allowed time.

**Results and Overview:** <br>
A function is defined to process the results of the Vehicle Routing Problem solution and display them on a graph. The results are as follows:

![Results Overview](https://github.com/salacjamesrhode77/portfolio_assets/blob/main/images/capacitated_vehicle_routing_problem/results_overview.jpg?raw=true)

![Route Visualization](https://github.com/salacjamesrhode77/portfolio_assets/blob/main/images/capacitated_vehicle_routing_problem/route_visualization.jpg?raw=true)

### 📈 Key Results <br>
✅ Extracted and processed 42,814 edges and 17,434 nodes from OpenStreetMap to model road networks in Cagayan de Oro City and solve the Capacitated Vehicle Routing Problem with Time Windows (CVRPTW).<br> 
✅ Optimized delivery routes for a fleet of vehicles, ensuring that all deliveries were completed within the 9-hour operating window while meeting customer demands and time constraints.


### 📊 Final Deliverables
[View full project](final_deliverables/Capacitated_Vehicle_Routing_Problem_with_Time_Windows.ipynb)
