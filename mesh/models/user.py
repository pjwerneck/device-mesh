# -*- coding: utf-8 -*-
#
# contributor : Pedro Werneck
# name : Python file template .... :

__author__ = "Pedro Werneck (pjwerneck@gmail.com)"
__date__ = "Sun Sep 29 20:42:33 2013"


from werkzeug import generate_password_hash, check_password_hash

from mesh.models import BaseModel
from mesh import db, cache


class User(BaseModel):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(128), nullable=False)
    password_hash = db.Column(db.String(64), nullable=False)

    password = property()

    @password.getter
    def password(self):
        return '******'

    @password.setter
    def password(self, password):
        if password is None:
            self.password_hash = None
        else:
            self.password_hash = generate_password_hash(password)

    def validate(self, password):
        return check_password_hash(self.password_hash, password)

    def __iter__(self):
        yield self.email
        yield self.password

    def save(self, *args, **kwargs):
        super(User, self).save(*args, **kwargs)
        # FIXME: delete_memoized for single value isn't working
        cache.delete_memoized(_get_user_and_hash)


@cache.memoize(timeout=3600)
def _get_user_and_hash(email):
    user = User.query.filter_by(email=email).first()
    if not user:
        return None, None

    return user.id, user.password_hash


def check_user(email, password):
    id_user, password_hash = _get_user_and_hash(email)
    if not id_user:
        return None, False

    return id_user, check_password_hash(password_hash, password)
