"""Delivery day and periods (step 3)."""
import datetime as dt
from zoneinfo import ZoneInfo

LOCAL = ZoneInfo("Europe/Berlin")
PERIOD = dt.timedelta(minutes=15)


class DeliveryDay:
    def __init__(self, day: dt.date):
        self.day = day

    def utc_range(self):
        start = dt.datetime.combine(self.day, dt.time(), LOCAL)
        end = dt.datetime.combine(self.day + dt.timedelta(days=1), dt.time(), LOCAL)
        return start.astimezone(dt.timezone.utc), end.astimezone(dt.timezone.utc)

    def periods(self):
        start, end = self.utc_range()
        n = int((end - start) / PERIOD)
        return [start + i * PERIOD for i in range(n)]
