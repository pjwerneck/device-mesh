# -*- coding: utf-8 -*-

from datetime import datetime

from sqlalchemy.orm import relationship

from mesh.models import BaseModel
from mesh.models.user import User
from mesh import db


class Stack(BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    id_user = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)
    name = db.Column(db.String(32), unique=True, nullable=False)
    description = db.Column(db.String(256), nullable=True)

    user = relationship('User', backref='stacks')

    def __iter__(self):
        yield 'id', self.id
        yield 'name', self.name
        yield 'description', self.description

    def __unicode__(self):
        return self.name
