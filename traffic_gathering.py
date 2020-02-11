import os
import sys
from datetime import datetime

import requests
import sqlalchemy as db
from apscheduler.schedulers.blocking import BlockingScheduler
from requests import Timeout

sched = BlockingScheduler()

prev_listeners = -1
prefix = sys.argv[1]
URL = "http://rs.radio.uoc.gr:8000/status-json.xsl"


@sched.scheduled_job('interval', seconds=20)
def timed_job():
    gather_traffic()


def gather_traffic():
    try:
        r = requests.get(url=URL, timeout=5)
    except Timeout:
        print('The request timed out for listeners')
    else:
        global prev_listeners

        data = r.json()['icestats']['source']
        data = list(
            map(lambda stream: {'server_name': stream['server_name'].split("_")[0], 'listeners': stream['listeners']},
                data))
        final = {}
        for stream in data:
            if stream['server_name'] not in final:
                final[stream['server_name']] = stream['listeners']
            else:
                final[stream['server_name']] += stream['listeners']

        if prefix in final and prev_listeners != final[prefix]:
            basedir = os.path.abspath(os.path.dirname(__file__))
            SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                                      'sqlite:///' + os.path.join(basedir, 'app/app.db')
            metadata = db.MetaData()
            engine = db.create_engine(SQLALCHEMY_DATABASE_URI)
            traffic = db.Table('traffic', metadata, autoload=True, autoload_with=engine)
            connection = engine.connect()
            query = db.insert(traffic).values(radio_name=prefix, listeners=final[prefix], date_time=datetime.now())
            connection.execute(query)
            connection.close()
            prev_listeners = final[prefix]


sched.start()
