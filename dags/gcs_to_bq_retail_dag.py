from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.google.cloud.transfers.gcs_to_bigquery import GCSToBigQueryOperator
from airflow.utils.dates import days_ago
import pandas as pd
import os
from google.cloud import storage

# --- CONFIG ---
BUCKET_NAME = "retail-sales-bucket"
SOURCE_PREFIX = "daily_sales/"
GCP_CREDENTIALS_PATH = "/opt/airflow/gcp_creds.json"
BQ_DATASET = "retail_analytics"
BQ_TABLE = "daily_sales"

default_args = {
    "owner": "ajinkya",
    "start_date": days_ago(1),
}

def clean_csv(**context):
    execution_date = context['ds']  
    filename = f"{execution_date}.csv"
    blob_path = f"{SOURCE_PREFIX}{filename}"
    temp_path = f"/tmp/{filename}"

    client = storage.Client.from_service_account_json(GCP_CREDENTIALS_PATH)
    bucket = client.bucket(BUCKET_NAME)
    blob = bucket.blob(blob_path)

    if not blob.exists():
        print(f"⚠️ File {blob_path} not found in bucket. Skipping this run.")
        return

    blob.download_to_filename(temp_path)
    df = pd.read_csv(temp_path)
    df.dropna(inplace=True)
    df.columns = [col.strip().replace(" ", "_").lower() for col in df.columns]
    df.to_csv(temp_path, index=False)
    blob.upload_from_filename(temp_path)
    print("✅ clean_csv completed.")

with DAG(
    dag_id="gcs_to_bigquery_retail_sales",
    default_args=default_args,
    schedule_interval="@daily",
    catchup=False,
    tags=["retail"],
    params={"execution_date": "2017-12-31"}
) as dag:

    clean = PythonOperator(
        task_id="clean_sales_csv",
        python_callable=clean_csv,
        provide_context=True,
    )

    load = GCSToBigQueryOperator(
        task_id="load_to_bigquery",
        bucket=BUCKET_NAME,
        source_objects=["daily_sales/{{ ds }}.csv"],
        destination_project_dataset_table=f"{BQ_DATASET}.{BQ_TABLE}",
        skip_leading_rows=1,
        write_disposition="WRITE_APPEND",
        source_format="CSV",
        autodetect=True,
    )

    clean >> load
