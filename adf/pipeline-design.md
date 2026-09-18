# Azure Data Factory Pipeline Design

## Overview

Azure Data Factory (ADF) is used as the ingestion and orchestration layer of the Spend Analytics pipeline.

The pipeline ingests CSV files from the source system and loads the raw data into Azure Data Lake Storage Gen2 (ADLS Gen2).

## Data Flow

CSV Source → Azure Data Factory → ADLS Gen2 → Databricks

## ADF Components

### Linked Services
Linked Services are used to establish connections with:

- Source file storage
- Azure Data Lake Storage Gen2
- Azure Databricks

### Datasets

Parameterized datasets are used to dynamically process multiple CSV files.

Parameters can include:

- Source folder
- File name
- Target folder

### Pipeline Activities

The pipeline can contain:

1. Get Metadata
2. Lookup
3. ForEach
4. Copy Data
5. Execute Pipeline

## Metadata-Driven Ingestion

A control table stores information about the source datasets.

Example:

| Source | Table/File | Load Type | Watermark Column |
|---|---|---|---|
| CSV | vendor.csv | Full | N/A |
| CSV | transactions.csv | Incremental | modified_date |
| CSV | invoice.csv | Incremental | modified_date |

ADF reads this configuration and dynamically executes ingestion pipelines.

## Incremental Loading

For incremental datasets, a watermark is maintained.

Only records newer than the previous successful watermark are processed.

After successful execution, the watermark is updated for the next pipeline run.

## Error Handling

The pipeline design includes:

- Retry configuration
- Failure dependencies
- Logging
- Pipeline status tracking
- Failed-file handling

## Output

Raw source data is stored in ADLS Gen2 and is subsequently processed by Azure Databricks.
