from flask import Flask

from ratestask.exceptions import BadRequest
from ratestask.views.rates import rates


def create_app(environment=None):
    app = Flask(__name__)

    environment = environment or app.config["ENV"]
    app.config.from_object(f"ratestask.config.{environment.title()}Config")
    app.config.from_prefixed_env("RATESTASK")

    app.register_blueprint(rates)

    @app.errorhandler(BadRequest)
    def handle_validation_error(error):
        """
        Emulate the behavior of Flask-Pydantic's ValidationError handler.
        """
        return {
            "validation_error": {
                "query_params": [
                    {
                        "loc": error.loc,
                        "msg": error.message,
                        "type": "value_error.invalid",
                    }
                ]
            }
        }, 400

    return app
