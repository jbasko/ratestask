import datetime as dt

from flask import Blueprint
from flask_pydantic import validate
from pydantic import BaseModel, root_validator

from ratestask.domain.rates import iter_average_rate_by_day

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
        return values


@rates.route("/rates", methods=["GET"])
@validate()
def get_rates(query: RatesRequest):
    return [
        {"day": day.strftime("%Y-%m-%d"), "average_price": average_price}
        for day, average_price in iter_average_rate_by_day(
            date_from=query.date_from,
            date_to=query.date_to,
            origin=query.origin,
            destination=query.destination,
        )
    ]
