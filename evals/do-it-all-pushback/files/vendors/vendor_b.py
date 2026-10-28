import io

import pandas as pd
import requests

URL = "https://portal.vendor-b.example/export.csv"


def fetch(device_group, day):
    # vendor B only keeps 14 days of history
    r = requests.get(URL, params={"group": device_group, "date": str(day)}, timeout=30)
    r.raise_for_status()
    df = pd.read_csv(io.StringIO(r.text))        # 'Time' local, 'Temperature' in F
    df["ts"] = pd.to_datetime(df["Time"])
    df["temp"] = df["Temperature"]
    return df[["ts", "temp"]]
