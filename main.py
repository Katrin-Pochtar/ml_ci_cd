from fastapi import FastAPI
from prometheus_client import Counter, Histogram, start_http_server
import time, os, random

app = FastAPI(title="ML Monitoring Demo")

REQUEST_COUNT = Counter("predict_requests_total", "Total number of prediction requests")
LATENCY = Histogram("prediction_latency_seconds", "Model prediction latency (s)")
ERROR_COUNT = Counter("predict_errors_total", "Total number of prediction errors")
VERSION = os.getenv("MODEL_VERSION", "v1.0.0")

@app.get("/health")
def health():
    return {"status": "ok", "version": VERSION}

@app.get("/predict")
def predict():
    start = time.time()
    REQUEST_COUNT.inc()
    try:
        if random.random() < 0.1:
            raise ValueError("Random failure!")
        time.sleep(random.uniform(0.05, 0.3))
        LATENCY.observe(time.time() - start)
        return {"prediction": "class_A", "version": VERSION}
    except Exception as e:
        ERROR_COUNT.inc()
        LATENCY.observe(time.time() - start)
        return {"error": str(e), "version": VERSION}

start_http_server(8001)