# Azure Spend Analytics - Incremental Delta MERGE
# Purpose: Insert new transactions and update existing transactions
# using Delta Lake MERGE.

from delta.tables import DeltaTable
from pyspark.sql import functions as F

# ---------------------------------------------------------
# 1. Configuration
# ---------------------------------------------------------

bronze_path = (
    "abfss://bronze@<storage-account>.dfs.core.windows.net/spend/"
)

silver_path = (
    "abfss://silver@<storage-account>.dfs.core.windows.net/spend/"
)

# ---------------------------------------------------------
# 2. Read new / changed Bronze records
# ---------------------------------------------------------

df_incremental = (
    spark.read
         .format("delta")
         .load(bronze_path)
)

# ---------------------------------------------------------
# 3. Clean incoming records
# ---------------------------------------------------------

df_incremental = (
    df_incremental
    .dropDuplicates(["transaction_id"])
    .filter(F.col("transaction_id").isNotNull())
    .fillna({
        "vendor_name": "Unknown",
        "category": "Uncategorized"
    })
    .withColumn(
        "vendor_name",
        F.trim(F.col("vendor_name"))
    )
    .withColumn(
        "category",
        F.upper(F.trim(F.col("category")))
    )
    .withColumn(
        "amount",
        F.col("amount").cast("decimal(18,2)")
    )
    .withColumn(
        "transaction_date",
        F.to_date(F.col("transaction_date"), "yyyy-MM-dd")
    )
    .withColumn(
        "silver_processed_timestamp",
        F.current_timestamp()
    )
)

# ---------------------------------------------------------
# 4. Check whether Silver Delta table already exists
# ---------------------------------------------------------

if DeltaTable.isDeltaTable(spark, silver_path):

    silver_table = DeltaTable.forPath(
        spark,
        silver_path
    )

    # -----------------------------------------------------
    # 5. MERGE / UPSERT
    # -----------------------------------------------------

    (
        silver_table.alias("target")
        .merge(
            df_incremental.alias("source"),
            "target.transaction_id = source.transaction_id"
        )
        .whenMatchedUpdateAll()
        .whenNotMatchedInsertAll()
        .execute()
    )

    print("Incremental MERGE completed successfully.")

else:

    # -----------------------------------------------------
    # First load - create Silver Delta table
    # -----------------------------------------------------

    (
        df_incremental.write
                      .format("delta")
                      .mode("overwrite")
                      .save(silver_path)
    )

    print("Initial Silver Delta table created successfully.")
