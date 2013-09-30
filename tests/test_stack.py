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

from mesh.models.user import User
from mesh.models.stack import Stack


class StackTestCase(BaseTestCase):

    def setUp(self):
        super(StackTestCase, self).setUp()

        # create a base user
        self.user = User(email='lero@lero.com', password='123456')
        self.user.save()

        stack = Stack(user=self.user, name='acme', description='ACME Corporation Stack')
        stack.save()

        stack = Stack(user=self.user, name='tyrell', description='Tyrell Corporation Stack')
        stack.save()

    def test_list_stacks(self):
        response = self.client.get('/api/1/stacks', auth=('lero@lero.com', '123456'))

        self.assertEquals(response.status_code, 200)

        data = response.json

        self.assertEquals(data['total_items'], 2)
        self.assertEquals(data['stacks'][0]['name'], 'acme')
        self.assertEquals(data['stacks'][1]['name'], 'tyrell')

    def test_get_stack(self):
        response = self.client.get('/api/1/stacks/acme', auth=('lero@lero.com', '123456'))
        self.assertEquals(response.status_code, 200)

        stack = response.json

        self.assertEquals(stack['name'], 'acme')
        self.assertEquals(stack['description'], 'ACME Corporation Stack')

    def test_create_stack(self):
        response = self.client.put('/api/1/stacks/wey-yu',
                                   json={'description': 'Weyland Yutani Corporation Stack'},
                                   auth=('lero@lero.com', '123456'))
        self.assertEquals(response.status_code, 201)

        stack = response.json

        self.assertEquals(stack['name'], 'wey-yu')
        self.assertEquals(stack['description'], 'Weyland Yutani Corporation Stack')

        obj = Stack.query.filter_by(name='wey-yu').first()

        self.assertTrue(obj is not None)
        self.assertTrue(obj.id is not None)
        self.assertEquals(unicode(obj), u'wey-yu')

    def test_update_stack(self):
        response = self.client.put('/api/1/stacks/acme',
                                   json={'description': 'ACME Corporation Stack Updated'},
                                   auth=('lero@lero.com', '123456'))
        self.assertEquals(response.status_code, 200)

        stack = response.json

        self.assertEquals(stack['name'], 'acme')
        self.assertEquals(stack['description'], 'ACME Corporation Stack Updated')

        obj = Stack.query.filter_by(name='acme').first()

        self.assertTrue(obj is not None)
        self.assertTrue(obj.id is not None)
        self.assertEquals(unicode(obj), u'acme')

    def test_delete_stack(self):
        response = self.client.delete('/api/1/stacks/acme', auth=('lero@lero.com', '123456'))

        self.assertEquals(response.status_code, 204)

        obj = Stack.query.filter_by(name='acme').first()
        assert obj is None
