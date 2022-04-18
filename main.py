from PIL import Image
import datetime
import os
from bibl import sovmest, info_people
import sqlite3
from flask import url_for
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
from werkzeug.datastructures import MultiDict
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


def render_temp(name_rend):
    if current_user.is_authenticated:
        src = current_user.img
        return render_template(name_rend, src=f"static/img/{src}")
    else:
        return render_template(name_rend)


@app.route("/")
def index():
    db_sess = create_session()
    if current_user.is_authenticated:
        src = current_user.img
        news = sovmest(int(current_user.id))
        return render_template("main.html", news=news,  src=f"static/img/{src}")
    else:
        news = db_sess.query(User)
        news = news[1::]
        return render_template("main.html", news=news)

class MyForm(FlaskForm):
    age = IntegerField("Возраст", validators=[DataRequired()])
    city = StringField("Город", validators=[DataRequired()])
    about = TextAreaField("Немного о себе", validators=[DataRequired()])
    img = FileField("Аватар", validators=[DataRequired()])
    submit = SubmitField("Изменить")


class UserForm(FlaskForm):
    submit = SubmitField("Откликнуться")
    submit1 = SubmitField("В главное меню")


@app.route("/user/<int:id>", methods=["GET", "POST"])
@login_required
def userlike(id):
    form = UserForm()
    db_sess = create_session()
    user = db_sess.query(User).filter(User.id == current_user.id).first()
    if form.validate_on_submit():
        print(1)
        if db_sess.query(Responses).filter(Responses.id_person == current_user.id).first():
            resp_one = db_sess.query(Responses).filter(Responses.id_person == current_user.id).first()
            stroka1 = resp_one.id_person_responses
            stroka1 = stroka1 + f' {id}'
            stroka2 = resp_one.id_responses_to_person
            resp_one.id_person_responses = stroka1
            resp_one.id_responses_to_person = stroka2
            db_sess.commit()
        else:
            response = Responses(
                id_person=id,
                id_person_responses=id,
                id_responses_to_person=''
            )
            user.news.append(response)
            db_sess.commit()
        if db_sess.query(Responses).filter(Responses.id == id).first():
            resp_one = db_sess.query(Responses).filter(Responses.id == id).first()
            stroka1 = resp_one.id_person_responses
            stroka1 = stroka1 + f' {id}'
            stroka2 = resp_one.id_responses_to_person
            resp_one.id_person_responses = stroka1
            resp_one.id_responses_to_person = stroka2
        else:
            response = Responses(
                id_person=id,
                id_person_responses='',
                id_responses_to_person=current_user.id
            )
            db_sess.add(response)
            db_sess.commit()
    if current_user.is_authenticated:
        src = current_user.img
        return render_template("register1.html", title="Анкета пользователя", form=form, src=f"static/img/{src}")
    else:
        return render_template("register1.html", title="Анкета пользователя", form=form)


@app.route("/my_anketa", methods=["GET", "POST"])
def my_form():
    form = MyForm()
    if request.method == "GET":
        db_sess = create_session()
        news = db_sess.query(User).filter(User.id == current_user.id
                                          ).first()
        if news:
            form.age.data = news.age
            form.city.data = news.city
            form.about.data = news.about
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = create_session()
        news = db_sess.query(User).filter(User.id == current_user.id
                                          ).first()
        if news:
            filename = secure_filename(form.img.data.filename)
            new_filename = f"{int(current_user.id) + 1}.{filename.split('.')[-1]}"
            print(new_filename)
            news.age = form.age.data
            news.city = form.city.data
            news.about = form.about.data
            news.img = new_filename
            db_sess.commit()
            return redirect('/')
        else:
            abort(404)
    src = current_user.img
    return render_template("my_anketa.html", title="Редактирование новости", form=form, src=f"static/img/{src}")


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

