from dagster import job
from assets.ingestion_assets import ingest_csvs, ingest_customers_from_crm, ingest_products_from_catalog, ingest_sellers_from_catalog, ingest_reviews_from_api, consume_order_payments
from assets.transformation_assets import run_dbt_models, run_dbt_models_single
from assets.erp_ingestion import ingest_erp_data

@job
def olist_pipeline():
    raw = ingest_csvs()
    run_dbt_models_single(start_after=raw)  # Use single dependency version

@job
def erp_pipeline():
    ingest_erp_data()

@job
def crm_pipeline():
    ingest_customers_from_crm()

@job
def catalog_pipeline():
    ingest_products_from_catalog()
    ingest_sellers_from_catalog()

@job
def review_pipeline():
    ingest_reviews_from_api()

@job
def streaming_pipeline():
    consume_order_payments()

@job
def master_pipeline():
    """Master pipeline that orchestrates all data ingestion and transformation"""
    erp = ingest_erp_data()
    crm = ingest_customers_from_crm()
    products = ingest_products_from_catalog()
    sellers = ingest_sellers_from_catalog()
    reviews = ingest_reviews_from_api()
    # Wait for all ingestion to complete, then run dbt transformations
    run_dbt_models(start_after=[erp, crm, products, sellers, reviews])  # Use multi-dependency version
