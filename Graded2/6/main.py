from fastapi import FastAPI, Request
from fastapi.responses import PlainTextResponse
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST
import time
import uuid

app = FastAPI()

EMAIL = "24f2003068@ds.study.iitm.ac.in"

# App start time
START_TIME = time.time()

# Prometheus Counter
REQUEST_COUNTER = Counter(
    "http_requests_total",
    "Total HTTP Requests"
)

# Store logs in memory
logs = []


@app.middleware("http")
async def middleware(request: Request, call_next):

    REQUEST_COUNTER.inc()

    request_id = str(uuid.uuid4())

    log = {
        "level": "INFO",
        "ts": time.time(),
        "path": request.url.path,
        "request_id": request_id
    }

    logs.append(log)

    # Keep only latest 1000 logs
    if len(logs) > 1000:
        logs.pop(0)

    response = await call_next(request)

    return response


@app.get("/work")
def work(n: int = 0):
    for _ in range(n):
        pass

    return {
        "email": EMAIL,
        "done": n
    }


@app.get("/metrics")
def metrics():
    return PlainTextResponse(
        generate_latest().decode(),
        media_type=CONTENT_TYPE_LATEST
    )


@app.get("/healthz")
def health():

    return {
        "status": "ok",
        "uptime_s": time.time() - START_TIME
    }


@app.get("/logs/tail")
def tail(limit: int = 10):

    return logs[-limit:]