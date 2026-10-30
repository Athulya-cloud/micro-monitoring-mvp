# Micro Monitoring MVP

A small end-to-end monitor for microservices. Services send health metrics to an API, they are stored in Postgres, and a dashboard shows them live.

![architecture](assets/architecture.png)

## What it does

- **Ingest:** a FastAPI endpoint (`POST /ingest`) accepts one metrics record per call
- **Store:** every record goes into a Postgres `monitor` table
- **See:** a Streamlit dashboard shows the table and a latency chart
- **Each record has:** microservice name, start/end time, response code, latency, memory, CPU, health

## Run it

You need Python 3.10+ and a Postgres database. The quickest way to get one:

```bash
docker run -d --name monitor-db -p 5432:5432 -e POSTGRES_PASSWORD=postgres postgres
```

Get the code and install the dependencies:

```bash
git clone https://github.com/Athulya-cloud/micro-monitoring-mvp.git
cd micro-monitoring-mvp
pip install -r backend/requirements.txt streamlit pandas
```

Start the API from the project root (it creates the table on startup):

```bash
uvicorn backend.app.main:app --port 8000
```

In a second terminal, load the sample data and start the dashboard:

```bash
python scripts/seed_from_csv.py
streamlit run dashboard/streamlit_app.py
```

Open http://localhost:8501 to see the dashboard.

By default everything connects to `postgresql://postgres:postgres@localhost:5432/postgres`. Set the `DATABASE_URL` environment variable to use a different database.

## Send your own data

```bash
curl -X POST http://localhost:8000/ingest \
  -H "Content-Type: application/json" \
  -d '{"microservice": "Email", "responsecode": 200, "latency": 23, "health": true}'
```

## Stop it

Press `Ctrl+C` in each terminal, then `docker rm -f monitor-db` to remove the database.

## Tech stack

Python, FastAPI, SQLAlchemy, PostgreSQL, Streamlit, Docker.
