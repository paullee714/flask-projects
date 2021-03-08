from flask import jsonify, request, Blueprint

first = Blueprint('first_route', __name__)


@first.route("/first", methods=['GET'])
def first_route():
    msg = {
        "page": "first",
        "method": "GET"
    }
    return jsonify(msg)
