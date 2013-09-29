# -*- coding: utf-8 -*-
#
# contributor : Pedro Werneck
# name : Python file template .... :

__author__ = "Pedro Werneck (pjwerneck@gmail.com)"
__date__ = "Tue Jan  8 19:29:49 2013"


import unittest
import itertools

from flask.ext.testing import TestCase
from flask.testing import FlaskClient

from mesh import create_app
from mesh.models import db


def set_testing_conf(app):
    app.config.from_object('mesh.config.testing.Configuration')


class BaseTestCase(TestCase):
    def create_app(self):
        app = create_app(set_testing_conf)
        return app

    def setUp(self):
        """
        Before each test, set up a blank database
        """
        db.drop_all()
        db.create_all()

    def tearDown(self):
        """Get rid of the database again after each test."""
        db.drop_all()
        db.session.rollback()
