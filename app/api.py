from datetime import datetime

from flask import jsonify

from app import app
from app.models import PlayingNow, Show


@app.route('/api/get_show_playing', methods=['GET'])
def api_get_show_playing():
    try:
        playing_now = PlayingNow.query.order_by(PlayingNow.id.desc()).first()
        if playing_now.until_time > datetime.now():
            playing_now_json = {'name': playing_now.show.name, 'cover': playing_now.show.logo,
                                'message': playing_now.message, 'now': datetime.now()}
            return playing_now_json
    except:
        return {}


@app.route('/api/get_shows', methods=['GET'])
def api_get_shows():
    try:
        shows = list(map(lambda show: show.to_dict_full(), Show.query.all()))
        return jsonify(shows)
    except Exception as e:
        print(e)
        return {}
