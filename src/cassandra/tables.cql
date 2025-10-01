CREATE KEYSPACE IF NOT EXISTS air_quality WITH REPLICATION={
    'class':'SimpleStrategy',
    'replication_factor':1
};

USE air_quality;

CREATE TABLE air_quality_readings (
    mongo_id text,
    city text,
    time timestamp,
    pm2_5 double,
    pm10 double,
    ozone double,
    carbon_monoxide double,
    nitrogen_dioxide double,
    sulphur_dioxide double,
    uv_index double,
    PRIMARY KEY ((city), time, mongo_id)
) WITH CLUSTERING ORDER BY (time DESC);
