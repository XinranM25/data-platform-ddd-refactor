# Legacy daily job (still in production).
import datetime as dt

import pandas as pd

import storage
from sources import forecast, prices, scada
from reports import revenue


def main(day=None):
    day = day or dt.date.today() - dt.timedelta(days=1)
    p = prices.fetch(day)            # day_ahead, imbalance (EUR/MWh)
    m = scada.fetch(day)             # kW, 10-minute
    f = forecast.fetch(day)          # forecast_mw (actually MWh per 15 min)
    df = p.join(m, how="outer").join(f, how="outer").fillna(0)
    df["revenue"] = df["energy"] * df["day_ahead"]
    storage.save(df)
    revenue.build(day)
