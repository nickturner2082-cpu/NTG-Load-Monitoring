# NTG Load Monitoring (MVP)

A minimal load monitoring app with:
- FastAPI backend API + static file serving
- SQLite data storage
- Background worker that records CPU/memory/disk usage
- Responsive browser dashboard

## Project structure

- `app/main.py` – FastAPI application
- `app/database.py` – SQLite schema and query helpers
- `worker.py` – continuous monitoring loop
- `static/` – HTML/CSS/JS frontend
- `monitoring.db` – SQLite DB file (created at runtime)

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Configuration

Optional environment variables:

- `NTG_DB_PATH` (default: `monitoring.db`) – path to SQLite file
- `NTG_POLL_INTERVAL_SECONDS` (default: `5`) – worker collection interval (must be greater than `0`)

## Run

### 1) Start worker

```bash
python worker.py
```

This collects system metrics every 5 seconds (or custom interval via env var).

### 2) Start API/web server (new terminal)

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

Open `http://localhost:8000`.

## API endpoints

- `GET /api/health`
- `GET /api/metrics/latest`
- `GET /api/metrics/history?limit=50`


## Validation checks

```bash
python -m compileall app worker.py
curl -s http://127.0.0.1:8000/api/health
```
