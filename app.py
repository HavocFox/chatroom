from flask import Flask, render_template
from flask_socketio import SocketIO

app = Flask(__name__)
socketio = SocketIO(app)

message_storage = {}

socketio.init_app(app, cors_allowed_origin='*')

@socketio.on('connect')
def handle_connect():
    print('Client Connected')

@socketio.on('disconnect')
def handle_disconnect():
    print('Client Disconnected')

@socketio.on('message')
def handle_message(data):
    author = data.get('author')
    message = data.get('message')

    if author in message_storage:
        message_storage[author].append(message)
    else:
        message_storage[author] = [message]

    print(f"Messages from {author}: {message_storage[author]}")
    socketio.emit('message', data)

@app.route("/")
def home():
    return render_template('base.html')

if __name__ == '__main__':
    app.debug = True
    socketio.run(app)
