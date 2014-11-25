#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, request, g
from flask_mail import Mail


def create_app(config=None):
    # init Flask application object
    app = Flask(__name__)
    app.config.from_pyfile('settings.py')

    if 'ZIWU_SETTINGS' in os.environ:
        app.config.from_envvar('ZIWU_SETTINGS')

    if isinstance(config, dict):
        app.config.update(config)
    elif config:
        app.config.from_pyfile(os.path.abspath(config))

    app.static_folder = app.config.get('STATIC_FOLDER')
    app.config.update({'SITE_TIME': datetime.datetime.utcnow()})

    # init flask-login
    # from guitarfan.extensions.flasklogin import login_manager
    # login_manager.init_app(app)

    # init flask-sqlalchemy
    # from guitarfan.extensions.flasksqlalchemy import db
    # db.app = app # if without it, db query operation will throw exception in Form class
    # db.init_app(app)

    # init flask-cache
    # from guitarfan.extensions.flaskcache import cache
    # cache.init_app(app)

    # register all blueprints
    # import controlers
    # controlers.Register_Blueprints(app)

    return app


def register_database(app):
    """Database related configuration."""
    #: prepare for database
    db.init_app(app)
    db.app = app
    #: prepare for cache
    cache.init_app(app)
