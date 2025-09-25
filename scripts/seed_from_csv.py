# scripts/seed_from_csv.py
import csv
import sqlalchemy
import os
from sqlalchemy import text

DB_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/postgres")
engine = sqlalchemy.create_engine(DB_URL, future=True)

with engine.begin() as conn:
    with open("data/seed.csv") as f:
        reader = csv.DictReader(f)
        for row in reader:
            conn.execute(
                text(
                    "INSERT INTO monitor("
                    "microservice,starttime,endtime,readable_starttime,readable_endtime,"
                    "responsecode,latency,memory_usage,cpu,health"
                    ") VALUES ("
                    ":microservice,:starttime,:endtime,:readable_starttime,:readable_endtime,"
                    ":responsecode,:latency,:memory_usage,:cpu,:health)"
                ),
                {
                    "microservice": row["microservice"],
                    "starttime": int(float(row["starttime"])),
                    "endtime": int(float(row["endtime"])),
                    "readable_starttime": row["readable_starttime"],
                    "readable_endtime": row["readable_endtime"],
                    "responsecode": int(row["responsecode"]),
                    "latency": float(row["latency"]),
                    "memory_usage": int(row["memory_usage"]),
                    "cpu": int(row["cpu"]),
                    "health": row["health"].strip().upper() in ("TRUE", "T", "1")
                }
            )

print("Seed complete")
