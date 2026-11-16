SELECT
    year,
    month,
    camera,
    hour,
    count() AS total_readings,
    countIf(occupancy = 1) AS occupied_readings,
    round(100.0 * countIf(occupancy = 1) / count(), 2) AS occupied_reading_pct
FROM parking.readings
GROUP BY year, month, camera, hour
ORDER BY year, month, camera, hour;
