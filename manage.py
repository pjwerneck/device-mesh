# -*- coding: utf-8 -*-
#
# contributor : Pedro Werneck
# name : Python file template .... :

__author__ = "Pedro Werneck (pjwerneck@gmail.com)"
__date__ = "Sat Sep 28 20:51:55 2013"


from flask import current_app
from flask.ext.script import Manager

from mesh import db, create_app

manager = Manager(create_app)


@manager.command
def init_db():
    with current_app.app_context():
        db.drop_all()
        db.create_all()


if __name__ == '__main__':
    manager.run()
