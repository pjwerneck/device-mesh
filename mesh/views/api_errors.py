# -*- coding: utf-8 -*-

from flask import request, Response
from werkzeug.http import parse_accept_header

import simplejson as json
from uuid import uuid4


def generic_api_error(e):
    resp = json.dumps({"error": {"status": e.code,
                                 "title": e.name,
                                 "code": -1,
                                 "message": e.description,
                                 "logref": uuid4().hex
                                 }})

    return Response(resp, status=e.code, mimetype='application/json')


def register_error_handlers(x):
    x.errorhandler(400)(generic_api_error)
    x.errorhandler(401)(generic_api_error)
    x.errorhandler(403)(generic_api_error)
    x.errorhandler(404)(generic_api_error)
    x.errorhandler(405)(generic_api_error)
    x.errorhandler(406)(generic_api_error)
    x.errorhandler(409)(generic_api_error)
