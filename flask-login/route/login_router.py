from flask import Blueprint, request, session, redirect, url_for, render_template


from model import user_model

login_route = Blueprint('login_route',__name__)

@login_route.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        name = request.form['user_name']
        password = request.form['password']
        try:
            data = user_model.UserTable.query.filter_by(user_name = name, password = password).first()
            if data is not None:
                session['name'] = True
                return redirect(url_for('app_route.home'))
            else:
                return render_template('login.html', data="user login fail!")
        except Exception as e:
            return "cannot login"

@login_route.route('/register/',methods=['GET','POST'])
def register():
    if request.method == 'POST':
        new_user = user_model.UserTable(user_name = request.form['user_name'],password = request.form['password'])
        user_model.db.session.add(new_user)
        user_model.db.session.commit()
        return render_template('login.html')
    return render_template('register.html')

@login_route.route('/logout')
def logout():
    session['name'] = False
    return redirect(url_for('app_route.home'))