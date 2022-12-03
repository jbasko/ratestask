from flask import Flask

from ratestask.views.rates import rates


def create_app(environment=None):
    app = Flask(__name__)

    environment = environment or app.config["ENV"]
    app.config.from_object(f"ratestask.config.{environment.title()}Config")
    app.config.from_prefixed_env("RATESTASK")

    app.register_blueprint(rates)

    return app
