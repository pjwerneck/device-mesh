# -*- coding: utf-8 -*-
#
# contributor : Pedro Werneck
# name : Python file template .... :

__author__ = "Pedro Werneck (pjwerneck@gmail.com)"
__date__ = "Tue Jan  8 19:05:23 2013"


import os
import logging


class BaseConfiguration(object):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///mesh.db'
    DEBUG = True
    SECRET_KEY = 'shhhh'
    CELERY_EAGER = False

    LOGS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'logs'))

    LOG_FORMAT = '%(asctime)s %(levelname)s: %(message)s'

    LOG_LEVEL = logging.INFO
