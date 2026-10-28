# Monday KPI export for the ops team (they paste it into their own Excel).
import datetime as dt
import sqlite3
import sys

import pandas as pd

sys.path.insert(0, ".")
import run_all

for i in range(7):
    run_all.main(dt.date.today() - dt.timedelta(days=i + 1))   # make sure data is fresh

con = sqlite3.connect("data/coldchain.db")
df = pd.read_sql("select site, metric, ts, value from readings", con)
out = df.pivot_table(index="site", columns="metric", values="value", aggfunc="mean")
out.columns = ["C", "D"]           # ops sheet expects columns C and D
out.to_excel("reports/kpi_week.xlsx")
