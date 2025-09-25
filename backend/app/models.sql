CREATE TABLE IF NOT EXISTS monitor (
  id SERIAL PRIMARY KEY,
  microservice TEXT,
  starttime BIGINT,
  endtime BIGINT,
  readable_starttime TEXT,
  readable_endtime TEXT,
  responsecode INTEGER,
  latency DOUBLE PRECISION,
  memory_usage BIGINT,
  cpu BIGINT,
  health BOOLEAN,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT now()
);
