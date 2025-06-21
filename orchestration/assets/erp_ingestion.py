# orchestration/assets/erp_ingestion.py
from dagster import op
import os
import pandas as pd
from sqlalchemy import create_engine

@op
def ingest_erp_data():
    erp_path = "/app/ingestion/data/erp"
    conn_str = "postgresql+psycopg2://olist:olist123@postgres:5432/olist_dw"
    engine = create_engine(conn_str)
    
    for file in os.listdir(erp_path):
        if file.endswith(".csv"):
            table_name = f"erp_{file.replace('.csv', '')}"
            df = pd.read_csv(os.path.join(erp_path, file))
            df.to_sql(table_name, engine, if_exists="replace", index=False)
            print(f"✅ ERP: Loaded {len(df)} rows into {table_name}")
    
    return "erp_ingestion_complete"
