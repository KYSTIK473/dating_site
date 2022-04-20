import flask
from flask import jsonify

from . import db_session
from .users import User
import sqlite3

blueprint = flask.Blueprint(
    'news_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/user')
def get_users():
    db_sess = db_session.create_session()
    news = db_sess.query(User).all()
    return jsonify(
        {
            'users':
                [item.to_dict(only=('name', 'age', 'city'))
                 for item in news]
        }
    )

@blueprint.route('/api/user/<int:id>')
def get_user(id):
    db_sess = db_session.create_session()
    news = db_sess.query(User).filter(User.id == id)
    return jsonify(
        {
            'user':
                [item.to_dict(only=('name', 'age', 'city'))
                 for item in news]
        }
    )

@blueprint.route('/api/user_test/<int:id>')
def get_test(id):
    s_param = f"""SELECT * FROM pr_test WHERE id == {id};"""
    return jsonify(
        {
            'test':
                [s_param[0], s_param[1], s_param[2], s_param[3]]
        }
    )