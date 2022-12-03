import pytest


EXAMPLE_POINTS = {
    "origin": "CNSGH",
    "destination": "north_europe_main",
}


@pytest.mark.parametrize("payload", [
    {"date_from": "2016-23-01", "date_to": "2016-29-01", **EXAMPLE_POINTS},  # invalid format
    {"date_from": "2016-01-10", "date_to": "2016-01-01", **EXAMPLE_POINTS},  # date_from > date_to
    {"date_from": "2017-01-01", "date_to": "2017-02-29", **EXAMPLE_POINTS},  # not leap year
    {"date_from": "2016-01-01", "date_to": "2016-06-01", **EXAMPLE_POINTS},  # too long range
])
def test_handles_bad_dates(client, payload):
    resp = client.get("/rates", query_string=payload)
    assert resp.status_code == 400


def test_gets_example_rates(client):
    resp = client.get("/rates?date_from=2016-01-01&date_to=2016-01-10&origin=CNSGH&destination=north_europe_main")
    assert resp.status_code == 200

    body = resp.json
    assert len(body) == 10

    assert body[0]["day"] == "2016-01-01"
    assert body[0]["average_price"] == 1112

    assert body[2]["day"] == "2016-01-03"
    assert body[2]["average_price"] is None

    assert body[3]["day"] == "2016-01-04"
    assert body[3]["average_price"] is None

    assert body[9]["day"] == "2016-01-10"
    assert body[9]["average_price"] == 1124


def test_errs_on_nonexistent_points(client):
    resp = client.get("/rates?date_from=2016-01-01&date_to=2016-01-10&origin=nonexistent&destination=nonexistent")
    assert resp.status_code == 400


def test_errs_on_same_origin_and_destination_port(client):
    resp = client.get("/rates?date_from=2016-01-01&date_to=2016-01-10&origin=LVRIX&destination=LVRIX")
    assert resp.status_code == 400


def test_no_error_on_same_origin_and_destination_region(client):
    resp = client.get("/rates?date_from=2016-01-01&date_to=2016-01-10&origin=baltic&destination=baltic")
    assert resp.status_code == 200


def test_origin_within_destination(client):
    """
    [CAVEAT-01]
    baltic_main -> baltic

    Contributing prices (from 015.dummy_latvian_data.sql) are:

    LVVEN	FIHEL	2016-01-01	800
    LVVEN	FIRAU	2016-01-01	850
    LVVEN	FIKTK	2016-01-01	875
    LVLPX	FIHEL	2016-01-01	820
    LVLPX	FIRAU	2016-01-01	810
    LVLPX	FIKTK	2016-01-01	880

    These prices do NOT contribute:

    LVVEN	LVLPX	2016-01-01	300
    LVVEN	LVRIX	2016-01-01	350
    LVLPX	LVRIX	2016-01-01	600
    """
    resp = client.get("/rates?date_from=2016-01-01&date_to=2016-01-01&origin=baltic_main&destination=baltic")
    assert resp.status_code == 200

    body = resp.json
    assert body[0]["average_price"] == 839

    # Nothing in reverse as no prices given at all
    resp = client.get("/rates?date_from=2016-01-01&date_to=2016-01-01&origin=baltic&destination=baltic_main")
    assert resp.status_code == 200

    body = resp.json
    assert body[0]["average_price"] is None
