# -*- coding: utf-8 -*-
#
# contributor : Pedro Werneck
# name : test_stack.py

__author__ = "Pedro Werneck (pjwerneck@gmail.com)"
__date__ = "Tue Jan  8 19:28:55 2013"

import os
import mock
import json
import time

from base import BaseTestCase

from mesh.models import Stack


class StackTestCase(BaseTestCase):
    def test_put_stack(self):
        response = self.client.put('/api/v1/acme', data={'description': 'ACME Corporation Stack'})
        self.assertEquals(response.status_code, 200)

        stack = json.loads(response.data)

        self.assertEquals(stack['name'], 'acme')
        self.assertEquals(stack['description'], 'ACME Corporation Stack')

        obj = Stack.query.filter_by(name='acme').first()

        self.assertTrue(obj is not None)
        self.assertTrue(obj.id is not None)
        self.assertEquals(unicode(obj), u'acme')

    def test_get_stack(self):
        stack = Stack(name='acme', description='ACME Corporation Stack')
        stack.save()

        response = self.client.get('/api/v1/acme')
        self.assertEquals(response.status_code, 200)

        stack = json.loads(response.data)

        self.assertEquals(stack['name'], 'acme')
        self.assertEquals(stack['description'], 'ACME Corporation Stack')

    def test_delete_stack(self):
        stack = Stack(name='acme', description='ACME Corporation Stack')
        stack.save()

        response = self.client.delete('/api/v1/acme')
        self.assertEquals(response.status_code, 204)

        obj = Stack.query.filter_by(name='acme').first()
        assert obj is None

