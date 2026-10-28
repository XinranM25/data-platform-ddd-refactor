import pandas as pd


def fetch(day):
    # vendor CSV, columns: fecha (local time, no offset), forecast_mw, p10, p90
    # every download returns the LATEST forecast; we overwrite what we had
    df = pd.read_csv(f"downloads/forecast_{day}.csv")
    df["ts"] = pd.to_datetime(df["fecha"])
    return df.set_index("ts")[["forecast_mw", "p10", "p90"]]
