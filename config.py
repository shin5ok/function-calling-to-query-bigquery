import os
  
VERTEX_AI_LOCATION = "global"
PROJECT_ID = os.environ.get("PROJECT_ID")
DATASTORE_ID = os.environ.get("DATASTORE_ID")

BUCKET_NAME = os.environ.get("BUCKET_NAME", PROJECT_ID)
LOCATION = os.environ.get("LOCATION", "europe-west1")

BQ_DATASET_ID = os.environ.get("BQ_DATASET_ID")
BQ_TABLE_NAME = os.environ.get("BQ_TABLE_NAME")


MODEL_VERSION = "gemini-1.5-flash-001/answer_gen/v1"
