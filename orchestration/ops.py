# orchestration/ops.py
from dagster import op
import subprocess

@op
def run_ingestion():
    subprocess.run(["python", "erp_loader.py"], check=True, cwd="/app")

@op
def run_dbt():
    subprocess.run(["dbt", "run"], check=True, cwd="/usr/app")
