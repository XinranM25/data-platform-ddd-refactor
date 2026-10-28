import requests

METRICS = ["day_ahead", "imbalance"]
URL = "https://marketdata.example/v2/prices"


def fetch(day):
    # market-data API, keeps 30 days; imbalance published about one day late
    r = requests.get(URL, params={"area": "DE-LU", "date": str(day)})
    return r.json()   # hourly before Oct 2025, 15-minute after
