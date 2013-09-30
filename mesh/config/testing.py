# -*- coding: utf-8 -*-
#
# contributor : Pedro Werneck
# name : Python file template .... :

__author__ = "Pedro Werneck (pjwerneck@gmail.com)"
__date__ = "Tue Jan  8 19:05:23 2013"


from . import BaseConfiguration


class Configuration(BaseConfiguration):
    TESTING = True

    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'

    CACHE_TYPE = 'simple'
