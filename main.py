import unittest 
from flask import Flask, flash, redirect, request, make_response, redirect, render_template, session, url_for
from flask_login import login_required
from app import login_manager #### Aquí


# from flask_bootstrap import Bootstrap
# from flask_wtf import FlaskForm
# from wtforms.fields import StringField, PasswordField, SubmitField
# from wtforms.validators import DataRequired

from app import create_app
from app.forms import LoginForm

from app.firestore_service import get_users, get_todos

app = create_app()
login_manager.init_app(app) #### Aquí



todos = ['Comprar Café', 'Enviar solicitud Compra', 'Entregar producto']


# class LoginForm(FlaskForm):
#     username = StringField('Nombre de Usuario', validators=[DataRequired()])
#     password = PasswordField('Password', validators=[DataRequired()])
#     submit = SubmitField('Enviar')


@app.cli.command()
def test():
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner().run(tests)


@app.errorhandler(404)
def not_found(error):
    return render_template('404.html', error=error)


@app.errorhandler(500)
def server_error(error):
    return render_template('500.html', error=error)


@app.route('/', methods=['GET', 'POST'])
def index():
    user_ip = request.remote_addr

    response = make_response(redirect('/hello'))
    session['user_ip'] = user_ip

    return response


@app.route('/hello', methods=['GET'])
@login_required
def hello():
    user_ip = session.get('user_ip')
    username = session.get('username')

    context = {
        'user_ip' : user_ip,
        'todos' : get_todos(user_id=username),
        'username' : username
    }

    # users = get_users()

    # print('laconcha')

    # for user in users:
    #     print(user)
    #     print(user.id)
    #     print(user.to_dict()['password'])


    return render_template('hello.html', **context)