<h1 align="center">Micro Monitoring MVP</h1>
<p align="center"><b>See how all your services are doing, in one place.</b></p>

<p align="center"><img src="assets/architecture.png" alt="How Micro Monitoring works" width="760"></p>

Microservices go down quietly. This small monitor collects health metrics from every service, stores them, and shows latency and status on a live dashboard, so you spot trouble before your users do.

Send a record with one request. See it on the dashboard seconds later.

## Why you'll like it

- **One call to report:** a single `POST /ingest` takes a metrics record from any service
- **Nothing gets lost:** every record is saved in Postgres
- **See it at a glance:** a Streamlit dashboard shows the full table and a latency chart
- **Tracks what matters:** response code, latency, memory, CPU and health for each service

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
