import requests
import pandas as pd
from datetime import datetime

PROM_URL = "http://localhost:9090/api/v1/query"

QUERIES = {
    "cpu_usage": "100 - (avg by(instance)(rate(node_cpu_seconds_total{mode='idle'}[1m])) * 100)",
    "memory_usage": "(node_memory_Active_bytes / node_memory_MemTotal_bytes) * 100",
    "disk_io": "rate(node_disk_io_time_seconds_total[1m])",
    "network_latency": "rate(node_network_receive_errs_total[1m])",
    "error_rate": "rate(node_network_transmit_errs_total[1m])"
}

def fetch_metric(query):
    r = requests.get(PROM_URL, params={"query": query})
    result = r.json()["data"]["result"]
    if not result:
        return 0.0
    return float(result[0]["value"][1])

def get_live_metrics():
    data = {
        "timestamp": datetime.utcnow(),
    }
    for k, q in QUERIES.items():
        data[k] = fetch_metric(q)

    return pd.DataFrame([data])
