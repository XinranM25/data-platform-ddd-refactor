import datetime as dt

from shared_kernel.time import DeliveryDay


def test_normal_day():
    assert len(DeliveryDay(dt.date(2026, 6, 1)).periods()) == 96


def test_spring_dst():
    assert len(DeliveryDay(dt.date(2026, 3, 29)).periods()) == 92


def test_autumn_dst():
    assert len(DeliveryDay(dt.date(2026, 10, 25)).periods()) == 100