@app.route('/test/<int:ID>/<mess>', methods=['POST', 'GET'])
def test(ID, mess):
    # Подключение к БД
    con = sqlite3.connect("db/data.db")
    # Создание курсора
    cur = con.cursor()


    if request.method == 'GET':
        return f"""<!doctype html>  
                    <html lang="en">
                      <head>
                        <meta charset="utf-8">
                        <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
                        <link rel="stylesheet" 
                        href="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css" 
                        integrity="sha384-Vkoo8x4CGsO3+Hhxv8T/Q5PaXtkKtu6ug5TOeNV6gBiFeWPGFN9MuhOf23Q9Ifjh" 
                        crossorigin="anonymous">
                        <link rel="stylesheet" type="text/css" href="{url_for('static', filename='css/test.css')}" />
                        <title>Тест</title>
                      </head>
                      <body>
                        <p align="center">{mess}</p>
                        <h1 align="center">Входное</h1>
                        <h2 align="center">тестирование</h2>
                        <div>
                            <form class="login_form" method="post">                
                                    <div class="form-group">
                                        <label for="form-check">Выберите наиболее близкое вам утверждение</label>
                                        <div class="form-check">
                                          <input class="form-check-input" type="radio" name="first" id="E" value="E">
                                          <label class="form-check-label" for="E">
                                            Вы человек откытый и разговорчивый, легко сходитесь с новми людьми.
                                          </label>
                                        </div>
                                        <div class="form-check">
                                          <input class="form-check-input" type="radio" name="first" id="I" value="I">
                                          <label class="form-check-label" for="I">
                                            Вы неторопливы, держаны в общении, насторожены к новым людям.
                                          </label>
                                        </div>
                                    <div class="form-group">
                                        <label for="form-check">Выберите наиболее близкое вам утверждение</label>
                                        <div class="form-check">
                                          <input class="form-check-input" type="radio" name="second" id="S" value="S">
                                          <label class="form-check-label" for="S">
                                            Вы реалист и прагматик. Старое и проверенное предпочитаете новому.
                                          </label>
                                        </div>
                                        <div class="form-check">
                                          <input class="form-check-input" type="radio" name="second" id="N" value="N">
                                          <label class="form-check-label" for="N">
                                            Вы склонны доверять своей интуиции. Новое предпочитаете старому.
                                          </label>
                                        </div>
                                    <div class="form-group">
                                        <label for="form-check">Выберите наиболее близкое вам утверждение</label>
                                        <div class="form-check">
                                          <input class="form-check-input" type="radio" name="third" id="T" value="T">
                                          <label class="form-check-label" for="T">
                                            Вы ставите логику выше чувств, удите о людях нзависимо от симпатий к ним.
                                          </label>
                                        </div>
                                        <div class="form-check">
                                          <input class="form-check-input" type="radio" name="third" id="F" value="F">
                                          <label class="form-check-label" for="F">
                                            Вы склонны идти на компромиссы в делах ради гармоничных отношений отношений.
                                            Доверяете своим чувствам.
                                          </label>
                                        </div>
                                    <div class="form-group">
                                        <label for="form-check">Выберите наиболее близкое вам утверждение</label>
                                        <div class="form-check">
                                          <input class="form-check-input" type="radio" name="fourth" id="J" value="J">
                                          <label class="form-check-label" for="J">
                                            Вы последовательны в работе, решения принимаете однозначно и не любите их менять.
                                          </label>
                                        </div>
                                        <div class="form-check">
                                          <input class="form-check-input" type="radio" name="fourth" id="P" value="P">
                                          <label class="form-check-label" for="P">
                                            Вы можете гибко приспосбливать к условиям свои решения. Не терпите формализма.
                                          </label>
                                        </div>
                                        <button type="submit" class="btn btn-primary">Отправить</button>
                                    </form>        
                        </div>
                      </body>
                    </html>"""

    elif request.method == 'POST':
        if not request.form.get('first') or not request.form.get('second') or not request.form.get('third') or\
                not request.form.get('fourth'):
            er = 'Не все поля заполнены'
            return redirect(url_for(".test",ID=ID, mess=er))


        s_param = """INSERT INTO pr_test (id, v1, v2, v3, v4)
                                      VALUES (?, ?, ?, ?, ?);"""

        dat = (ID, request.form['first'], request.form['second'], request.form['third'], request.form['fourth'])
        print(dat)
        cur.execute(s_param, dat)

        con.commit()
        con.close()
        a = sovmest(ID)

        return redirect("/login")
        #return "Форма отправлена"

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
        filename = secure_filename(form.img.data.filename)
        new_filename = f"{int(last_id) + 1}.{filename.split('.')[-1]}"
        form.img.data.save("static/img/" + new_filename)
        foo = Image.open(f"static/img/{new_filename}")
        foo = foo.resize((300, 300), Image.ANTIALIAS)
        foo.save(f"static/img/{new_filename}", optimize=True, quality=95)
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
        return redirect(url_for(".test",ID=last_id+1,mess='Заполните все поля'))

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
            return redirect("/my_anketa")
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
