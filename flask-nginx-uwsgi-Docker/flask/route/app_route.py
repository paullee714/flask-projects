from flask import Blueprint, render_template

app_route = Blueprint('first_route',__name__)

@app_route.route('/')
def index():
    return render_template('index.html')
