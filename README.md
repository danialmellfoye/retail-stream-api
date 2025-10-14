# Retail Streaming API

A FastAPI app that streams mock retail transaction events in real time.
Ideal for testing streaming ingestion in Databricks or Spark Structured Streaming.

## Run locally
```bash
pip install -r requirements.txt
python -m uvicorn stream_api:app --reload --port 8000