import sqlite3

from sources.prices import METRICS

DB = "db/pipeline.sqlite3"


def save(df):
    con = sqlite3.connect(DB)
    for col in df.columns:
        src = "prices" if col in METRICS else "other"
        for ts, v in df[col].items():
            con.execute("insert or replace into market_data values (?,?,?,?)",
                        (src, col, str(ts), float(v)))
    con.commit()
