# Retail Sales Analytics Pipeline

A complete end-to-end data pipeline project using Apache Airflow, Google Cloud Storage (GCS), BigQuery, and Power BI to ingest, clean, store, and visualize retail sales data.

## 🚀 Project Overview

* This pipeline simulates daily retail sales ingestion:

* Daily CSV files are uploaded to GCS

* Airflow DAGs clean and load the data into BigQuery

* Power BI connects to BigQuery for interactive dashboards

## 📁 Project Structure

### Retail Sales Analytics Project Structure

```plaintext
├── dags/                          # Airflow DAGs for data pipeline (GCS to BigQuery)
│   ├── gcs_to_bigquery_retail_sales.py
│   └── bulk_load_historical_sales.py
├── dashboards/                    # Power BI dashboard files
│   └── Retail_Sales_Insights.pbix
├── docker-compose.yaml            # Docker setup for Airflow services
├── Requirement.txt                # Python package dependencies for Airflow
├── README.md                      # Project documentation
└── .env.example                   # Example environment config (GCP creds, etc.)
```



## 🧰 Prerequisites

* Docker + Docker Compose

* GCP project with:

  * A bucket in GCS

  * BigQuery dataset & table created

* Service account with access to GCS & BigQuery

## 🔐 Setup Instructions

**1. Clone the repository**
```plaintext
git clone https://github.com/<your-username>/retail-sales-pipeline.git
cd retail-sales-pipeline
```

**2. Create your .env file**
```plaintext
cp .env.example .env
```

**3. Edit .env and set values like:**
```plaintext
AIRFLOW_UID=50000
GCP_PROJECT=your-project-id
```

**4. Place your GCP service account key**

  * Save your credentials file as: gcp_creds.json
  
  * Place it in the root directory (DO NOT commit it)

**5. Start Airflow**
```plaintext
docker-compose up --build -d
```
**6. Access the UI:** 
 * http://localhost:8080
 * Login: airflow / airflow

**7. Upload CSV files to GCS**

  * Format: daily_sales/YYYY-MM-DD.csv
  
  * Example: daily_sales/2017-12-31.csv

**8 Trigger DAGs**

  * Manual: Use Airflow UI or CLI:
 ```plaintext 
docker exec -it airflow-docker-airflow-scheduler-1 \
   airflow dags backfill gcs_to_bigquery_retail_sales -s 2017-12-31 -e 2017-12-31
```
## 📊 Power BI Dashboard

* Open dashboard/retail_sales_dashboard.pbix

* Connect to your BigQuery table: retail_analytics.daily_sales

* Visuals included:

  * Total Revenue
  
  * Orders by Region
  
  * Top-Selling Products
  
  * Daily Trends

## ✅ Features

  * Handles daily or bulk file uploads
  
  * Cleans and standardizes CSV columns
  
  * Safe to run even when daily files are missing
  
  * Backfill-ready for testing

## 🙋‍♂️ Author

Ajinkya Chintawar <br><br> [MSc Data Analytics | Data Engineer | ML Intern] <br><br>
[LinkedIn Profile](https://www.linkedin.com/in/ajinkya-chintawar/)



// Improved readability of README on 16 Feb 2025, 14:14

// Improved readability of README on 17 Feb 2025, 16:34

// Updated styling and layout on 02 Mar 2025, 09:14

// Updated styling and layout on 05 Mar 2025, 12:49
