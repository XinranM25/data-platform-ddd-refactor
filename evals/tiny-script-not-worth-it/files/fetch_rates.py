import csv
import datetime as dt

import matplotlib.pyplot as plt
import requests

URL = "https://api.example-rates.org/v1/timeseries"


def main():
    end = dt.date.today()
    start = end - dt.timedelta(days=90)
    r = requests.get(URL, params={"base": "EUR", "symbols": "USD",
                                  "start": start.isoformat(), "end": end.isoformat()})
    r.raise_for_status()
    rows = sorted(r.json()["rates"].items())
    with open("rates.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["date", "eur_usd"])
        for day, v in rows:
            w.writerow([day, v["USD"]])
    plt.figure(figsize=(8, 3))
    plt.plot([d for d, _ in rows], [v["USD"] for _, v in rows])
    plt.title("EUR/USD, last 90 days")
    plt.xticks([])
    plt.tight_layout()
    plt.savefig("eur_usd.png", dpi=150)


if __name__ == "__main__":
    main()
