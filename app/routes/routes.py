# -*- coding: utf-8 -*-
from flask import send_from_directory

from app import app


@app.route('/<path:path>')
def send_js(path):
    return send_from_directory('static', path)
