import psutil
import time
from datetime import datetime

def collect_metrics():
    return {
        "timestamp": datetime.now(),
        "cpu_usage": psutil.cpu_percent(interval=1),
        "memory_usage": psutil.virtual_memory().percent,
        "disk_io": psutil.disk_io_counters().read_bytes / 1e6,
        "network_latency": psutil.net_io_counters().bytes_sent / 1e6,
        "error_rate": 0.0
    }

def stream_metrics():
    history = []
    while True:
        data = collect_metrics()
        history.append(data)

        # Sliding window
        if len(history) > 200:
            history.pop(0)

        yield history
        time.sleep(2)

