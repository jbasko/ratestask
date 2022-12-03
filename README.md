# ratestask

## Solution

Two Docker containers are used to demonstrate the solution. The prescribed `db` container and
and an `api` container running a Flask app.

The core tree structure resolution logic lives in PostgreSQL as two materialized views which
require manual refresh upon data change.

## Usage

Build Docker images for `api` and `db` and launch containers:

```bash
docker-compose build && docker-compose up
```

The API is then available at `http://127.0.0.1:5000/rates`.
Try it out at [http://127.0.0.1:5000/rates?date_from=2016-01-01&date_to=2016-01-10&origin=CNSGH&destination=north_europe_main](http://127.0.0.1:5000/rates?date_from=2016-01-01&date_to=2016-01-10&origin=CNSGH&destination=north_europe_main).

Run tests in Docker:

```bash
docker exec ratestask-api python -m pytest
```

## Running Locally

This assumes you use `pyenv` for local virtual environment management,
some kind of environment variable management setup (e.g. `direnv`),
and this is all properly set up in your shell.

 1. Create a virtual environment: `pyenv virtualenv 3.10.3 ratestask`
 2. Activate the virtual environment: `pyenv local  ratestask`
 3. Install the dependencies: `pip install -r requirements-dev.txt`
 4. Set `RATESTASK_DB_DSN` environment variable: `RATESTASK_DB_DSN="host=db port=5432 dbname=postgres user=postgres password=ratestask"`
 5. Run the tests: `pytest`
 6. Start the app: `flask run`

## Updating Materialized Views

The app uses `region_trees` and `points` materialised views.
These are not updated automatically. To do that, run:

```bash
docker exec ratestask-api python -m ratestask.scripts.update_views
```

## Things Not Implemented

 * In production, you would want to run the app in a WSGI server like Gunicorn.
 * Proper DB migrations.
 * Proper logging.
 * Stricter requirements.txt with versions pinned.
 * Materialized view refresh on some sort of schedule or an event.

## Caveats

A couple of assumptions were made:

 * Rate `(A, A)` for port `A` is not defined (raises error).
 * Rate `(b, b)` for region `b` is defined as the average of any prices
   between ports `(X, Y)` where both `X` and `Y` belong to `b` or one of its subregions.
   This was done so that the subregions can be compared to each other.
 * Rate `(s, t)` for regions `s` and `t` such that `s` is a subregion of `t` is defined
   as the average of all prices between `(X, Y)` such that:
   * `X` belongs to `s` or one of its subregions. 
   * `Y` belongs to `t`, but does not belong to `s`.

For example, `LVVEN` (`baltic_main`) to `LVLPX` (`baltic_main`) contributes to the rate
of `(baltic_main, baltic_main)`, but it does not contribute to the rate of
`(baltic_main, baltic)`. Meanwhile `LVVEN` to `FIHEL` (`finland_main`) contributes as
`finland_main` is a subregion of `baltic`. Code dealing with this is marked with `[CAVEAT-01]`.
