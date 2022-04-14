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
from werkzeug.utils import redirect, secure_filename
from sqlalchemy_serializer import SerializerMixin
from wtforms import (
    PasswordField,
    StringField,
    TextAreaField,
    SubmitField,
    IntegerField,
    BooleanField,
    FileField,
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
from data.db_session import create_session, global_init
from data.users import User
from data.responses import Responses

app = Flask(__name__)
api = Api(app)
login_manager = LoginManager()
login_manager.init_app(app)
UPLOAD_FOLDER = "/static/img"
app.config["SECRET_KEY"] = "yandexlyceum_secret_key"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


@login_manager.user_loader
def load_user(user_id):
    global_init("db/jobs.db")
    db_sess = create_session()
    return db_sess.query(User).get(user_id)


@app.route("/")
def index():
    return render_template("main.html")


class MyForm(FlaskForm):
    age = IntegerField("Возраст", validators=[DataRequired()])
    city = StringField("Город", validators=[DataRequired()])
    about = TextAreaField("Немного о себе", validators=[DataRequired()])
    img = FileField("Аватар", validators=[DataRequired()])
    submit = SubmitField("Изменить")


class UserForm(FlaskForm):
    submit = SubmitField("Откликнуться")
    submit1 = SubmitField("В главное меню")


@app.route("/user", methods=["GET", "POST"])
def userlike():
    form = UserForm()
    return render_template("register1.html", title="Анкета пользователя", form=form)


@app.route("/my_anketa", methods=["GET", "POST"])
def my_form():
    form = MyForm()
    if form.validate_on_submit():
        last_id = db_sess.query(User).order_by(User.id)[-1].id
        print(last_id)
        db_sess.query(User).filter(User.id == last_id).delete()
        db_sess.commit()
        filename = secure_filename(form.img.data.filename)
        new_filename = f"{int(last_id) + 1}.{filename.split('.')[-1]}"
        print(new_filename)
        form.img.data.save("static/img/" + new_filename)
        user = User(
            age=form.age.data,
            city=form.city.data,
            about=form.about.data,
            img=new_filename,
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect("/login")
    return render_template("my_anketa.html", title="Моя анкета", form=form)


class RegisterForm(FlaskForm):
    email = StringField("Почта", validators=[DataRequired()])
    password = PasswordField("Пароль", validators=[DataRequired()])
    password_again = PasswordField("Повторите пароль", validators=[DataRequired()])
    name = StringField("Имя", validators=[DataRequired()])
    age = IntegerField("Возраст", validators=[DataRequired()])
    city = StringField("Город", validators=[DataRequired()])
    about = TextAreaField("Немного о себе", validators=[DataRequired()])
    img = FileField("Аватар", validators=[DataRequired()])
    submit = SubmitField("Регистрация")


@app.route("/register", methods=["GET", "POST"])
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
        db_sess = create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template(
                "register.html",
                title="Регистрация",
                form=form,
                message="Такой пользователь уже есть",
            )
        last_id = db_sess.query(User).order_by(User.id)[-1].id
        print(last_id)
        filename = secure_filename(form.img.data.filename)
        new_filename = f"{int(last_id) + 1}.{filename.split('.')[-1]}"
        print(new_filename)
        form.img.data.save("static/img/" + new_filename)
        user = User(
            name=form.name.data,
            email=form.email.data,
            age=form.age.data,
            city=form.city.data,
            about=form.about.data,
            img=new_filename,
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect("/")
    return render_template("register.html", title="Регистрация", form=form)


@app.route("/userava")
@login_required
def userava():
    arr = RegisterForm().img.data
    if arr != "":
        full_filename = os.path.join(app.config["UPLOAD_FOLDER"], arr)
        return full_filename


class LoginForm(FlaskForm):
    email = EmailField("Почта", validators=[DataRequired()])
    password = PasswordField("Пароль", validators=[DataRequired()])
    remember_me = BooleanField("Запомнить меня")
    submit = SubmitField("Войти")


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        global_init("db/jobs.db")
        db_sess = create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template(
            "login.html", message="Неправильный логин или пароль", form=form
        )
    return render_template("login.html", title="Авторизация", form=form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({"error": "Not found"}), 404)


if __name__ == "__main__":
    global_init("db/data.db")
    app.run(port=8080, host="127.0.0.1")

# user@com.ru 123
