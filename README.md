# azure-data-engineering-spend-analytics
End-to-end Azure Data Engineering project using ADF, ADLS Gen2, Databricks, PySpark, Delta Lake and Medallion Architecture.
# Azure Spend Analytics Data Engineering Pipeline

## 📌 Project Overview

This project demonstrates an end-to-end Azure Data Engineering pipeline for processing and transforming spend data.

The solution uses Azure Data Factory (ADF) for data ingestion, Azure Data Lake Storage Gen2 (ADLS Gen2) for storage, and Azure Databricks with PySpark and Delta Lake for data processing.

The project follows the Medallion Architecture (Bronze, Silver, and Gold layers) to create clean and analytics-ready spend data.

---

## 🏗️ Architecture

CSV Source  
↓  
Azure Data Factory (ADF)  
↓  
Azure Data Lake Storage Gen2  
↓  
Azure Databricks  
↓  
Bronze Layer  
↓  
Silver Layer  
↓  
Gold Layer  
↓  
Spend Analytics / Reporting

---

## 🛠️ Technologies Used

- Azure Data Factory (ADF)
- Azure Data Lake Storage Gen2 (ADLS Gen2)
- Azure Databricks
- PySpark
- Delta Lake
- SQL
- Databricks Workflows
- Medallion Architecture

---

## 🔄 Pipeline Workflow

### 1. Data Ingestion

Spend data is received through CSV files.

Azure Data Factory is responsible for ingesting the source files and loading them into ADLS Gen2.

The ingestion framework can support:

- Parameterized pipelines
- Metadata-driven ingestion
- Incremental data loading
- Watermark-based processing
- Error handling and retry mechanisms

### 2. Bronze Layer

Raw data from ADLS Gen2 is ingested into the Bronze layer using Azure Databricks.

The Bronze layer maintains the source data with minimal transformations.

### 3. Silver Layer

PySpark is used to clean and transform the Bronze data.

Typical transformations include:

- NULL handling
- Duplicate removal
- Data type conversion
- Data validation
- Standardization
- Business-rule implementation

### 4. Gold Layer

The transformed Silver data is aggregated into business-ready datasets.

The Gold layer provides curated data for spend analysis and downstream reporting.

---

## ⚡ Incremental Processing

The pipeline supports incremental data processing to avoid reprocessing the complete dataset.

Delta Lake `MERGE` operations can be used to implement idempotent upsert logic.

This allows the pipeline to safely handle both new and updated records.

---

## 🛡️ Data Quality & Reliability

The solution includes concepts such as:

- Data validation
- Duplicate detection
- Pipeline retries
- Failure handling
- Logging
- Checkpointing
- Idempotent processing

---

## 📊 Output

The final Gold layer contains curated datasets that can be consumed by reporting and analytics applications for spend analysis.
├── sql/
└── docs/
