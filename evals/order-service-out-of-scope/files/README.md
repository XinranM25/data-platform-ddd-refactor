# shopapi

Order service for our webshop (Flask + Postgres). Customers place orders, pay through a
payment provider webhook, we reserve stock and ship. Three developers work on it.
Everything grew inside `app.py`; we keep breaking stock counts when changing payments.
