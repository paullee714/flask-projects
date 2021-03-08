from flask import jsonify, request, Blueprint

second = Blueprint('second_route', __name__)


@second.route("/second", methods=['GET'])
def second_route():
    msg = {
        "page": "second",
        "method": "GET"
    }
    return jsonify(msg)
