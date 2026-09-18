
# Architecture

This folder contains the architecture diagrams for the Azure Spend Analytics Data Engineering project.

## Data Flow

CSV Source → Azure Data Factory → ADLS Gen2 → Azure Databricks → Bronze → Silver → Gold → Spend Report

                 ┌─────────────┐
                 │ CSV Sources │
                 └──────┬──────┘
                        ↓
              ┌───────────────────┐
              │ Azure Data Factory│
              │  Ingestion / ETL  │
              └─────────┬─────────┘
                        ↓
                 ┌─────────────┐
                 │ ADLS Gen2   │
                 │ Landing Zone│
                 └──────┬──────┘
                        ↓
                Azure Databricks
                        │
             ┌──────────┼──────────┐
             ↓          ↓          ↓
          BRONZE      SILVER      GOLD
           Raw        Cleaned     Curated
             │          │          │
             └──────────┴──────────┘
                        ↓
                  Spend Report
