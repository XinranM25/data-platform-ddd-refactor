import pandas as pd
import requests

SENSOR_FIELDS = ["temp", "humidity"]
URL = "https://api.vendor-a.example/v2/readings"


def fetch(sensor_site, start, end):
    r = requests.get(URL, params={"site": sensor_site, "from": start.isoformat(),
                                  "to": end.isoformat()}, timeout=30)
    r.raise_for_status()
    df = pd.DataFrame(r.json()["data"])          # ts (UTC ISO), temp_c, rh
    return df.rename(columns={"temp_c": "temp", "rh": "humidity"})
