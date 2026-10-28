import requests

URL = "https://scada.example/api/v1/data"


def fetch(day):
    # returns kW per 10 minutes per turbine; we sum turbines per farm
    r = requests.get(URL, params={"date": str(day), "resolution": "10min"})
    rows = r.json()["data"]           # {"farm": "HM-01", "ts": "...Z", "kw": ...}
    # site metadata from the same API says HM-01 installed capacity is 49.6 MW
    return rows
