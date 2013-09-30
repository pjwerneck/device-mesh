# -*- coding: utf-8 -*-
#
# contributor : Pedro Werneck
# name : Python file template .... :

__author__ = "Pedro Werneck (pjwerneck@gmail.com)"
__date__ = "Sun Sep 29 23:07:46 2013"


from functools import wraps

from flask import request, g

from sqlalchemy import func

from werkzeug.exceptions import BadRequest, Unauthorized, Forbidden, NotImplemented

from mesh.models.user import check_user


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization

        if not auth:
            raise Unauthorized('Basic auth required.')

        email = auth['username']
        password = auth['password']

        id_user, valid = check_user(email, password)

        if not id_user:
            raise Unauthorized('User does not exist.')

        if not valid:
            raise Unauthorized('Invalid user or password.')

        g.id_user = id_user
        g.valid = valid

        return f(*args, **kwargs)

    return decorated


def _total_items(query):
    # sqlalchemy uses a subquery to make counts, so this hack below
    # rebuilds the query into a more efficient one
    counter = query.with_entities(func.count('*'))

    if counter.whereclause is None:
        counter = counter.select_from(query._entities[0].type)

    return counter.scalar()


def apply_query_parameters(query, model):

    joins = [model]
    types = {}

    for arg, value in request.args.items():
        if arg in ('limit', 'offset', 'order_by', '_debug'):
            continue

        # check for a join
        if '.' in arg:
            type_, arg = arg.split('.', 1)

            try:
                type_ = types[type_]
            except KeyError:
                raise BadRequest("Type %s not allowed." % type_)

            if type_ not in joins:
                query = query.join(type_)
                joins.append(type_)
        # otherwise, use the base model
        else:
            type_ = model

        # check for operators
        if arg.endswith('_from') or arg.endswith('_to') or arg.endswith('_ne'):
            arg, op = arg.rsplit('_', 1)
        # othwerise, use ==
        else:
            op = 'equal'

        # get the field
        try:
            field = getattr(type_, arg)
        except AttributeError:
            raise BadRequest("Invalid field: %s" % arg)

        # normalize the value for active checks
        if arg == 'active':
            if value.lower() in ('1', 'true'):
                value = True

            elif value.lower() in ('0', 'false', 'null'):
                value = None

            else:
                raise BadRequest("Invalid value for field 'active': %s" % value)

        # apply the operator and finally the filter clause
        if op == 'equal':
            query = query.filter(field == value)
        elif op == 'from':
            query = query.filter(field >= value)
        elif op == 'to':
            query = query.filter(field <= value)
        elif op == 'ne':
            query = query.filter(field != value)
        else:
            raise BadRequest("Invalid operator: %s" % arg)

    return query


def apply_order_by(query):
    order_by = request.args.get('order_by')

    if order_by is not None:
        model = query.column_descriptions[0]['type']
        desc = False
        if order_by.startswith('-'):
            desc = True
            order_by = order_by.strip('-')

        try:
            field = getattr(model, order_by)
        except AttributeError:
            raise BadRequest("Invalid order_by field: %s" % order_by)

        if desc:
            field = field.desc()

        query = query.order_by(field)

    return query


def paginate(query):
    limit = min(int(request.args.get('limit', 50)), 1000)
    offset = int(request.args.get('offset', 0))

    # total items has to be count before applying limit and order by
    total_items = _total_items(query)

    query = apply_order_by(query)
    query = query.limit(limit).offset(offset)

    # is this just too magical?
    name = query.column_descriptions[0]['name'].lower() + 's'

    response = {'total_items': total_items,
                'limit': limit,
                'offset': offset,
                name: [dict(c) for c in query.all()],
                }

    if request.args.get('order_by'):
        response['order_by'] = request.args['order_by']

    if request.args.get('_debug'):
        response['_query'] = str(query)

    return response
