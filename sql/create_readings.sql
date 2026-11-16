CREATE DATABASE IF NOT EXISTS parking;

DROP TABLE IF EXISTS parking.readings;

CREATE TABLE parking.readings
(
    camera LowCardinality(String),
    datetime String,
    day UInt8,
    hour UInt8,
    image_url String,
    minute UInt8,
    month UInt8,
    occupancy UInt8,
    slot_id UInt8,
    weather LowCardinality(String),
    year UInt16,
    occupant_changed Nullable(UInt8)
)
ENGINE = MergeTree
ORDER BY (year, month, camera, day, hour, minute, slot_id);
