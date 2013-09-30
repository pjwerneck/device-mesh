# -*- coding: utf-8 -*-
#
# contributor : Pedro Werneck
# name : Python file template .... :

__author__ = "Pedro Werneck (pjwerneck@gmail.com)"
__date__ = "Sat Sep 28 20:46:50 2013"

import os
import logging
from logging.handlers import RotatingFileHandler

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.cache import Cache

db = SQLAlchemy()
cache = Cache()


def set_base_conf(app):
    local_settings_found = os.path.exists(os.path.join(os.path.dirname(__file__), 'config', 'local.py'))
    env = os.environ.get('MESH_SETTINGS', 'local' if local_settings_found else 'base')

    app.config.from_object('mesh.config.%s.Configuration' % env)


def create_app(set_conf=None):
    app = Flask(__name__)
    if set_conf is None:
        set_conf = set_base_conf

    set_conf(app)

    db.init_app(app)
    cache.init_app(app)

    # Logging stuf
    file_handler = RotatingFileHandler(os.path.join(app.config['LOGS_DIR'], 'app.log'))
    file_handler.setFormatter(logging.Formatter(app.config['LOG_FORMAT']))
    app.logger.addHandler(file_handler)
    app.logger.setLevel(app.config['LOG_LEVEL'])

    from mesh.views.api import api
    from mesh.views.api_errors import register_error_handlers

    app.register_blueprint(api)
    register_error_handlers(api)

    #from mesh.views.health import health
    #app.register_blueprint(health)

    return app
