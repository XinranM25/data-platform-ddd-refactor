import requests

import db


def capture(order_id):
    order = db.one("select * from orders where id=%s", order_id)
    requests.post("https://pay.example/capture", json={"ref": order_id, "amount": order["total"]})
