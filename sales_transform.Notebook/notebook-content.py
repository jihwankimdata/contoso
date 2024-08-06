# Fabric notebook source

# METADATA ********************

# META {
# META   "kernel_info": {
# META     "name": "synapse_pyspark"
# META   },
# META   "dependencies": {
# META     "lakehouse": {
# META       "default_lakehouse": "4c4ae86b-809f-4227-ba3a-648237cdf294",
# META       "default_lakehouse_name": "silver_contoso",
# META       "default_lakehouse_workspace_id": "3a92de98-c671-477a-b7a2-694924bba5b2",
# META       "known_lakehouses": [
# META         {
# META           "id": "4c4ae86b-809f-4227-ba3a-648237cdf294"
# META         }
# META       ]
# META     }
# META   }
# META }

# CELL ********************

# Welcome to your new notebook
# Type here in the cell editor to add code!


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

sales = spark.read.format("csv").option("header","true").load("Files/contoso/sales.csv")
# df now is a Spark DataFrame containing CSV data from "Files/contoso/sales.csv".
display(sales)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Code generated by Data Wrangler for PySpark DataFrame

from pyspark.sql import functions as F
from pyspark.sql import types as T

def clean_data(sales):
    # Change column type to int64 for columns: 'OrderKey', 'CustomerKey' and 3 other columns
    sales = sales.withColumn('OrderKey', sales['OrderKey'].cast(T.LongType()))
    sales = sales.withColumn('CustomerKey', sales['CustomerKey'].cast(T.LongType()))
    sales = sales.withColumn('StoreKey', sales['StoreKey'].cast(T.LongType()))
    sales = sales.withColumn('ProductKey', sales['ProductKey'].cast(T.LongType()))
    sales = sales.withColumn('LineNumber', sales['LineNumber'].cast(T.LongType()))
    # Change column type to float64 for columns: 'Quantity', 'UnitPrice' and 3 other columns
    sales = sales.withColumn('Quantity', sales['Quantity'].cast(T.DoubleType()))
    sales = sales.withColumn('UnitPrice', sales['UnitPrice'].cast(T.DoubleType()))
    sales = sales.withColumn('NetPrice', sales['NetPrice'].cast(T.DoubleType()))
    sales = sales.withColumn('UnitCost', sales['UnitCost'].cast(T.DoubleType()))
    sales = sales.withColumn('ExchangeRate', sales['ExchangeRate'].cast(T.DoubleType()))
    # Replace all instances of "-" with "" in columns: 'OrderDate', 'DeliveryDate'
    sales = sales.withColumn('OrderDate', F.regexp_replace('OrderDate', "(?i)-", ""))
    sales = sales.withColumn('DeliveryDate', F.regexp_replace('DeliveryDate', "(?i)-", ""))
    # Change column type to int64 for columns: 'OrderDate', 'DeliveryDate'
    sales = sales.withColumn('OrderDate', sales['OrderDate'].cast(T.LongType()))
    sales = sales.withColumn('DeliveryDate', sales['DeliveryDate'].cast(T.LongType()))
    return sales

sales_silver = clean_data(sales)
display(sales_silver)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Load the data into a Delta table
table_name = "sales"  # Replace with your desired table name
sales_silver.write.format("delta").mode("overwrite").saveAsTable(table_name)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
