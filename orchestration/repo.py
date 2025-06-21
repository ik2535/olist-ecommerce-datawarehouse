from dagster import Definitions
from jobs import erp_pipeline, crm_pipeline, catalog_pipeline, review_pipeline, streaming_pipeline, olist_pipeline, master_pipeline
from schedules import analytics_schedule, incremental_analytics

defs = Definitions(
    jobs=[erp_pipeline, crm_pipeline, catalog_pipeline, review_pipeline, streaming_pipeline, olist_pipeline, master_pipeline, incremental_analytics],
    schedules=[analytics_schedule]
)
