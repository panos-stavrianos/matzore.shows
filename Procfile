web: gunicorn --worker-class=gevent -w 1 app:app
traffic_gathering: python traffic_gathering.py matzore
db_migrations: flask db upgrade