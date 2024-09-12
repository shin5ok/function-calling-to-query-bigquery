
from pprint import pprint as pp
import os

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from google.cloud import bigquery
from google.auth import default


import config as c

# 環境変数から設定を取得
PROJECT_ID = os.environ.get("PROJECT_ID")
DATASET_ID = os.environ.get("BQ_DATASET_ID")
TABLE_NAME = os.environ.get("BQ_TABLE_NAME")

# 必要な環境変数が設定されているか確認
required_env_vars = {
    "GCP_PROJECT_ID": PROJECT_ID,
    "BQ_DATASET_ID": DATASET_ID,
    "BQ_TABLE_NAME": TABLE_NAME
}

default_model = "gemini-1.5-flash-001"

for var_name, var_value in required_env_vars.items():
    if not var_value:
        raise ValueError(f"{var_name} environment variable is not set")

# ADCを使用してクレデンシャルを取得
credentials, project = default()

# BigQuery クライアントの設定
client = bigquery.Client(credentials=credentials, project=PROJECT_ID)


class InventoryRequest(BaseModel):
    customer_name: str
    store_name: str
    product_name: str

def get_inventory(request: InventoryRequest):
    """
    Retrieve inventory information corresponding to the request
    """
    query = f"""
    SELECT 
        customer_name,
        store_name,
        product_code,
        product_name,
        quantity,
        last_update
    FROM 
        `{PROJECT_ID}.{DATASET_ID}.{TABLE_NAME}`
    WHERE 
        customer_name = @customer_name
        AND store_name = @store_name
        AND product_name = @product_name
    """
    print(query)

    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("customer_name", "STRING", request.customer_name),
            bigquery.ScalarQueryParameter("store_name", "STRING", request.store_name),
            bigquery.ScalarQueryParameter("product_name", "STRING", request.product_name),
        ]
    )

    try:
        query_job = client.query(query, job_config=job_config)
        pp(query_job)
        results = query_job.result()

        if results.total_rows == 0:
            raise HTTPException(status_code=404, detail="Inventory data not found")

        inventory_data = next(results)
        
        return {
            "customer_name": inventory_data.customer_name,
            "store_name": inventory_data.store_name,
            "product_code": inventory_data.product_code,
            "product_name": inventory_data.product_name,
            "quantity": inventory_data.quantity,
            "last_update": inventory_data.last_update.isoformat()
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

app = FastAPI()

@app.post("/inventory")
def _get_inventory(request: InventoryRequest):
    """
    Retrieve inventory information corresponding to the request
    """
    return get_inventory(request)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", "8080")))
