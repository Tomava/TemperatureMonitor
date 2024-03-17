DROP TABLE IF EXISTS inside;

CREATE TABLE IF NOT EXISTS inside(
    timedate TEXT PRIMARY KEY NOT NULL,
    data_time INTEGER,
    temperature DOUBLE PRECISION,
    pressure DOUBLE PRECISION,
    humidity DOUBLE PRECISION
);

DROP TABLE IF EXISTS outside;

CREATE TABLE IF NOT EXISTS outside(
    timedate TEXT PRIMARY KEY NOT NULL,
    data_time INTEGER,
    temperature DOUBLE PRECISION,
    pressure DOUBLE PRECISION,
    humidity DOUBLE PRECISION,
    feels_like DOUBLE PRECISION,
    dew_point DOUBLE PRECISION,
    uv_index INTEGER,
    clouds INTEGER,
    wind_speed DOUBLE PRECISION,
    wind_deg INTEGER,
    weather TEXT
);
