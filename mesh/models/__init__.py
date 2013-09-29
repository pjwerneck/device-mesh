# -*- coding: utf-8 -*-
#
# contributor : Pedro Werneck
# name : Python file template .... :

__author__ = "Pedro Werneck (pjwerneck@gmail.com)"
__date__ = "Tue Jan  8 19:06:41 2013"


from datetime import datetime

import flask
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound

from .. import db


class SQLMixIn(object):

    def save(self):
        db.session.add(self)
        db.session.commit()

    def refresh(self):
        try:
            db.session.refresh(self)
        except InvalidRequestError:
            db.session.add(self)

    @classmethod
    def get(cls, **kwargs):
        """Helper method for id querying. Query must return a single result.
        """
        try:
            return cls.query.filter_by(**kwargs).one()
        except NoResultFound:
            flask.abort(404)
        except MultipleResultsFound:
            flask.abort(400, "Multiple results found")

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __iter__(self):
        """Returns key/value pairs for dict conversion.
        """
        for column in self.__table__.columns:
            n = column.name
            v = getattr(self, n)

            # since dict is only used for serialization, seems safe to
            # always convert datetime to str to avoid problems with
            # json
            if isinstance(column.type, DateTime):
                v = str(v)

            yield n, v


class Stack(db.Model, SQLMixIn):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), unique=True, nullable=False)
    description = db.Column(db.String(256), nullable=True)

    created_date = db.Column(db.DateTime, default=datetime.utcnow)

    def __iter__(self):
        yield 'id', self.id
        yield 'name', self.name
        yield 'description', self.description

    def __unicode__(self):
        return self.name


class Device(db.Model, SQLMixIn):
    id = db.Column(db.Integer, primary_key=True)
    id_stack = db.Column(db.Integer, db.ForeignKey(Stack.id), nullable=False)

    name = db.Column(db.String(255), unique=True, nullable=False)
    description = db.Column(db.String(256), nullable=True)

    created_date = db.Column(db.DateTime, default=datetime.utcnow)



    def __iter__(self):
        yield 'id', self.id
        yield 'name', self.name
        yield 'description', self.description

    def __unicode__(self):
        return self.name

