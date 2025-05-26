import os
import json

# Input event for the create_knowledge_base feature
CREATE_KNOWLEDGE_BASE_INPUT_EVENT = {
    "body": json.dumps(
        {
            "kb_input_refence": [
                {
                    "database_name": "db_olist_ecommerce",
                    "table_name": "tbl_olist_customers"
                },
                {
                    "database_name": "db_olist_ecommerce",
                    "table_name": "tbl_olist_geolocation"
                },
                {
                    "database_name": "db_olist_ecommerce",
                    "table_name": "tbl_olist_order_items"
                },
                {
                    "database_name": "db_olist_ecommerce",
                    "table_name": "tbl_olist_order_payments"
                },
                {
                    "database_name": "db_olist_ecommerce",
                    "table_name": "tbl_olist_order_reviews"
                },
                {
                    "database_name": "db_olist_ecommerce",
                    "table_name": "tbl_olist_orders"
                },
                {
                    "database_name": "db_olist_ecommerce",
                    "table_name": "tbl_olist_products"
                },
                {
                    "database_name": "db_olist_ecommerce",
                    "table_name": "tbl_olist_sellers"
                }
            ],
            "account_credentials": {
                "access_key_id": os.getenv("AWS_ACCESS_KEY_ID"),
                "secret_access_key": os.getenv("AWS_SECRET_ACCESS_KEY"),
                "session_token": os.getenv("AWS_SESSION_TOKEN")
            }
        }
    )
}

# Input event for the process_user_prompt feature
PROCESS_USER_PROMPT_INPUT_EVENT = {
    "body": json.dumps(
        {
            "user_prompt": "Qual a média movel de preço dos produtos vendidos nos últimos 3 meses de 2017 para cada estado?",
            "kb_id": "95cf3ba0-fab4-4963-85bb-6edb99b9df31",
            "account_credentials": {
                "access_key_id": os.getenv("AWS_ACCESS_KEY_ID"),
                "secret_access_key": os.getenv("AWS_SECRET_ACCESS_KEY"),
                "session_token": os.getenv("AWS_SESSION_TOKEN")
            }
        }
    )
}
