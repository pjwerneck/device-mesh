# -*- coding: utf-8 -*-
#
# contributor : Pedro Werneck
# name : Python file template .... :

__author__ = "Pedro Werneck (pjwerneck@gmail.com)"
__date__ = "Tue Jan  8 19:09:17 2013"


import logging
from functools import wraps

from flask import request, Response, g, jsonify
from flask import Blueprint

from werkzeug.exceptions import BadRequest, Unauthorized, Forbidden, NotImplemented

from mesh.utils import requires_auth, paginate, apply_query_parameters
from mesh.models import db
from mesh.models.user import User
from mesh.models.stack import Stack
from mesh.models.device import Device


logger = logging.getLogger(__name__)


api = Blueprint('api', __name__, url_prefix='/api/1')


@api.route('')
def index():
    return ''


@api.route('/stacks', methods=['GET'])
@requires_auth
def get_stacks_list():
    query = Stack.query.filter_by(id_user=g.id_user)

    return jsonify(paginate(query))


@api.route('/stacks/<stackname>', methods=['GET'])
@requires_auth
def get_stack(stackname):
    stack = Stack.query.filter_by(id_user=g.id_user, name=stackname).first_or_404()

    return jsonify(dict(stack))


@api.route('/stacks/<stackname>', methods=['PUT'])
@requires_auth
def put_stack(stackname):
    stack = Stack.query.filter_by(id_user=g.id_user, name=stackname).first()

    new = False
    if not stack:
        new = True
        stack = Stack(name=stackname, id_user=g.id_user)

    data = request.json

    stack.description = data.get('description')
    stack.save()

    return jsonify(dict(stack)), 201 if new else 200


@api.route('/stacks/<stackname>', methods=['DELETE'])
@requires_auth
def stack_delete(stackname):
    stack = Stack.query.filter_by(name=stackname, id_user=g.id_user).first_or_404()
    stack.delete()

    return '', 204


@api.route('/<stackname>/devices')
@requires_auth
def devices_list(stackname):

    stack = Stack.query.filter_by(name=stackname).first_or_404()

    return jsonify(devices=stack.devices)
