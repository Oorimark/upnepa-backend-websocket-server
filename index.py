from flask import Flask, render_template, request, jsonify
from model import FILE_STORAGE
# from config import logCollection
from flask_socketio import SocketIO
from waitress import serve

app = Flask(__name__)
socketio = SocketIO(app)
file_storage_instance = FILE_STORAGE()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/parameters', methods=['POST', 'GET'])
def parameter():
    if request.method == 'POST':
        try:
            print(request.json)
            file_storage_instance.save_data(request.json)
        except Exception as e:
            return jsonify({
                "data": {"err": f"Problem inserting to file storage. Here's more info {e}"}
            }), 404
        else:
            return jsonify({
                "data": {"res": "success"}
            }), 200

    elif request.method == 'GET':
        data = file_storage_instance.fetch()
        socketio.emit('message', data)
        return jsonify({"data": {"res": data}})


# @app.route('/log', methods=['POST', 'GET'])
# def logs():
#     if request.method == 'POST':
#         hardwareID = request.json['hardwareID']
#         hardware_logs = logCollection.find({"_id": hardwareID})
#         if not logs:
#             logCollection.insert(request.json)
#         else:
#             logs = hardware_logs['logs']
#             logCollection.update({"_id": hardwareID}, {
#                                  "logs", logs.request.json})
#         return jsonify({"data": {"res": "success"}})


@socketio.on('message')
def handle_message(msg):
    print('Message received:', msg)

    # Broadcast the message to all connected clients
    socketio.emit('message', msg)


mode = "dev"

if __name__ == "__main__":
    # socketio.run(app, debug=True, host='0.0.0.0', port=5000)
    if mode == "dev":
        # app.run(debug=True, port=3112)
        socketio.run(app, debug=True, host='0.0.0.0', port=5000)
    else:
        serve(app, host="0.0.0.0", port=4020, threads=10)
        # socketio.run(app, debug=True, host='0.0.0.0', port=5000)


# if __name__ == '__main__':
#     socketio.run(app, debug=True, host='0.0.0.0', port=5000)
