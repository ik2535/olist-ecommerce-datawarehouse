from dagster import op, In
import subprocess
import os
from typing import List

@op(
    ins={"start_after": In(List[str], description="Wait for multiple upstream tasks")}
)
def run_dbt_models(start_after: List[str]):
    print(f"⚙️ Running dbt models after: {start_after}")
    
    # Step 1: Always install/update dependencies first
    print("📦 Installing dbt dependencies...")
    deps_result = subprocess.run(
        ["dbt", "deps"], 
        cwd="/usr/app/dbt", 
        capture_output=True, 
        text=True
    )
    
    if deps_result.returncode != 0:
        print("⚠️ dbt deps had warnings but continuing...")
        if deps_result.stderr:
            print("📥 DBT deps stderr:\n", deps_result.stderr)
    else:
        print("✅ dbt dependencies installed successfully")
    
    # Step 2: Run dbt transformations
    print("🔄 Running dbt transformations...")
    result = subprocess.run(["dbt", "run"], cwd="/usr/app/dbt", capture_output=True, text=True)

    print("📤 DBT stdout:\n", result.stdout)
    if result.stderr:
        print("📥 DBT stderr:\n", result.stderr)

    if result.returncode != 0:
        raise Exception("dbt run failed")
    else:
        print("✅ dbt run completed successfully")

@op
def run_dbt_models_single(start_after: str):
    """Single dependency version with auto-deps for backward compatibility"""
    print(f"⚙️ Running dbt models after: {start_after}")
    
    # Step 1: Install dependencies
    print("📦 Installing dbt dependencies...")
    deps_result = subprocess.run(
        ["dbt", "deps"], 
        cwd="/usr/app/dbt", 
        capture_output=True, 
        text=True
    )
    
    if deps_result.returncode != 0:
        print("⚠️ dbt deps had warnings but continuing...")
        if deps_result.stderr:
            print("📥 DBT deps stderr:\n", deps_result.stderr)
    else:
        print("✅ dbt dependencies installed successfully")
    
    # Step 2: Run models
    result = subprocess.run(["dbt", "run"], cwd="/usr/app/dbt", capture_output=True, text=True)

    print("📤 DBT stdout:\n", result.stdout)
    if result.stderr:
        print("📥 DBT stderr:\n", result.stderr)

    if result.returncode != 0:
        raise Exception("dbt run failed")
    else:
        print("✅ dbt run completed successfully")

@op
def run_dbt_models_scheduled():
    """Standalone dbt run for scheduled executions without dependencies"""
    print("⚙️ Running scheduled dbt transformations for incremental models")
    
    # Step 1: Install dependencies
    print("📦 Installing dbt dependencies...")
    deps_result = subprocess.run(
        ["dbt", "deps"], 
        cwd="/usr/app/dbt", 
        capture_output=True, 
        text=True
    )
    
    if deps_result.returncode != 0:
        print("⚠️ dbt deps had warnings but continuing...")
        if deps_result.stderr:
            print("📥 DBT deps stderr:\n", deps_result.stderr)
    else:
        print("✅ dbt dependencies installed successfully")
    
    # Step 2: Run dbt models (specifically for incremental processing)
    print("🔄 Running dbt incremental transformations...")
    result = subprocess.run(["dbt", "run"], cwd="/usr/app/dbt", capture_output=True, text=True)

    print("📤 DBT stdout:\n", result.stdout)
    if result.stderr:
        print("📥 DBT stderr:\n", result.stderr)

    if result.returncode != 0:
        raise Exception("dbt run failed")
    else:
        print("✅ dbt incremental run completed successfully")
        return "incremental_models_updated"
