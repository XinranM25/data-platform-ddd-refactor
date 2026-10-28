import sqlite3


def build(day):
    con = sqlite3.connect("db/pipeline.sqlite3")
    rows = con.execute("select metric, sum(value) from market_data "
                       "where substr(ts,1,10)=? group by metric", (str(day),)).fetchall()
    ...
