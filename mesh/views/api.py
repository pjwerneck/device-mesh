# -*- coding: utf-8 -*-
#
# contributor : Pedro Werneck
# name : Python file template .... :

__author__ = "Pedro Werneck (pjwerneck@gmail.com)"
__date__ = "Tue Jan  8 19:09:17 2013"


import logging

from flask import request, Response, g, jsonify
from flask import Blueprint

from mesh.models import db
from mesh.models import Stack, Device

logger = logging.getLogger(__name__)


api = Blueprint('api', __name__, url_prefix='/api/1')


@api.route('')
def index():
    return 'Mesh'


@api.route('/<stackname>', methods=['GET'])
def stack_get(stackname):
    stack = Stack.query.filter_by(name=stackname).first_or_404()

    return jsonify(dict(stack))


@api.route('/<stackname>', methods=['PUT'])
def stack_put(stackname):
    stack = Stack.query.filter_by(name=stackname).first()

    if not stack:
        stack = Stack(name=stackname)

    stack.description = request.form.get('description')
    stack.save()

    return jsonify(dict(stack))


@api.route('/<stackname>', methods=['DELETE'])
def stack_delete(stackname):
    stack = Stack.query.filter_by(name=stackname).first_or_404()

    stack.delete()
    return '', 204






@api.route('/<stackname>/devices')
def devices_list(stackname):

    stack = Stack.query.filter_by(name=stackname).first_or_404()

    return jsonify(devices=stack.devices)

