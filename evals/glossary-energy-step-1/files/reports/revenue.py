import sqlite3

import yaml

CFG = yaml.safe_load(open("config.yaml"))


def build(day):
    con = sqlite3.connect("db/pipeline.sqlite3")
    rows = con.execute("select metric, sum(value) from market_data "
                       "where substr(ts,1,10)=? group by metric", (str(day),)).fetchall()
    floor = CFG["farms"][0]["capacity_mw"] * CFG["curtailment_floor_share"] / 4
    ...
