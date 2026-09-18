# Azure Spend Analytics - Bronze Layer
# Purpose: Ingest raw spend data from ADLS Gen2 into a Delta Bronze table

from pyspark.sql import functions as F

# ---------------------------------------------------------
# 1. Configuration
# ---------------------------------------------------------

source_path = "abfss://landing@<storage-account>.dfs.core.windows.net/spend/"

bronze_path = "abfss://bronze@<storage-account>.dfs.core.windows.net/spend/"

# ---------------------------------------------------------
# 2. Read raw CSV data from ADLS Gen2
# ---------------------------------------------------------

df_raw = (
    spark.read
         .format("csv")
         .option("header", "true")
         .option("inferSchema", "true")
         .load(source_path)
)

# ---------------------------------------------------------
# 3. Add ingestion metadata
# ---------------------------------------------------------

df_bronze = (
    df_raw
    .withColumn("ingestion_timestamp", F.current_timestamp())
    .withColumn("source_file", F.input_file_name())
)

# ---------------------------------------------------------
# 4. Write data to Bronze layer in Delta format
# ---------------------------------------------------------

(
    df_bronze.write
             .format("delta")
             .mode("append")
             .save(bronze_path)
)

print("Bronze ingestion completed successfully.")
