
# Architecture

This folder contains the architecture diagrams for the Azure Spend Analytics Data Engineering project.

![Azure Spend Analytics Architecture](architecture/azure-spend-analytics-architecture.png)

## Data Flow

CSV Source → Azure Data Factory → ADLS Gen2 → Azure Databricks → Bronze → Silver → Gold → Spend Report

## 📂 Project Structure

| Folder | Description |
|---|---|
| `adf/` | Azure Data Factory ingestion, orchestration and pipeline design |
| `architecture/` | End-to-end Azure data architecture diagram |
| `databricks/` | PySpark code for Bronze, Silver, Gold and Delta MERGE processing |
| `sql/` | Control table and watermark-based incremental loading logic |
| `sample-data/` | Sample CSV transaction data used by the pipeline |

---

## 🔄 End-to-End Data Flow

1. Spend transaction data arrives as CSV files.
2. Azure Data Factory orchestrates ingestion into ADLS Gen2.
3. Raw data is processed by Azure Databricks into the Bronze layer.
4. PySpark cleans, validates and standardizes the data for the Silver layer.
5. Delta Lake `MERGE` supports insert/update processing.
6. Gold-layer transformations aggregate spend by vendor and category.
7. Curated Gold data is made available for analytics and reporting.

---

## 🥉 Bronze Layer

The Bronze layer stores raw source data with minimal transformations.

Additional metadata is captured including:

- Ingestion timestamp
- Source filename

Implementation:

`databricks/01_bronze_ingestion.py`

---

## 🥈 Silver Layer

The Silver layer performs data cleansing and standardization using PySpark.

Transformations include:

- Duplicate removal
- NULL handling
- Data-type conversion
- Vendor-name standardization
- Category standardization
- Invalid-record filtering
- Data-quality validation

Implementation:

`databricks/02_silver_transformation.py`

---

## 🥇 Gold Layer

The Gold layer creates business-ready spend analytics.

Metrics include:

- Total spend
- Transaction count
- Average transaction amount
- Highest transaction
- Lowest transaction

The data is aggregated by vendor and spend category.

Implementation:

`databricks/03_gold_spend_report.py`

---

## ⚡ Incremental Processing

The solution demonstrates incremental processing using metadata/watermark concepts and Delta Lake MERGE.

For changed records:

- Existing `transaction_id` → UPDATE
- New `transaction_id` → INSERT

This helps make pipeline reruns idempotent and reduces unnecessary target processing.

Implementation:

`databricks/04_delta_merge_incremental.py`

---

## 🧰 Technology Stack

- Azure Data Factory
- Azure Data Lake Storage Gen2
- Azure Databricks
- PySpark
- Delta Lake
- SQL
- Databricks Workflows
- Medallion Architecture

---

## 🔐 Security

No credentials, access keys, SAS tokens, client secrets or production data are stored in this repository.

Storage-account names and connection details are represented using placeholders.

---

## 🎯 Skills Demonstrated

This project demonstrates:

- End-to-end ETL/ELT pipeline design
- ADF orchestration
- ADLS Gen2 integration
- PySpark data transformations
- Medallion Architecture
- Delta Lake
- Delta MERGE / Upsert
- Data-quality handling
- Metadata-driven ingestion concepts
- Incremental processing
- SQL
- Spend analytics
               
