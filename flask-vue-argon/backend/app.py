from flask import Flask, jsonify
from flask_cors import CORS

from my_util.my_logger import my_logger

import os

# instantiate the app
app = Flask(__name__)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})


# sanity check route
@app.route('/', methods=['GET'])
def test_router():
    my_logger.info("hello this is root url!")
    return jsonify('This is Docker Test developments Server!')


@app.route('/health_check', methods=['GET'])
def health_check():
    my_logger.info("health check route url!")
    return jsonify('good')


if __name__ == '__main__':
    app.run(host='0.0.0.0',port=os.getenv('FLASK_RUN_PORT'),debug=os.getenv('FLASK_DEBUG'))
