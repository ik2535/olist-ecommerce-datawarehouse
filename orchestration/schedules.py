# orchestration/schedules.py
from dagster import schedule, DefaultScheduleStatus, job
from assets.transformation_assets import run_dbt_models_scheduled

@job
def incremental_analytics():
    """Process accumulated streaming data with dbt incremental models"""
    run_dbt_models_scheduled()  # Standalone op with no dependencies

@schedule(
    job=incremental_analytics,
    cron_schedule="*/5 * * * *",  # Every 5 minutes
    default_status=DefaultScheduleStatus.RUNNING
)
def analytics_schedule():
    """Trigger dbt transformations every 5 minutes"""
    return {}
