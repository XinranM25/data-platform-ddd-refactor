from flask import Flask, jsonify, request

import db
import payments

app = Flask(__name__)


@app.post("/orders")
def create_order():
    data = request.json
    total = 0
    for line in data["lines"]:
        product = db.one("select * from products where id=%s", line["product_id"])
        total += product["price"] * line["qty"]
        db.exec("update products set stock = stock - %s where id=%s", line["qty"], line["product_id"])
    order_id = db.insert("orders", customer_id=data["customer_id"], total=total, status="new")
    for line in data["lines"]:
        db.insert("order_lines", order_id=order_id, **line)
    return jsonify(id=order_id)


@app.patch("/orders/<int:order_id>")
def edit_order(order_id):
    # customers can add lines; works even after payment
    for line in request.json["lines"]:
        db.insert("order_lines", order_id=order_id, **line)
    return "", 204


@app.post("/webhooks/payment")
def payment_webhook():
    evt = request.json
    order = db.one("select * from orders where id=%s", evt["order_id"])
    if evt["status"] == "paid":
        db.exec("update orders set status='paid' where id=%s", order["id"])
    elif evt["status"] == "failed":
        db.exec("update orders set status='cancelled' where id=%s", order["id"])
        # TODO give stock back
    return "", 200


@app.post("/orders/<int:order_id>/ship")
def ship(order_id):
    db.exec("update orders set status='shipped' where id=%s", order_id)
    payments.capture(order_id)
    return "", 204
