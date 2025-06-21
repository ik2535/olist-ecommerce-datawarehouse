from dagster import op
import os
import pandas as pd
import psycopg2
import requests
import json
from kafka import KafkaConsumer
from sqlalchemy import create_engine, text

@op
def ingest_csvs():
    print("📁 Scanning for CSVs...")
    data_dir = "/app/ingestion/data"
    conn_str = "postgresql+psycopg2://olist:olist123@postgres:5432/olist_dw"
    engine = create_engine(conn_str)

    for filename in os.listdir(data_dir):
        if filename.endswith(".csv"):
            table_name = f"raw_{filename.replace('.csv', '')}"
            df = pd.read_csv(os.path.join(data_dir, filename))

            # Truncate existing table if it exists
            with engine.begin() as conn:
                conn.execute(text(f"TRUNCATE TABLE {table_name} RESTART IDENTITY CASCADE"))

            df.to_sql(table_name, engine, if_exists="append", index=False)
            print(f"✅ Loaded {len(df)} rows into '{table_name}'")

    return "ingestion_complete"

@op
def ingest_customers_from_crm():
    csv_path = "/app/ingestion/data/crm/olist_customers_dataset.csv"  # ✅ Define before using
    engine = create_engine("postgresql+psycopg2://olist:olist123@postgres:5432/olist_dw")
    df = pd.read_csv(csv_path)
    with engine.begin() as conn:
        conn.execute(text("TRUNCATE TABLE raw_olist_customers_dataset RESTART IDENTITY CASCADE"))  # Recommended
    df.to_sql("raw_olist_customers_dataset", engine, if_exists="append", index=False)
    print(f"✅ CRM: Loaded {len(df)} rows into 'raw_olist_customers_dataset'")
    return "crm_ingestion_done"

@op
def ingest_products_from_catalog():
    csv_path = "/app/ingestion/data/catalog_db/olist_products_dataset.csv"
    engine = create_engine("postgresql+psycopg2://olist:olist123@postgres:5432/olist_dw")

    with engine.begin() as conn:
        conn.execute(text("DROP VIEW IF EXISTS stg_products CASCADE"))  # ✅ Wrap in text()

    df = pd.read_csv(csv_path)
    df.to_sql("raw_olist_products_dataset", engine, if_exists="replace", index=False)
    print(f"✅ Catalog DB: Loaded {len(df)} rows into 'raw_olist_products_dataset'")
    return "products_loaded"

@op
def ingest_sellers_from_catalog():
    csv_path = "/app/ingestion/data/catalog_db/olist_sellers_dataset.csv"
    engine = create_engine("postgresql+psycopg2://olist:olist123@postgres:5432/olist_dw")
    df = pd.read_csv(csv_path)
    df.to_sql("raw_olist_sellers_dataset", engine, if_exists="replace", index=False)
    print(f"✅ Catalog DB: Loaded {len(df)} rows into 'raw_olist_sellers_dataset'")
    return "sellers_loaded"

@op
def ingest_reviews_from_api():
    url = "http://review_api:5001/api/reviews"
    response = requests.get(url)
    data = response.json()
    df = pd.DataFrame(data)

    engine = create_engine("postgresql+psycopg2://olist:olist123@postgres:5432/olist_dw")

    # Truncate instead of drop
    with engine.begin() as conn:
        conn.execute(text("TRUNCATE TABLE raw_olist_order_reviews_dataset"))

    df.to_sql("raw_olist_order_reviews_dataset", engine, if_exists="append", index=False)

    print(f"✅ Ingested {len(df)} rows into raw_olist_order_reviews_dataset")
    
    return "reviews_loaded"  # Added missing return statement

@op
def consume_order_payments():
    engine = create_engine("postgresql+psycopg2://olist:olist123@postgres:5432/olist_dw")
    consumer = KafkaConsumer(
        'order_payments',
        bootstrap_servers='kafka:9092',
        auto_offset_reset='earliest',
        group_id='olist-payments',
        value_deserializer=lambda m: json.loads(m.decode('utf-8'))
    )
    
    for message in consumer:
        data = message.value
        pd.DataFrame([data]).to_sql("raw_order_payments", engine, if_exists="append", index=False)
        print(f"💾 Ingested: {data}")
