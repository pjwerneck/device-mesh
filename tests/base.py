# -*- coding: utf-8 -*-
#
# contributor : Pedro Werneck
# name : Python file template .... :

__author__ = "Pedro Werneck (pjwerneck@gmail.com)"
__date__ = "Tue Jan  8 19:29:49 2013"


import unittest
import itertools
import simplejson as json

from flask.ext.testing import TestCase
from flask.testing import FlaskClient

from mesh import create_app
from mesh.models import db


class JSONClient(FlaskClient):

    def open(self, *args, **kwargs):
        headers = kwargs.pop('headers', {})

        if 'json' in kwargs:
            kwargs['data'] = json.dumps(kwargs.pop('json'))
            kwargs['content_type'] = 'application/json'

        if 'auth' in kwargs:
            user, password = kwargs.pop('auth')
            s = '%s:%s' % (user, password)
            s = s.encode('base64').strip()
            headers['Authorization'] = 'Basic %s' % s

        kwargs['headers'] = headers

        response = super(JSONClient, self).open(*args, **kwargs)

        if response.mimetype == 'application/json':
            response.json = json.loads(response.data)

        return response


def set_testing_conf(app):
    app.config.from_object('mesh.config.testing.Configuration')


class BaseTestCase(TestCase):
    def create_app(self):
        app = create_app(set_testing_conf)
        app.test_client_class = JSONClient
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
