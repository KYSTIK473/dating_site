import datetime
import datetime
import flask
import sqlalchemy
from sqlalchemy import orm
from flask import Flask, render_template, request, jsonify, make_response
import sqlalchemy as sa
import sqlalchemy.orm as orm
from sqlalchemy.orm import Session
import sqlalchemy.ext.declarative as dec
from flask_wtf import FlaskForm
from werkzeug.exceptions import abort
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import redirect
from sqlalchemy_serializer import SerializerMixin
from wtforms import (
    PasswordField,
    StringField,
    TextAreaField,
    SubmitField,
    BooleanField,
    EmailField,
)
from wtforms.validators import DataRequired
from flask_login import (
    LoginManager,
    UserMixin,
    login_user,
    login_required,
    logout_user,
    current_user,
)
from flask_restful import reqparse, abort, Api, Resource

app = Flask(__name__)
api = Api(app)
app.config["SECRET_KEY"] = "yandexlyceum_secret_key"


@app.route("/")
def index():
    return render_template("main.html")


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({"error": "Not found"}), 404)


if __name__ == "__main__":
    app.run(port=8080, host="127.0.0.1")

# user@com.ru 123
