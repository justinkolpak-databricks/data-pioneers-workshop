# Databricks notebook source
# MAGIC %md
# MAGIC # Lab 2: Dashboard Lab
# MAGIC In this lab, we will build an AI/BI Dashboard to view and understand metrics about customers that are potentially going to Churn!
# MAGIC
# MAGIC AI/BI Dashboards allows business users to create dashboards and visualizations from your data to enable data-driven decision-making for everyone. Users can generate detailed reports containing insights into performance, trends and key metrics to empower users to act on what their data tells them.

# COMMAND ----------

# MAGIC %md
# MAGIC # What are we going to build
# MAGIC We are going to build a Customer churn dashboard with preditictive KPIs that helps you understand the current state of risk and identify the customers that are potentially going to churn. Here's how the dashboard is going to look. 
# MAGIC
# MAGIC ![](./Images/aibi_dashboard/Dashboard Final.png)

# COMMAND ----------

# MAGIC %md
# MAGIC # Features covered in this lab
# MAGIC
# MAGIC - Part 1: Add Dataset and Calculated Measures
# MAGIC - Part 2: Design widgets with different visualizations
# MAGIC - Part 3: Configure Filter with parameters
# MAGIC - Part 4: Publish and Embed Dashboards
# MAGIC
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC ##Part 1: Add Datasets
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC ### 1.1: Create Dashboard
# MAGIC
# MAGIC Navigate to the side panel menu --> SQL --> Dashboards. Click "Create Dashboard" to create a new Dashboard.
# MAGIC
# MAGIC ![](./Images/aibi_dashboard/Create Dashboard.png)

# COMMAND ----------

# MAGIC %md
# MAGIC ### 1.2: Rename and to go Data tab
# MAGIC
# MAGIC Rename the Dashboard to "{Unique prefix} Churn Prediction Dashboard" and click on "Data" to add Datasets.
# MAGIC
# MAGIC ![](./Images/aibi_dashboard/Dashboard Rename.png)

# COMMAND ----------

# MAGIC %md
# MAGIC ### 1.3: Click on "Create from SQL" to add the first dataset
# MAGIC
# MAGIC ![](./Images/aibi_dashboard/Dashboard Add Dataset1.png)

# COMMAND ----------

# MAGIC %md
# MAGIC ### 1.4: Add the following datasets 
# MAGIC
# MAGIC Important : Execute the sql query to ensure you get results.
# MAGIC
# MAGIC | Dataset Name | SQL Query |
# MAGIC | ----------- | ----------- |
# MAGIC | Churn - Monthly Revenue Risk - Universal | SELECT amount FROM data_pioneers.c360.churn_orders o left join data_pioneers.c360.churn_users cu on o.user_id = cu.user_id WHERE month(to_timestamp(o.creation_date, 'MM-dd-yyyy HH:mm:ss')) = (select max(month(to_timestamp(creation_date, 'MM-dd-yyyy HH:mm:ss'))) from data_pioneers.c360.churn_orders) and o.user_id in (SELECT user_id FROM data_pioneers.c360.churn_users WHERE churn=1); |
# MAGIC | Churn - Subscriptions based on Internet Service | select platform, churn, count(*) as event_count from data_pioneers.c360.churn_app_events inner join data_pioneers.c360.churn_users using (user_id) where platform is not null group by platform, churn |
# MAGIC | Churn - Predicted Churn Percent Payment Method - Universal | SELECT p.country, p.churn, count(*) as customers FROM data_pioneers.c360.churn_features p GROUP BY p.country, p.churn |
# MAGIC | Churn - At-Risk Customers - Universal | SELECT count(*)/12 as at_risk FROM data_pioneers.c360.churn_users WHERE churn=1 |
# MAGIC | Churn - Customer Breakdown - Universal | SELECT canal, count(*) as users_count FROM data_pioneers.c360.churn_features  WHERE churn =1  and canal is not null GROUP BY canal |
# MAGIC | Churn - Total MRR - Universal | SELECT sum(amount)/10 as MRR FROM data_pioneers.c360.churn_orders o left join data_pioneers.c360.churn_users cu on o.user_id = cu.user_id WHERE (month(to_timestamp(o.creation_date, 'MM-dd-yyyy HH:mm:ss')) = (select max(month(to_timestamp(creation_date, 'MM-dd-yyyy HH:mm:ss'))) from data_pioneers.c360.churn_orders)); |
# MAGIC | Churn - Predicted to Churn - Universal | SELECT user_id, churn from data_pioneers.c360.churn_users where churn=1 |
# MAGIC | Churn - Predictions - Universal | SELECT cast(days_since_creation/30 as int) as days_since_creation, churn, count(*) as customers FROM data_pioneers.c360.churn_features GROUP BY days_since_creation, churn having days_since_creation < 1000 |
# MAGIC | Churn - Country Filter | select distinct country from data_pioneers.c360.churn_users;|
# MAGIC
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC ### 1.5: Add Calculated Measure
# MAGIC
# MAGIC In AI/BI dashboards, visualizations are based on datasets defined in the Data tab. Calculated measures provide a way to create and visualize new data fields without altering the original dataset.
# MAGIC
# MAGIC Click on "Calculated Measure" button for the dataset "Churn - Monthly Revenue Risk - Universal" as shown below. 
# MAGIC
# MAGIC ![](./Images/aibi_dashboard/Dashboard CalcMeasure 1.png)

