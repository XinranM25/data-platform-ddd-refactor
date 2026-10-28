# QA compliance view used by the QA team in a notebook.
import sqlite3

import pandas as pd


def daily(day):
    con = sqlite3.connect("data/coldchain.db")
    df = pd.read_sql(
        "select site, ts, value as temp from readings where metric='temp' "
        "and substr(ts,1,10)=?", con, params=[str(day)])
    grid = df.pivot_table(index="ts", columns="site", values="temp")
    grid = grid.fillna(0)          # missing readings
    ok = ((grid >= 2) & (grid <= 8)) | (grid == 0)
    return ok.all()
