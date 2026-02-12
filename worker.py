"""Simple monitoring worker loop for NTG Load Monitoring."""

from __future__ import annotations

import os
import time
from datetime import datetime, timezone

import psutil

from app.database import init_db, insert_metric

def get_poll_interval_seconds() -> float:
    raw_value = os.getenv("NTG_POLL_INTERVAL_SECONDS", "5")
    interval = float(raw_value)
    if interval <= 0:
        raise ValueError("NTG_POLL_INTERVAL_SECONDS must be greater than 0")
    return interval


def collect_metrics() -> tuple[float, float, float]:
    cpu_percent = psutil.cpu_percent(interval=None)
    memory_percent = psutil.virtual_memory().percent
    disk_percent = psutil.disk_usage("/").percent
    return cpu_percent, memory_percent, disk_percent


def run_forever() -> None:
    poll_interval_seconds = get_poll_interval_seconds()
    init_db()
    psutil.cpu_percent(interval=None)
    print(f"Starting worker loop (interval={poll_interval_seconds}s)")

    try:
        while True:
            started_at = time.monotonic()
            recorded_at = datetime.now(timezone.utc).isoformat()
            cpu_percent, memory_percent, disk_percent = collect_metrics()

            insert_metric(
                recorded_at=recorded_at,
                cpu_percent=cpu_percent,
                memory_percent=memory_percent,
                disk_percent=disk_percent,
            )

            print(
                "Saved metric",
                {
                    "recorded_at": recorded_at,
                    "cpu_percent": cpu_percent,
                    "memory_percent": memory_percent,
                    "disk_percent": disk_percent,
                },
            )

            elapsed = time.monotonic() - started_at
            time.sleep(max(0.0, poll_interval_seconds - elapsed))
    except KeyboardInterrupt:
        print("Worker interrupted. Exiting cleanly.")


if __name__ == "__main__":
    run_forever()
