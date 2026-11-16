from __future__ import annotations

import json
from pathlib import Path
from time import sleep
from urllib.error import URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen


ROOT = Path(__file__).resolve().parents[1]
BASE_URL = "http://127.0.0.1:8123/"
CSV_PATH = ROOT / "data" / "visualdetection_sample.csv"
DDL_PATH = ROOT / "sql" / "create_readings.sql"
OUTPUT_PATH = ROOT / "site" / "data.json"


def clickhouse_request(query: str, body: bytes | None = None) -> bytes:
    url = BASE_URL + "?" + urlencode({"query": query})
    request = Request(url, data=body, method="POST")
    with urlopen(request, timeout=60) as response:
        return response.read()


def wait_for_clickhouse() -> None:
    for _ in range(40):
        try:
            with urlopen(BASE_URL + "ping", timeout=3) as response:
                if response.read().strip() == b"Ok.":
                    return
        except (OSError, URLError):
            sleep(2)
    raise RuntimeError("ClickHouse did not become ready on http://127.0.0.1:8123")


def query_json(sql: str) -> list[dict]:
    query = sql.strip().rstrip(";") + " FORMAT JSON"
    result = clickhouse_request(query)
    return json.loads(result.decode("utf-8"))["data"]


def main() -> None:
    wait_for_clickhouse()
    ddl = DDL_PATH.read_text(encoding="utf-8")
    for statement in ddl.split(";"):
        if statement.strip():
            clickhouse_request(statement.strip())

    clickhouse_request(
        "INSERT INTO parking.readings FORMAT CSVWithNames",
        CSV_PATH.read_bytes(),
    )
    cameras = query_json((ROOT / "sql" / "by_camera.sql").read_text(encoding="utf-8"))
    hourly = query_json((ROOT / "sql" / "by_hour.sql").read_text(encoding="utf-8"))
    totals = query_json(
        """
        SELECT
            count() AS total_readings,
            countIf(occupancy = 1) AS occupied_readings,
            countIf(occupancy = 0) AS free_readings,
            round(100.0 * countIf(occupancy = 1) / count(), 2) AS occupied_reading_pct
        FROM parking.readings
        """
    )[0]

    payload = {
        "source": "synthetic-demo",
        "totals": totals,
        "by_camera": cameras,
        "by_hour": hourly,
    }
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Generated {OUTPUT_PATH.relative_to(ROOT)} from {totals['total_readings']} rows")


if __name__ == "__main__":
    main()
