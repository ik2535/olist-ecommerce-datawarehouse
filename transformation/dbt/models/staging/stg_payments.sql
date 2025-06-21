{{ config(materialized='incremental', unique_key='payment_key') }}

WITH batch_payments AS (
    SELECT
        order_id || '_' || payment_sequential as payment_key,
        order_id,
        payment_sequential,
        payment_type,
        payment_installments,
        payment_value,
        'batch' as data_source
    FROM raw_olist_order_payments_dataset
),

streaming_payments AS (
    SELECT
        order_id || '_' || payment_sequential as payment_key,
        order_id,
        payment_sequential,
        payment_type,
        payment_installments,
        payment_value,
        'streaming' as data_source
    FROM raw_order_payments
)

SELECT * FROM batch_payments
UNION ALL
SELECT * FROM streaming_payments

{% if is_incremental() %}
    WHERE payment_key NOT IN (SELECT payment_key FROM {{ this }})
{% endif %}