# COMMAND ----------

# MAGIC %md
# MAGIC ### 1.6: Configure the Calculated Measure
# MAGIC
# MAGIC Configure the Calculated Measure and click on Create button.
# MAGIC - **Name** : MRR_at_risk
# MAGIC - **Expression** : sum(amount)/100
# MAGIC
# MAGIC ![](./Images/aibi_dashboard/Dashboard CalcMeasure 2.png)

# COMMAND ----------

# MAGIC %md
# MAGIC ##Part 2: Add Widgets to build the Dashboard
# MAGIC
# MAGIC Now that we have all the datasets defined, we can start building the dashboard by adding Widgets.
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC ### 2.1: Add your first Widget!
# MAGIC
# MAGIC Click on the Canvas tab followed by the Widget icon from the bottom of the screen to add a new Widget to the Dashboard.
# MAGIC
# MAGIC ![](./Images/aibi_dashboard/Dashboard Add Widget1.1.png)

# COMMAND ----------

# MAGIC %md
# MAGIC
# MAGIC ### 2.2: Add a Metric - "Total MRR ($)"
# MAGIC
# MAGIC In the Widget panel on the right hand side, select the following options as shown in the image below
# MAGIC
# MAGIC - **Title Checkbox** : Enabled
# MAGIC - **Title Value** : Total MRR ($)
# MAGIC - **Dataset** : Churn - Total MRR - Universal
# MAGIC - **Visualization** : Counter 
# MAGIC - **Value** : MRR
# MAGIC
# MAGIC
# MAGIC ![](./Images/aibi_dashboard/Dashboard Add Widget1.2.png)

# COMMAND ----------

# MAGIC %md
# MAGIC
# MAGIC ### 2.3: Format the visualiztion
# MAGIC
# MAGIC Change the default formatting to remove decimals by clicking on the 'value' dropdown box and navigating to ‘Format’ tab as shown in the image below.
# MAGIC
# MAGIC
# MAGIC
# MAGIC ![](./Images/aibi_dashboard/Dashboard Add Widget1.3.png)

# COMMAND ----------

# MAGIC %md
# MAGIC
# MAGIC ### 2.4: Add the Widget - "Predicted Churn - Monthly Revenue Risk ($)"
# MAGIC
# MAGIC Click on Widget button from the bottom to add a another Widget. In the Widget panel on the right hand side, select the following options as shown in the image below
# MAGIC
# MAGIC - **Title Checkbox** : Enabled
# MAGIC - **Title Value** : Predicted Churn - Monthly Revenue Risk ($)
# MAGIC - **Dataset** : Churn - Monthly Revenue Risk - Universal
# MAGIC - **Visualization** : Counter 
# MAGIC - **Value** : MRR_at_risk
# MAGIC
# MAGIC
# MAGIC ![](./Images/aibi_dashboard/Dashboard Add Widget2.png)

# COMMAND ----------

# MAGIC %md
# MAGIC
# MAGIC ### 2.5: Add the Widget - "At-Risk Customers"
# MAGIC
# MAGIC Click on Widget button from the bottom to add a another Widget. In the Widget panel on the right hand side, select the following options as shown in the image below
# MAGIC
# MAGIC - **Title Checkbox** : Enabled
# MAGIC - **Title Value** : At-Risk Customers
# MAGIC - **Dataset** : Churn - At-Risk Customers - Universal
# MAGIC - **Visualization** : Counter 
# MAGIC - **Value** : at_risk
# MAGIC
# MAGIC
# MAGIC ![](./Images/aibi_dashboard/Dashboard Add Widet3.1.png)

# COMMAND ----------

# MAGIC %md
# MAGIC
# MAGIC ### 2.6: Format the visualiztion
# MAGIC
# MAGIC Change the default formatting to remove decimals by clicking on the 'value' dropdown box and navigating to ‘Format’ tab as shown in the image below.
# MAGIC
# MAGIC
# MAGIC
# MAGIC ![](./Images/aibi_dashboard/Dashboard Add Widet3.2.png)

# COMMAND ----------

