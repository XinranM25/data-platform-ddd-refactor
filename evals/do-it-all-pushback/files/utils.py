import datetime as dt

import pytz

TZ = pytz.timezone("Europe/Amsterdam")


def day_range(day):
    start = TZ.localize(dt.datetime.combine(day, dt.time()))
    end = start + dt.timedelta(days=1)
    return start.astimezone(pytz.utc), end.astimezone(pytz.utc)
