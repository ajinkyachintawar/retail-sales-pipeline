**Retail Sales Analytics Pipeline**

A complete end-to-end data pipeline project using Apache Airflow, Google Cloud Storage (GCS), BigQuery, and Power BI to ingest, clean, store, and visualize retail sales data.

🚀 Project Overview

This pipeline simulates daily retail sales ingestion:

Daily CSV files are uploaded to GCS

Airflow DAGs clean and load the data into BigQuery

Power BI connects to BigQuery for interactive dashboards

📁 Project Structure

retail-sales-pipeline/
├── dags/
│   ├── gcs_to_bigquery_retail_sales.py      # Daily DAG
│   └── bulk_load_historical_sales.py        # One-time historical loader
├── docker-compose.yaml                      # Airflow setup
├── .env.example                             # Env config sample
├── requirements.txt                         # Python dependencies
├── test_data/
│   └── sample_2017-12-31.csv                # Example CSV
├── dashboard/
│   └── retail_sales_dashboard.pbix          # Optional Power BI file
└── README.md                                # This file

🧰 Prerequisites

Docker + Docker Compose

GCP project with:

A bucket in GCS

BigQuery dataset & table created

Service account with access to GCS & BigQuery

🔐 Setup Instructions

Clone the repository

git clone https://github.com/<your-username>/retail-sales-pipeline.git
cd retail-sales-pipeline

Create your .env file

cp .env.example .env

Edit .env and set values like:

AIRFLOW_UID=50000
GCP_PROJECT=your-project-id

Place your GCP service account key

Save your credentials file as: gcp_creds.json

Place it in the root directory (DO NOT commit it)

Start Airflow

docker-compose up --build -d

Access the UI at: http://localhost:8080Login: airflow / airflow

Upload CSV files to GCS

Format: daily_sales/YYYY-MM-DD.csv

Example: daily_sales/2017-12-31.csv

Trigger DAGs

Manual: Use Airflow UI or CLI:

docker exec -it airflow-docker-airflow-scheduler-1 \
  airflow dags backfill gcs_to_bigquery_retail_sales -s 2017-12-31 -e 2017-12-31

📊 Power BI Dashboard

Open dashboard/retail_sales_dashboard.pbix

Connect to your BigQuery table: retail_analytics.daily_sales

Visuals included:

Total Revenue

Orders by Region

Top-Selling Products

Daily Trends

✅ Features

Handles daily or bulk file uploads

Cleans and standardizes CSV columns

Safe to run even when daily files are missing

Backfill-ready for testing

🙋‍♂️ Author

Ajinkya Chintawar[MSc Data Analytics | Data Engineer | ML Intern]

