# Azure Spend Analytics - Gold Layer
# Purpose: Create business-ready spend analytics from Silver data

from pyspark.sql import functions as F

# ---------------------------------------------------------
# 1. Configuration
# ---------------------------------------------------------

silver_path = "abfss://silver@<storage-account>.dfs.core.windows.net/spend/"
gold_path = "abfss://gold@<storage-account>.dfs.core.windows.net/spend_report/"

# ---------------------------------------------------------
# 2. Read Silver Delta data
# ---------------------------------------------------------

df_silver = (
    spark.read
         .format("delta")
         .load(silver_path)
)

# ---------------------------------------------------------
# 3. Create Spend Report
# ---------------------------------------------------------

df_gold = (
    df_silver
    .groupBy(
        "vendor_name",
        "category"
    )
    .agg(
        F.sum("amount").alias("total_spend"),
        F.countDistinct("transaction_id").alias("transaction_count"),
        F.avg("amount").alias("average_transaction_amount"),
        F.max("amount").alias("highest_transaction"),
        F.min("amount").alias("lowest_transaction")
    )
)

# ---------------------------------------------------------
# 4. Round reporting metrics
# ---------------------------------------------------------

df_gold = (
    df_gold
    .withColumn(
        "total_spend",
        F.round(F.col("total_spend"), 2)
    )
    .withColumn(
        "average_transaction_amount",
        F.round(F.col("average_transaction_amount"), 2)
    )
)

# ---------------------------------------------------------
# 5. Add processing timestamp
# ---------------------------------------------------------

df_gold = df_gold.withColumn(
    "gold_processed_timestamp",
    F.current_timestamp()
)

# ---------------------------------------------------------
# 6. Write Gold data in Delta format
# ---------------------------------------------------------

(
    df_gold.write
           .format("delta")
           .mode("overwrite")
           .option("overwriteSchema", "true")
           .save(gold_path)
)

print("Gold Spend Report created successfully.")
