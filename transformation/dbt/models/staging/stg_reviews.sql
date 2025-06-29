{{ config(materialized='view') }}

SELECT
    review_id,
    order_id,
    review_score,
    review_comment_title,
    review_comment_message,
    review_creation_date::timestamp AS review_creation_date,
    review_answer_timestamp::timestamp AS review_answer_timestamp
FROM raw_olist_order_reviews_dataset