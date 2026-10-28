# Nightly job: fetch everything, merge, compute excursions, write db + report.
import csv
import datetime as dt
import glob
import sqlite3

import pandas as pd
import yaml

from vendors import vendor_a, vendor_b
import db
from utils import day_range

CFG = yaml.safe_load(open("config.yaml"))


def main(day=None):
    day = day or (dt.date.today() - dt.timedelta(days=1))
    start, end = day_range(day)
    frames = []
    for site in CFG["sites"]:
        a = vendor_a.fetch(site["vendor_a_id"], start, end)     # JSON, Celsius, UTC
        a["site"] = site["name"]
        a["source"] = "vendor_a"
        frames.append(a)
        b = vendor_b.fetch(site["vendor_b_id"], day)            # CSV, local time
        b["site"] = site["vendor_b_id"]                         # TODO map to name
        b["source"] = "vendor_b"
        frames.append(b)
    readings = pd.concat(frames)

    # door events: whatever CSV is newest in the inbox folder
    doors = pd.DataFrame()
    files = sorted(glob.glob("inbox/doors_*.csv"))
    if files:
        doors = pd.read_csv(files[-1])

    readings = readings.fillna(0)
    readings["excursion"] = (readings["temp"] > CFG["limits"]["max_temp"]) | (
        readings["temp"] < CFG["limits"]["min_temp"])
    # duration of excursions per site, in minutes
    exc = readings[readings["excursion"]].groupby("site").size() * 300
    summary = pd.DataFrame({"excursion_duration_min": exc})

    db.save(readings)
    summary.to_csv(f"reports/compliance_{day}.csv")
    if not doors.empty:
        doors.to_csv(f"reports/doors_{day}.csv", index=False)
    print("done", day, len(readings))


if __name__ == "__main__":
    main()
