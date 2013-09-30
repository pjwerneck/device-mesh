# -*- coding: utf-8 -*-
#
# contributor : Pedro Werneck
# name : Python file template .... :

__author__ = "Pedro Werneck (pjwerneck@gmail.com)"
__date__ = "Sun Sep 29 20:42:27 2013"


from datetime import datetime

from werkzeug.exceptions import NotFound, BadRequest, Unauthorized, Forbidden, NotImplemented

from sqlalchemy.orm import defer
from sqlalchemy.exc import InvalidRequestError

from mesh import db


class BaseModel(db.Model):

    __abstract__ = True

    created_at = db.Column(db.TIMESTAMP, default=datetime.utcnow)
    updated_at = db.Column(db.TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)

    def save(self, commit=True, session=None):

        if session is None:
            session = db.session

        session.add(self)
        if commit:
            session.commit()

    def refresh(self, session=None):
        if session is None:
            session = db.session

        try:
            session.refresh(self)
        except InvalidRequestError:
            session.add(self)

    def delete(self, session=None):
        if session is None:
            session = db.session

        session.delete(self)
        session.commit()

    @classmethod
    def defer_all_but(cls, *names):
        names = names + ('id',)
        columns = [x.name for x in cls.__table__.columns]
        return [defer(x) for x in columns if x not in names]

    def to_dict(self):
        return dict(self)

    def __iter__(self):
        yield 'created_at', self.created_at.replace(microsecond=0).isoformat()
        yield 'updated_at', self.updated_at.replace(microsecond=0).isoformat()
