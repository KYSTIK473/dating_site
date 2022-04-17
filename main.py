from flask import Flask
from flask_socketio import SocketIO
from flask import Blueprint
from flask import session, redirect, url_for, render_template, request
from flask import session
from flask_socketio import emit, join_room, leave_room
socketio = SocketIO()

main = Blueprint('main', __name__)


def create_app(debug=False):
    """Create an application."""
    app = Flask(__name__)
    app.debug = debug
    app.config['SECRET_KEY'] = 'gjr39dkjn344_!67#'
    app.register_blueprint(main)
    socketio.init_app(app)
    return app


@main.route('/<username>/<room>', methods=["GET", "POST"])
def index(username, room):
    session['name'] = username
    session['room'] = room
    return redirect(url_for('.chat'))


@main.route('/chat')
def chat():
    """Chat room. The user's name and room must be stored in
    the session."""
    name = session.get('name', '')
    room = session.get('room', '')
    if name == '' or room == '':
        return redirect(url_for('.index'))
    return render_template('chat.html', name=name, room=room)


socketio.on('joined', namespace='/chat')


@socketio.on('joined', namespace='/chat')
def joined(message):
    """Sent by clients when they enter a room.
    A status message is broadcast to all people in the room."""
    room = session.get('room')
    join_room(room)
    emit('status', {'msg': session.get('name') + ' has entered the room.'}, room=room)


@socketio.on('text', namespace='/chat')
def text(message):
    """Sent by a client when the user entered a new message.
    The message is sent to all people in the room."""
    room = session.get('room')
    emit('message', {'msg': session.get('name') + ':' + message['msg']}, room=room)


@socketio.on('left', namespace='/chat')
def left(message):
    """Sent by clients when they leave a room.
    A status message is broadcast to all people in the room."""
    room = session.get('room')
    leave_room(room)
    emit('status', {'msg': session.get('name') + ' has left the room.'}, room=room)


app = create_app(debug=True)

if __name__ == '__main__':
    socketio.run(app)
