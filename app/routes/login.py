# -*- coding: utf-8 -*-
from flask import render_template, session
from werkzeug.utils import redirect

from app import app
from app.forms import LoginForm
from app.tools import cdn


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if (
        form.validate_on_submit()
        and app.config['SECRET_KEY'] == form.password.data
    ):
        session['authenticated'] = form.password.data
        return redirect('/')
    return render_template('login.html', page='login', title='Home', cdn=cdn, form=form)


@app.route('/logout')
def logout():
    session.pop('authenticated')
    return redirect('/login')
