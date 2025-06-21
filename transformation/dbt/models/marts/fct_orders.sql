{{ config(
    materialized='incremental',
    unique_key='order_id',
    on_schema_change='sync_all_columns'
) }}

WITH orders AS (
    SELECT * FROM {{ ref('stg_orders') }}
    {% if is_incremental() %}
        WHERE order_id IN (
            SELECT DISTINCT order_id FROM {{ ref('stg_payments') }}
            WHERE payment_key NOT IN (
                SELECT payment_key FROM {{ this }} WHERE payment_key IS NOT NULL
            )
        )
    {% endif %}
),
payments AS (
    SELECT
        order_id,
        SUM(payment_value) AS total_payment_value
    FROM {{ ref('stg_payments') }}
    GROUP BY order_id
),
items AS (
    SELECT
        order_id,
        SUM(price) AS total_item_price,
        SUM(freight_value) AS total_freight
    FROM {{ ref('stg_order_items') }}
    GROUP BY order_id
),
reviews AS (
    SELECT
        order_id,
        AVG(review_score) AS avg_review_score
    FROM {{ ref('stg_reviews') }}
    GROUP BY order_id
)

SELECT
    o.order_id,
    o.customer_id,
    o.order_status,
    o.order_purchase_timestamp,
    o.order_delivered_customer_date,
    o.order_estimated_delivery_date,
    p.total_payment_value,
    i.total_item_price,
    i.total_freight,
    r.avg_review_score
FROM orders o
LEFT JOIN payments p ON o.order_id = p.order_id
LEFT JOIN items i ON o.order_id = i.order_id
LEFT JOIN reviews r ON o.order_id = r.order_id