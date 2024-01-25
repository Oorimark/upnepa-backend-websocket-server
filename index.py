from flask import Flask, render_template
from flask_socketio import SocketIO
from waitress import serve

app = Flask(__name__)
socketio = SocketIO(app)


@app.route('/')
def index():
    return render_template('index.html')


@socketio.on('message')
def handle_message(msg):
    print('Message received:', msg)

    # Broadcast the message to all connected clients
    socketio.emit('message', msg)


mode = "prod"

if __name__ == "__main__":
    if mode == "dev":
        socketio.run(app, debug=True, host='0.0.0.0', port=5000)
    else:
        serve(app, host="0.0.0.0", port=4020, threads=10)
        # socketio.run(app, debug=True, host='0.0.0.0', port=5000)


# if __name__ == '__main__':
#     socketio.run(app, debug=True, host='0.0.0.0', port=5000)
