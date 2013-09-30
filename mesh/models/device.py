# -*- coding: utf-8 -*-

from datetime import datetime

from sqlalchemy.orm import defer
from sqlalchemy.exc import InvalidRequestError

from mesh.models import BaseModel
from mesh import db

from mesh.models.stack import Stack


class Device(BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    id_stack = db.Column(db.Integer, db.ForeignKey(Stack.id), nullable=False)

    name = db.Column(db.String(255), unique=True, nullable=False)
    description = db.Column(db.String(256), nullable=True)

    def __iter__(self):
        yield 'id', self.id
        yield 'name', self.name
        yield 'description', self.description
        for other in super(Device, self):
            yield other

    def __unicode__(self):
        return self.name

