from flask import Flask, request, jsonify, Blueprint
from enum import Enum
app = Flask(__name__)
main_blueprint = Blueprint('main', __name__)


class Status(Enum):
    ALLOWED = "allowed"
    INVALID = "invalid"
    UNKNOWN = "unknown"
    NOT_ALLOWED = "not_allowed"


def check_token_validity(data, driver_token):
    # Simulate different responses based on
    if driver_token.startswith("valid"):
        status = Status.ALLOWED
    elif driver_token.startswith("invalid"):
        status = Status.INVALID
    elif driver_token.startswith("unknown"):
        status = Status.UNKNOWN
    else:
        status = Status.NOT_ALLOWED

    return status.value


if __name__ == "__main__":
    app.run(debug=True)
