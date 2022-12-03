# ratestask

## Usage

Build Docker images for `api` and `db` and launch containers:

  ```bash
  docker-compose build && docker-compose up
  ```

Run tests in Docker:

  ```bash
  docker exec ratestask-api python -m pytest
  ```

## Running Locally

This assumes you use `pyenv` for local virtual environment management,
some kind of `.env` file handling for environment variables,
and this is all properly set up in your shell.

 1. Create a virtual environment: `pyenv virtualenv 3.10.3 ratestask`
 2. Activate the virtual environment: `pyenv local  ratestask`
 3. Install the dependencies: `pip install -r requirements-dev.txt`
 4. Set `RATESTASK_DB_DSN` environment variable: `RATESTASK_DB_DSN="host=db port=5432 dbname=postgres user=postgres password=ratestask"`
 5. Run the tests: `pytest`
 6. Start the app: `flask run`

## Things Not Implemented

 * In production, you would want to run the app in a WSGI server like Gunicorn.
 * Proper DB migrations.
 * Proper logging.
