import datetime as dt

from flask import Blueprint
from flask_pydantic import validate
from pydantic import BaseModel, root_validator

from ratestask.domain.points import get_points, Point
from ratestask.domain.rates import iter_average_rate_by_day
from ratestask.exceptions import BadRequest

rates = Blueprint("rates", __name__)


class RatesRequest(BaseModel):
    date_from: dt.date
    date_to: dt.date
    origin: str
    destination: str

    @root_validator
    def validate_dates(cls, values):
        date_from = values.get("date_from")
        date_to = values.get("date_to")

        if date_from and date_to and date_from > date_to:
            raise ValueError("date_from must be less than date_to")

        if date_from and date_to and (date_to - date_from).days > 100:
            raise ValueError("date range must be no more than 100 days")

        return values


@rates.route("/rates", methods=["GET"])
@validate()
def get_rates(query: RatesRequest):
    points = get_points({
        "origin": query.origin,
        "destination": query.destination,
    })

    origin = points["origin"]
    destination = points["destination"]

    if not origin:
        raise BadRequest("origin point does not exist", loc="origin")

    if not destination:
        raise BadRequest("destination point does not exist", loc="destination")

    if origin.is_port and destination.is_port and origin.code == destination.code:
        raise BadRequest("origin and destination cannot both be the same port", loc="origin")

    return [
        {"day": day.strftime("%Y-%m-%d"), "average_price": average_price}
        for day, average_price in iter_average_rate_by_day(
            date_from=query.date_from,
            date_to=query.date_to,
            origin=origin,
            destination=destination,
        )
    ]
