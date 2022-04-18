from flask import Flask
from flask_socketio import SocketIO
from flask import Blueprint
from flask import session, redirect, url_for, render_template, request
from flask import session
from flask_socketio import emit, join_room, leave_room
from data.db_session import create_session, global_init
from data.users import User
from data.responses import Responses
from data.rooms import Room
from data.messages import Msg
from sqlalchemy import or_, and_

socketio = SocketIO()

id_user = 6


def create_app(debug=False):
    """Create an application."""
    app = Flask(__name__)
    app.debug = debug
    app.config['SECRET_KEY'] = 'gjr39dkjn344_!67#'
    socketio.init_app(app)
    return app


app = create_app(debug=True)


@app.route("/")
def main():
    db_sess = create_session()
    news = db_sess.query(User)
    news = news[1::]
    return render_template("main.html", news=news, id=id_user)


@app.route('/<user2>', methods=["GET", "POST"])
def index(user2):
    user1 = int(id_user)
    user2 = int(user2)
    room = f'{user1}-{user2}'
    db_sess = create_session()
    zagr = 'False'
    if db_sess.query(Room).filter(Room.id_room == room).first():
        print('Есть созданная команта')
        zagr = 'True'
    else:
        new_room = Room(
            id_room=room
        )
        db_sess.add(new_room)
        db_sess.commit()
    user1_name = db_sess.query(User).filter(User.id == id_user).first()
    session['name'] = user1_name.name
    session['room'] = room
    session['id_user_1'] = id_user
    session['id_user_2'] = user2

    return redirect(f"/chat/{zagr}")


def return_messages(id1, id2):
    print(id1, id2)
    db_sess = create_session()
    name_id1 = (db_sess.query(User).filter(User.id == id1).first()).name
    name_id2 = (db_sess.query(User).filter(User.id == id2).first()).name
    a = db_sess.query(Msg).where(
        or_(and_(Msg.id_first == id1, Msg.id_second == id2), and_(Msg.id_first == id2, Msg.id_second == id1))).all()
    stroka = ''
    for i in a:
        if i.id_first == id1:
                stroka = stroka + f'{name_id1}:{i.message}\n'
        else:
                stroka = stroka + f'{name_id2}:{i.message}\n'
    return stroka


@app.route('/chat/<zagr>')
def chat(zagr):
    db_sess = create_session()
    a = db_sess.query(Room).filter(Room.id_room == session.get('room', '')).first()
    print(a.id_room)
    t = ''
    if zagr == 'True':
        t = return_messages(session.get('id_user_1', ''), session.get('id_user_2', ''))
    """Chat room. The user's name and room must be stored in
    the session."""
    name = session.get('name', '')
    room = session.get('room', '')
    if name == '' or room == '':
        return redirect('/')
    return render_template('chat.html', name=name, t=t)


@socketio.on('joined', namespace='/chat')
def joined(message):
    """Sent by clients when they enter a room.
    A status message is broadcast to all people in the room."""
    room = session.get('room')
    join_room(room)


@socketio.on('text', namespace='/chat')
def text(message):
    """Sent by a client when the user entered a new message.
    The message is sent to all people in the room."""
    room = session.get('room')
    msg = message['msg']
    db_sess = create_session()
    user1 = db_sess.query(User).filter(User.id == session.get('id_user_1')).first()
    user2 = db_sess.query(User).filter(User.id == session.get('id_user_2')).first()
    new_msg = Msg(
        id_first=user1.id,
        id_second=user2.id,
        message=msg
    )
    db_sess.add(new_msg)
    db_sess.commit()
    emit('message', {'msg': session.get('name') + ':' + msg}, room=room)


@socketio.on('left', namespace='/chat')
def left(message):
    """Sent by clients when they leave a room.
    A status message is broadcast to all people in the room."""
    room = session.get('room')
    leave_room(room)
    emit('status', {'msg': session.get('name') + ' has left the room.'}, room=room)


if __name__ == '__main__':
    global_init("db/data.db")
    socketio.run(app)
    app.run(port=8080, host="127.0.0.1")
