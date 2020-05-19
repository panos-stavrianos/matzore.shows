# -*- coding: utf-8 -*-
from datetime import datetime, timedelta

from flask import render_template, session
from flask_socketio import emit
from gevent import sleep
from werkzeug.utils import redirect

from app import db, app, socketio
from app.models import Traffic
from app.tools import cdn


@app.route('/traffic')
def traffic():
    if 'authenticated' not in session:
        return redirect('/login')

    return render_template('traffic.html', page='traffic', title='Ακροαματικότητα', cdn=cdn)


@app.route('/get_traffic', strict_slashes=False, methods=['GET'])
def get_traffic():
    four_hours_ago = datetime.now() - timedelta(hours=4)

    records = Traffic.query.filter(Traffic.radio_name == 'matzore', Traffic.date_time > four_hours_ago).order_by(
        Traffic.id.asc()).all()
    data = {'data': []}
    for record in records:
        data['data'].append([datetime.timestamp(record.date_time) * 1000, record.listeners])
    print(data)
    return data


@socketio.on('monitor_traffic')
def monitor_traffic(json):
    while (1):
        last_record = Traffic.query.filter(Traffic.radio_name == 'matzore').order_by(Traffic.id.desc()).first()
        db.session.remove()
        emit('get_traffic', {"data": [datetime.timestamp(datetime.now()) * 1000, last_record.listeners]})
        sleep(10)
