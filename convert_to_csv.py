import pandas as pd
import os

# Path to your data folder
data_dir = "data"

for file in os.listdir(data_dir):
    if file.endswith(".xlsx"):
        full_path = os.path.join(data_dir, file)
        df = pd.read_excel(full_path)
        csv_name = file.replace(".xlsx", ".csv")
        df.to_csv(os.path.join(data_dir, csv_name), index=False)
        print(f"✅ Converted: {file} → {csv_name}")