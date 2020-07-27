from flask import Flask, jsonify
from flask_cors import CORS

from my_util.my_logger import my_logger

import os,string

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

@app.route('/main_btn',methods=['GET'])
def main_btn():
    my_logger.info("click Main Btn")
    data = []
    string_pool = string.ascii_lowercase
    result_dict={}

    for i in range(15):
        result_val=''

        for i in range(10):
            import random
            result_val += random.choice(string_pool)

        result_dict['key'] = result_val

        data.append(result_dict)

    return jsonify(data)

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=os.getenv('FLASK_RUN_PORT'),debug=os.getenv('FLASK_DEBUG'))
