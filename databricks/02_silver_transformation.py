# Azure Spend Analytics - Silver Layer
# Purpose: Clean, validate and transform Bronze spend data

from pyspark.sql import functions as F
from pyspark.sql.types import DecimalType, DateType

# ---------------------------------------------------------
# 1. Configuration
# ---------------------------------------------------------

bronze_path = "abfss://bronze@<storage-account>.dfs.core.windows.net/spend/"
silver_path = "abfss://silver@<storage-account>.dfs.core.windows.net/spend/"

# ---------------------------------------------------------
# 2. Read Bronze Delta data
# ---------------------------------------------------------

df_bronze = (
    spark.read
         .format("delta")
         .load(bronze_path)
)

# ---------------------------------------------------------
# 3. Remove duplicate transactions
# ---------------------------------------------------------

df_clean = df_bronze.dropDuplicates(["transaction_id"])

# ---------------------------------------------------------
# 4. Handle NULL values
# ---------------------------------------------------------

df_clean = (
    df_clean
    .fillna({
        "vendor_name": "Unknown",
        "category": "Uncategorized"
    })
)

# Remove records where critical fields are missing
df_clean = df_clean.filter(
    F.col("transaction_id").isNotNull()
)

# ---------------------------------------------------------
# 5. Standardize text columns
# ---------------------------------------------------------

df_clean = (
    df_clean
    .withColumn("vendor_name", F.trim(F.col("vendor_name")))
    .withColumn("category", F.upper(F.trim(F.col("category"))))
)

# ---------------------------------------------------------
# 6. Data type conversion
# ---------------------------------------------------------

df_clean = (
    df_clean
    .withColumn(
        "amount",
        F.col("amount").cast(DecimalType(18, 2))
    )
    .withColumn(
        "transaction_date",
        F.to_date(F.col("transaction_date"), "yyyy-MM-dd")
    )
)

# ---------------------------------------------------------
# 7. Apply data-quality rules
# ---------------------------------------------------------

df_clean = df_clean.filter(
    (F.col("amount").isNotNull()) &
    (F.col("amount") >= 0) &
    (F.col("transaction_date").isNotNull())
)

# ---------------------------------------------------------
# 8. Add Silver processing metadata
# ---------------------------------------------------------

df_silver = df_clean.withColumn(
    "silver_processed_timestamp",
    F.current_timestamp()
)

# ---------------------------------------------------------
# 9. Write Silver data in Delta format
# ---------------------------------------------------------

(
    df_silver.write
             .format("delta")
             .mode("overwrite")
             .option("overwriteSchema", "true")
             .save(silver_path)
)

print("Silver transformation completed successfully.")
