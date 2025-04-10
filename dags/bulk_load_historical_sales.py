from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.google.cloud.transfers.gcs_to_bigquery import GCSToBigQueryOperator
from airflow.utils.dates import days_ago
from google.cloud import storage

import os

# CONFIG
BUCKET_NAME = "retail-sales-bucket"
SOURCE_PREFIX = "daily_sales/"
BQ_DATASET = "retail_analytics"
BQ_TABLE = "daily_sales"
EXCLUDE_FILE = "daily_sales/2014-01-03.csv"  # Already processed

default_args = {
    'owner': 'ajinkya',
}

schema_fields = [
    {"name": "row_id", "type": "INTEGER", "mode": "NULLABLE"},
    {"name": "order_id", "type": "STRING", "mode": "NULLABLE"},
    {"name": "order_date", "type": "DATE", "mode": "NULLABLE"},
    {"name": "ship_date", "type": "DATE", "mode": "NULLABLE"},
    {"name": "ship_mode", "type": "STRING", "mode": "NULLABLE"},
    {"name": "customer_id", "type": "STRING", "mode": "NULLABLE"},
    {"name": "customer_name", "type": "STRING", "mode": "NULLABLE"},
    {"name": "segment", "type": "STRING", "mode": "NULLABLE"},
    {"name": "country", "type": "STRING", "mode": "NULLABLE"},
    {"name": "city", "type": "STRING", "mode": "NULLABLE"},
    {"name": "state", "type": "STRING", "mode": "NULLABLE"},
    {"name": "postal_code", "type": "INTEGER", "mode": "NULLABLE"},
    {"name": "region", "type": "STRING", "mode": "NULLABLE"},
    {"name": "product_id", "type": "STRING", "mode": "NULLABLE"},
    {"name": "category", "type": "STRING", "mode": "NULLABLE"},
    {"name": "sub-category", "type": "STRING", "mode": "NULLABLE"},
    {"name": "product_name", "type": "STRING", "mode": "NULLABLE"},
    {"name": "sales", "type": "FLOAT", "mode": "NULLABLE"},
    {"name": "quantity", "type": "INTEGER", "mode": "NULLABLE"},
    {"name": "discount", "type": "FLOAT", "mode": "NULLABLE"},
    {"name": "profit", "type": "FLOAT", "mode": "NULLABLE"},
]

def get_csv_file_list():
    client = storage.Client()
    bucket = client.bucket(BUCKET_NAME)
    blobs = bucket.list_blobs(prefix=SOURCE_PREFIX)

    csv_files = []
    for blob in blobs:
        if blob.name.endswith(".csv") and blob.name != EXCLUDE_FILE:
            csv_files.append(blob.name)

    return csv_files

def generate_tasks(**context):
    csv_files = get_csv_file_list()

    for file_name in csv_files:
        GCSToBigQueryOperator(
            task_id=f"load_{file_name.replace('/', '_').replace('.csv', '')}",
            bucket=BUCKET_NAME,
            source_objects=[file_name],
            destination_project_dataset_table=f"{BQ_DATASET}.{BQ_TABLE}",
            skip_leading_rows=1,
            source_format="CSV",
            write_disposition="WRITE_APPEND",
            schema_fields=schema_fields,
            autodetect=False,
            gcp_conn_id="google_cloud_default",
            dag=context['dag'],
        ).execute(context=context)

with DAG(
    dag_id="bulk_load_historical_sales",
    default_args=default_args,
    start_date=days_ago(1),
    schedule_interval=None,
    catchup=False,
    tags=["retail", "bulk", "bigquery"],
) as dag:

    run_bulk_upload = PythonOperator(
        task_id="load_all_csvs_to_bigquery",
        python_callable=generate_tasks,
        provide_context=True,
    )
