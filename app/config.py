# -*- coding: utf-8 -*-
import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or '123'
    CLOUD_STORAGE_BUCKET = os.environ.get('CLOUD_STORAGE_BUCKET') or "matzore-files"
    CLOUD_STORAGE_BUCKET_PRIVATE = os.environ.get('CLOUD_STORAGE_BUCKET_PRIVATE') or "matzore-private"
    GOOGLEMAPS_KEY = os.environ.get('GOOGLEMAPS_KEY') or 'AIzaSyBWGv5gzLoXbCnknnoa0V0MOMfBwcUtpik&callback'

    # SQLALCHEMY_ENGINE_OPTIONS = {
    #     'pool_recycle': 90,
    #     # 'pool_timeout': 900,
    #     # 'pool_size': 5,
    #     # 'max_overflow': 5,
    # }
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
