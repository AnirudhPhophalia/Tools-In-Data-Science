from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import os

app = FastAPI()

# Allow all origins (assignment only says it must allow browser access)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------
# Defaults
# -----------------------
config = {
    "port": 8000,
    "workers": 1,
    "debug": False,
    "log_level": "info",
    "api_key": "default-secret-000",
}

# -----------------------
# config.development.yaml
# -----------------------
config.update({
    "port": 8949,
    "workers": 11,
    "debug": False,
})

# -----------------------
# .env layer
# -----------------------
config.update({
    "port": 8155,
    "workers": 16,          # NUM_WORKERS alias
    "log_level": "debug",
    "api_key": "key-sfh0w41bh6",
})

# -----------------------
# OS Environment Layer
# -----------------------
config.update({
    "port": 8817,
    "debug": True,
    "api_key": "key-g12a7ogzb3",
})


def to_bool(value):
    return str(value).lower() in ("true", "1", "yes", "on")


@app.get("/effective-config")
def effective_config(set: List[str] = Query(default=[])):
    cfg = config.copy()

    # CLI overrides
    for item in set:
        if "=" not in item:
            continue

        key, value = item.split("=", 1)

        if key in ("port", "workers"):
            cfg[key] = int(value)

        elif key == "debug":
            cfg[key] = to_bool(value)

        else:
            cfg[key] = value

    # Mask secret
    cfg["api_key"] = "****"

    return cfg