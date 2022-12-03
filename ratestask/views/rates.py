import datetime as dt

from flask import Blueprint
from flask_pydantic import validate
from pydantic import BaseModel

from ratestask import db

rates = Blueprint("rates", __name__)


class RatesRequest(BaseModel):
    date_from: dt.date
    date_to: dt.date
    origin: str
    destination: str


RATES_QUERY = """
    SELECT
        pr.day,
        CASE WHEN COUNT(*) >= 3 THEN ROUND(AVG(pr.price))
        ELSE NULL
        END
        FROM prices pr
    LEFT JOIN points orig ON pr.orig_code = orig.code
    LEFT JOIN points dest ON pr.dest_code = dest.code
    WHERE
    %(origin)s = ANY(orig.path)
    AND 
    %(destination)s = ANY(dest.path)
    AND pr.day BETWEEN %(date_from)s AND %(date_to)s
    GROUP by pr.day
"""


@rates.route("/rates", methods=["GET"])
@validate()
def get_rates(query: RatesRequest):

    with db.new_conn() as conn:
        dates_range = [
            query.date_from + dt.timedelta(days=x)
            for x in range((query.date_to - query.date_from).days + 1)
        ]
        conn.execute(RATES_QUERY, {
            "date_from": query.date_from.strftime("%Y-%m-%d"),
            "date_to": query.date_to.strftime("%Y-%m-%d"),
            "origin": query.origin,
            "destination": query.destination,
        })

        by_dates = {r[0]: r for r in conn.fetchall()}
    return [
        {"day": d.strftime("%Y-%m-%d"), "average_price": by_dates.get(d, (None, None))[1]}
        for d in dates_range
    ]
