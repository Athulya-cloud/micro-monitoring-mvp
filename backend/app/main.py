from fastapi import FastAPI
from pydantic import BaseModel
import os
import sqlalchemy
from sqlalchemy import text

DB_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/postgres")
engine = sqlalchemy.create_engine(DB_URL, future=True)

app = FastAPI(title="Micro Monitor MVP")

class Record(BaseModel):
    microservice: str
    starttime: float | None = None
    endtime: float | None = None
    readable_starttime: str | None = None
    readable_endtime: str | None = None
    responsecode: int | None = None
    latency: float | None = None
    memory_usage: int | None = None
    cpu: int | None = None
    health: bool | None = None

@app.on_event("startup")
def startup():
    ddl = open("backend/app/models.sql").read()
    with engine.begin() as conn:
        conn.execute(text(ddl))

def to_int_epoch(val):
    if val is None:
        return None
    try:
        return int(float(val))
    except:
        return None

@app.post("/ingest")
def ingest(rec: Record):
    payload = rec.dict()
    # Convert scientific notation epochs to integers if present
    payload["starttime"] = to_int_epoch(payload.get("starttime"))
    payload["endtime"] = to_int_epoch(payload.get("endtime"))
    with engine.begin() as conn:
        conn.execute(
            text("""
            INSERT INTO monitor
            (microservice,starttime,endtime,readable_starttime,readable_endtime,responsecode,
             latency,memory_usage,cpu,health)
            VALUES (:microservice,:starttime,:endtime,:readable_starttime,:readable_endtime,
             :responsecode,:latency,:memory_usage,:cpu,:health)
            """),
            payload,
        )
    return {"status": "ok"}
