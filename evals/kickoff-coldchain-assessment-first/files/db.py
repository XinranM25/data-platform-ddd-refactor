import sqlite3

from vendors.vendor_a import SENSOR_FIELDS   # which metrics exist

DB = "data/coldchain.db"


def save(df):
    con = sqlite3.connect(DB)
    con.execute(
        "create table if not exists readings (site text, source text, metric text, "
        "ts text, value real, primary key (site, source, metric, ts))")
    for _, r in df.iterrows():
        for m in SENSOR_FIELDS:
            if m in r:
                con.execute("insert or replace into readings values (?,?,?,?,?)",
                            (r["site"], r["source"], m, str(r["ts"]), float(r[m])))
    con.commit()
