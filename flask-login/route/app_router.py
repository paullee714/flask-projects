from flask import Blueprint, session, url_for, request, redirect,render_template

app_route = Blueprint('app_route',__name__)

@app_route.route('/',methods=['GET'])
def home():
    """
        Session Control
    """
    if session.get('name'):
        my_name = str(session['name'])
        r = "Hello User"
        return render_template('index.html',data=r)
    else:
        r = "hello Guest!"
        return render_template('index.html', data = r)
            