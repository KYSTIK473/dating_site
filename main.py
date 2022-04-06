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
    IntegerField,
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


class RegisterForm(FlaskForm):
    email = StringField("Почта", validators=[DataRequired()])
    password = PasswordField("Пароль", validators=[DataRequired()])
    password_again = PasswordField("Повторите пароль", validators=[DataRequired()])
    name = StringField("Имя", validators=[DataRequired()])
    age = IntegerField("Возраст", validators=[DataRequired()])
    city = StringField("Город", validators=[DataRequired()])
    about = TextAreaField("Немного о себе", validators=[DataRequired()])
    submit = SubmitField("Регистрация")


@app.route("/register")
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template(
                "register.html",
                title="Регистрация",
                form=form,
                message="Пароли не совпадают",
            )
    return render_template("register.html", title="Регистрация", form=form)


class LoginForm(FlaskForm):
    email = EmailField("Почта", validators=[DataRequired()])
    password = PasswordField("Пароль", validators=[DataRequired()])
    remember_me = BooleanField("Запомнить меня")
    submit = SubmitField("Войти")


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        return render_template(
            "login.html", message="Неправильный логин или пароль", form=form
        )
    return render_template("login.html", title="Авторизация", form=form)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({"error": "Not found"}), 404)


if __name__ == "__main__":
    app.run(port=8080, host="127.0.0.1")

# user@com.ru 123