# MAGIC %md
# MAGIC
# MAGIC ### 2.7: Add the Widget - "Predicted as Churn - Customer Tenure"
# MAGIC
# MAGIC Click on Widget button from the bottom to add a another Widget. In the Widget panel on the right hand side, select the following options as shown in the image below
# MAGIC
# MAGIC - **Title Checkbox** : Enabled
# MAGIC - **Title Value** : Predicted as Churn - Customer Tenure
# MAGIC - **Dataset** : Churn - Predictions - Universal
# MAGIC - **Visualization** : Bar
# MAGIC - **X axis** : days_since_creation
# MAGIC - **Y axis** : SUM(customers)
# MAGIC - **Color** : churn
# MAGIC
# MAGIC
# MAGIC ![](./Images/aibi_dashboard/Dashboard Add Widet4.png)

# COMMAND ----------

# MAGIC %md
# MAGIC
# MAGIC ### 2.8: Add the Widget - "At Risk Customers - Have Device Protection"
# MAGIC
# MAGIC Click on Widget button from the bottom to add a another Widget. In the Widget panel on the right hand side, select the following options as shown in the image below
# MAGIC
# MAGIC - **Title Checkbox** : Enabled
# MAGIC - **Title Value** : At Risk Customers - Have Device Protection
# MAGIC - **Dataset** : Churn - Customer Breakdown - Universal
# MAGIC - **Visualization** : Pie
# MAGIC - **Angle** : SUM(users_count)
# MAGIC - **Color** : canal
# MAGIC - **Labels** : Enabled
# MAGIC
# MAGIC
# MAGIC ![](./Images/aibi_dashboard/Dashboard Add Widet5.png)

# COMMAND ----------

# MAGIC %md
# MAGIC
# MAGIC ### 2.9: Add the Widget - "Percent Predicted Churn - Payment Method"
# MAGIC
# MAGIC Click on Widget button from the bottom to add a another Widget. In the Widget panel on the right hand side, select the following options as shown in the image below
# MAGIC
# MAGIC - **Title Checkbox** : Enabled
# MAGIC - **Title Value** : Percent Predicted Churn - Payment Method
# MAGIC - **Dataset** : Churn - Predicted Churn Percent Payment Method - Universal
# MAGIC - **Visualization** : Bar
# MAGIC - **X axis** : churn
# MAGIC - **Y axis** : customers
# MAGIC - **Color** : country
# MAGIC
# MAGIC
# MAGIC ![](./Images/aibi_dashboard/Dashboard Add Widet6.png)

# COMMAND ----------

# MAGIC %md
# MAGIC
# MAGIC ### 2.10: Add the Widget - "Percent Predicted Churn - Payment Method"
# MAGIC
# MAGIC Click on Widget button from the bottom to add a another Widget. In the Widget panel on the right hand side, select the following options as shown in the image below
# MAGIC
# MAGIC - **Title Checkbox** : Enabled
# MAGIC - **Title Value** : Percent Predicted Churn - Payment Method
# MAGIC - **Dataset** : Churn - Predicted Churn Percent Payment Method - Universal
# MAGIC - **Visualization** : Bar
# MAGIC - **X axis** : churn
# MAGIC - **Y axis** : customers
# MAGIC - **Color** : country
# MAGIC
# MAGIC
# MAGIC ![](./Images/aibi_dashboard/Dashboard Add Widet6.png)

# COMMAND ----------

# MAGIC %md
# MAGIC
# MAGIC ### 2.11: Add the Widget - "Customers Predicted to Churn"
# MAGIC
# MAGIC Click on Widget button from the bottom to add a another Widget. In the Widget panel on the right hand side, select the following options as shown in the image below
# MAGIC
# MAGIC - **Title Checkbox** : Enabled
# MAGIC - **Title Value** : Customers Predicted to Churn
# MAGIC - **Dataset** : Churn - Predicted to Churn - Universal
# MAGIC - **Visualization** : Table
# MAGIC - **Columns** : Show/hide all
# MAGIC
# MAGIC ![](./Images/aibi_dashboard/Dashboard Add Widet7.png)

# COMMAND ----------

# MAGIC %md
# MAGIC
# MAGIC ### 2.12: Add the Widget - "Churn - Subscriptions based on Internet Service"
# MAGIC
# MAGIC Click on Widget button from the bottom to add a another Widget. In the Widget panel on the right hand side, select the following options as shown in the image below
# MAGIC
# MAGIC - **Title Checkbox** : Enabled
# MAGIC - **Title Value** : Churn - Subscriptions based on Internet Service
# MAGIC - **Dataset** : Churn - Predicted to Churn - Universal
# MAGIC - **Visualization** : Bar
# MAGIC - **X axis** : SUM(event_count)
# MAGIC - **Y axis** : platform
# MAGIC - **Color** : churn
# MAGIC - **Scale Type** : Categorical
# MAGIC - **Transform** : None
# MAGIC
# MAGIC
# MAGIC ![](./Images/aibi_dashboard/Dashboard Add Widet8.png)

