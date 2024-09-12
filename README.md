## Document

### Prerequisite
- Python 3.10+
- Google Cloud project, billing enabled
- Google Cloud SDK(gcloud, bq command)
- BigQuery

### Preparation
on your local environment
Run as below, to get authorization.
```
gcloud auth application-default login
gcloud auth login
```
Install required modules.
```
pip install -r requirements.txt
```
Set environment values.
```
export PROJECT_ID=<your project id>
export BQ_DATASET_ID=<your BigQuery dataset>
export BQ_TABLE_NAME=<your BigQuery table>
```
Load the sample csv to BigQuery
```
bq mk ${BQ_DATASET_ID}
bq load ${BQ_DATASET_ID}.${BQ_TABLE_NAME} ./sample/data.csv store_name:STRING,product_code:STRING,product_name:STRING,quantity:INTEGER,last_update:TIMESTAMP
```

### A. API mode
1. Run as api server
```
python api.py
```
You can test the api on "http://localhost:8080/docs".

### B. Chat mode
2. Run as Chainlit UI mode
```
chainlit run main.py
```
Once you run the cli, then the Chainlit UI will open on your browser.  
You can try to ask on the UI.
