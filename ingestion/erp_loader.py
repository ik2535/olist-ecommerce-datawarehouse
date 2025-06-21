import os
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError

# PostgreSQL connection config
DB_CONFIG = {
    "user": "olist",
    "password": "olist123",
    "host": "postgres",  # name of the docker service
    "port": 5432,
    "database": "olist_dw"
}

DATA_DIR = os.path.join(os.getcwd(), "data")
  # mounted from outside
TABLE_PREFIX = "raw_"

def load_csv_to_postgres(file_path, table_name, engine):
    try:
        print(f"📦 Loading {file_path} → {table_name}...")
        df = pd.read_csv(file_path)
        df.to_sql(table_name, engine, if_exists='replace', index=False)
        print(f"✅ Loaded {len(df)} rows into '{table_name}'")
    except Exception as e:
        print(f"❌ Failed to load {file_path}: {e}")

def main():
    print("🔌 Connecting to PostgreSQL...")
    try:
        engine = create_engine(
            f"postgresql://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}"
        )
        print("✅ Connection successful.")
    except SQLAlchemyError as e:
        print(f"❌ DB connection error: {e}")
        return

    # List CSV files in data/
    print(f"📁 Scanning {DATA_DIR}...")
    for file in os.listdir(DATA_DIR):
        if file.endswith(".csv"):
            file_path = os.path.join(DATA_DIR, file)
            table_name = TABLE_PREFIX + os.path.splitext(file)[0]
            load_csv_to_postgres(file_path, table_name, engine)

    print("🎉 Ingestion complete.")

if __name__ == "__main__":
    main()