# COMMAND ----------

# MAGIC %md
# MAGIC ##Part 3: Add Parameters and Filter
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC
# MAGIC ### 3.1 In order to add a filter to the dashboard, we'll first have to add a filter with parameter to each dataset (except two datasets listed in step 3.3) as shown below.
# MAGIC
# MAGIC - **Filter query** : and array_contains(:country, country)
# MAGIC - **Parameter settings -> Allow multiple selections** : Checked
# MAGIC
# MAGIC ![](./Images/aibi_dashboard/Dashboard Filter 1.png)

# COMMAND ----------

# MAGIC %md
# MAGIC
# MAGIC ### 3.2 In the country parameter, enter the values as USA, FR & SPAIN followed by executing the query for each of the datasets. 
# MAGIC
# MAGIC - **Parameter Values** : USA, FR, SPAIN
# MAGIC
# MAGIC ![](./Images/aibi_dashboard/Dashboard Filter 2.png)

# COMMAND ----------

# MAGIC %md
# MAGIC
# MAGIC 3.3 For the following two datasets, add the filter query with 'where' condition and add the parameter values followed by executing the query.
# MAGIC
# MAGIC - **Datasets** : 
# MAGIC > - Churn - Predicted Churn Percent Payment Method - Universal
# MAGIC > - Churn - Predictions - Universal
# MAGIC - **Filter query** : where array_contains(:country, country)
# MAGIC - **Parameter settings -> Allow multiple selections** : Checked
# MAGIC - **Parameter Values** : USA, FR, SPAIN
# MAGIC - Execute the query
# MAGIC
# MAGIC ![](./Images/aibi_dashboard/Dashboard Filter 3.png)

# COMMAND ----------

# MAGIC %md
# MAGIC
# MAGIC 3.4 Now we are ready to add the filter to the dashboard. Click on the Canvas tab at the top and click the Filter button at the bottom of the screen as shown in the image below
# MAGIC
# MAGIC ![](./Images/aibi_dashboard/Dashboard Filter 4.png)

# COMMAND ----------

# MAGIC %md
# MAGIC
# MAGIC 3.5 Follow the below steps to add the filter - Country
# MAGIC
# MAGIC - **Title** : Country
# MAGIC - **Filter** : Multiple values
# MAGIC - **Field** : Churn - Country Filter -> country
# MAGIC
# MAGIC ![](./Images/aibi_dashboard/Dashboard Filter 5.png)

# COMMAND ----------

# MAGIC %md
# MAGIC
# MAGIC 3.6 Add the parameter - customer from each of the datasets to associate it with the filter.
# MAGIC
# MAGIC - **Parameters** : Dataset -> country
# MAGIC
# MAGIC ![](./Images/aibi_dashboard/Dashboard Filter 6.png)

# COMMAND ----------

# MAGIC %md
# MAGIC
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC ##Part 4: Publish and Embed Dashboards
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC
# MAGIC ### 4.1 Publish Dashboard
# MAGIC
# MAGIC Click on the Publish button as shown below.
# MAGIC
# MAGIC
# MAGIC ![](./Images/aibi_dashboard/Dashboard Publish 1.png)

# COMMAND ----------

# MAGIC %md
# MAGIC
# MAGIC ### 4.2 Publish Dashboard
# MAGIC
# MAGIC Review the information and click on the Publish button as shown below.
# MAGIC
# MAGIC
# MAGIC ![](./Images/aibi_dashboard/Dashboard Publish 2.png)

# COMMAND ----------

# MAGIC %md
# MAGIC
# MAGIC ### 4.3 Create Embedding
# MAGIC
# MAGIC Click on the Share button to generate embedding iframe that can be used to embed the dashboard in applications
# MAGIC
# MAGIC
# MAGIC ![](./Images/aibi_dashboard/Dashboard Embed 1.png)

# COMMAND ----------

# MAGIC %md
# MAGIC
# MAGIC ### 4.4 Create Embedding
# MAGIC
# MAGIC Click on Embed Dashboard button to generate the iframe url as shown below.
# MAGIC
# MAGIC
# MAGIC ![](./Images/aibi_dashboard/Dashboard Embed 2.png)

# COMMAND ----------

# MAGIC %md
# MAGIC
# MAGIC ### 4.5 Create Embedding
# MAGIC
# MAGIC The generated URL can now be used to embed the dashboard in applications.
# MAGIC
# MAGIC
# MAGIC ![](./Images/aibi_dashboard/Dashboard Embed 3.png)

# COMMAND ----------

# MAGIC %md
# MAGIC ##Conclusion
