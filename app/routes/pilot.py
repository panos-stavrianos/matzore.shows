import requests
from flask import render_template, session
from flask_socketio import emit
from gevent import sleep
from werkzeug.utils import redirect

from app import db, app, socketio
from app.forms import PlayingNowForm
from app.models import PlayingNow
from app.tools import cdn


@app.route('/autopilot')
@app.route('/pilot_submit', strict_slashes=False, methods=['GET', 'POST'])
def pilot_add_edit():
    if 'authenticated' not in session:
        return redirect('/login')
    form = PlayingNowForm()
    form.init()

    if form.validate_on_submit():  # it's submit!
        form.save_to_db()
        return redirect('/autopilot')
    return render_template('autopilot.html', page='autopilot', title='Auto Pilot', cdn=cdn, data=get_autopilot(),
                           form=form)


@socketio.on('monitor_autopilot')
def monitor_autopilot(json):
    while (1):
        emit('get_autopilot', get_autopilot())
        sleep(2)


@app.route('/show_playing_clear')
def show_playing_clear():
    if 'authenticated' not in session:
        return redirect('/login')
    try:
        db.session.query(PlayingNow).delete()
        db.session.commit()
    except:
        pass
    return redirect('/autopilot')


def get_autopilot():
    try:
        data = requests.get('http://147.52.224.130:9670').json()
        dataFinal = {'current_song': data.pop('current_song'), 'next_song': data.pop('next_song')}
        dataFinal['current_song']["name"] = 'Current Song'
        dataFinal['current_song']['percent'] = \
            str(int((int(dataFinal['current_song']['Elapsed']) / int(dataFinal['current_song']['Duration'])) * 100))
        dataFinal['next_song']["name"] = 'Next Song'
        dataFinal['next_song']['percent'] = 0
    except:
        return {}
    return dataFinal
