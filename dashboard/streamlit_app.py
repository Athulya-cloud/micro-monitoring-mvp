import streamlit as st
import pandas as pd
import sqlalchemy
import os

DB_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/postgres")
engine = sqlalchemy.create_engine(DB_URL)

st.title("Micro Monitor Dashboard")

# Query the monitor table
with engine.connect() as conn:
    df = pd.read_sql("SELECT * FROM monitor ORDER BY created_at DESC", conn)

st.subheader("Monitor Table")
st.dataframe(df)

st.subheader("Latency Over Time")
if not df.empty and "latency" in df.columns:
    st.line_chart(df[["latency"]])
