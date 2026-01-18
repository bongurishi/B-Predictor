import psutil
import pandas as pd
import time
from datetime import datetime

print(" B-Predictor Agent Started (LIVE DEVICE DATA)")

while True:
    data = {
        "timestamp": datetime.now(),
        "cpu_usage": psutil.cpu_percent(interval=1),
        "memory_usage": psutil.virtual_memory().percent,
        "disk_io": psutil.disk_io_counters().read_bytes / 1e6,
        "network_latency": psutil.net_io_counters().bytes_sent / 1e6,
        "error_rate": 0
    }

    df = pd.DataFrame([data])
    df.to_csv("data/metrics.csv", mode="a", header=False, index=False)

    time.sleep(2)

