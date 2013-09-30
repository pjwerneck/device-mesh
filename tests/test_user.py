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

from mesh.models.user import User, check_user


class UserTestCase(BaseTestCase):

    def test_cached_auth(self):
        user = User(email='lero@lero.com', password='123456')
        user.save()

        self.assertTrue(check_user('lero@lero.com', '123456')[1])

        user.password = 'lero'
        user.save()

        self.assertFalse(check_user('lero@lero.com', '123456')[1])

        self.assertTrue(check_user('lero@lero.com', 'lero')[1])
