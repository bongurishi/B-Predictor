import requests
import pandas as pd
from datetime import datetime

PROM_URL = "http://localhost:9090/api/v1/query_range"

def fetch_metric(metric, start, end, step="60s"):
    params = {
        "query": metric,
        "start": start,
        "end": end,
        "step": step
    }
    r = requests.get(PROM_URL, params=params).json()
    values = r["data"]["result"][0]["values"]

    return pd.DataFrame(values, columns=["timestamp", metric])

def fetch_all_metrics():
    end = datetime.utcnow().timestamp()
    start = end - 3600

    cpu = fetch_metric("node_cpu_seconds_total", start, end)
    mem = fetch_metric("node_memory_MemAvailable_bytes", start, end)

    df = cpu.merge(mem, on="timestamp")
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="s")

    df.to_csv("data/metrics.csv", index=False)
