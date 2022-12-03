import pytest


@pytest.fixture()
def app():
    from ratestask import create_app
    yield create_app(environment="testing")


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()
