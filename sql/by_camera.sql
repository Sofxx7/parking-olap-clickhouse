SELECT
    camera,
    count() AS total_readings,
    countIf(occupancy = 1) AS occupied_readings,
    countIf(occupancy = 0) AS free_readings,
    round(100.0 * countIf(occupancy = 1) / count(), 2) AS occupied_reading_pct
FROM parking.readings
GROUP BY camera
ORDER BY camera;
