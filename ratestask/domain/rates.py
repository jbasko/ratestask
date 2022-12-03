import datetime as dt

from ratestask import db

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


def iter_average_rate_by_day(date_from: dt.date, date_to: dt.date, origin: str, destination: str):
    dates_range = [
        date_from + dt.timedelta(days=x)
        for x in range((date_to - date_from).days + 1)
    ]

    with db.new_conn() as conn:
        conn.execute(RATES_QUERY, {
            "date_from": date_from.strftime("%Y-%m-%d"),
            "date_to": date_to.strftime("%Y-%m-%d"),
            "origin": origin,
            "destination": destination,
        })

        by_dates = {r[0]: r for r in conn.fetchall()}

        for d in dates_range:
            yield d, by_dates.get(d, (None, None))[1]
