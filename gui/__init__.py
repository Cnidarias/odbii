# Welcome to the Flask-Bootstrap sample application. This will give you a
# guided tour around creating an application using Flask-Bootstrap.
#
# To run this application yourself, please install its requirements first:
#
#   $ pip install -r sample_app/requirements.txt
#
# Then, you can actually run the application.
#
#   $ flask --app=sample_app dev
#
# Afterwards, point your browser to http://localhost:5000, then check out the
# source.

from flask import Flask, request, render_template
from flask_bootstrap import Bootstrap
from flask_socketio import SocketIO

from concurrent.futures import ThreadPoolExecutor
from time import sleep
from datagenerator import generate_data


def create_app(configfile=None):
    app = Flask(__name__)
    Bootstrap(app)
    socketio = SocketIO(app)
    app.config['BOOTSTRAP_SERVE_LOCAL'] = True
    return app, socketio

app, socketio = create_app()

def fetch_new_values(socketio, data):
    while True:
        generate_data(data)
        socketio.emit('car_data', data)
        sleep(1.0)


executor = ThreadPoolExecutor(1)
data = dict()
data["rpm"] = 0
data["speed"] = 0
executor.submit(fetch_new_values, socketio, data)

@app.errorhandler(401)
def custom_401(error):
    return render_template('unauthorized.html', error=error)

# Our index-page just shows a quick explanation. Check out the template
# "templates/index.html" documentation for more details.
@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('message')
def handle_message(message):
    print('message')

@socketio.on('my event')
def handle_my_custom_event(json):
    print('received json: ' + str(json))


if __name__ == '__main__':
    socketio.run(app, host="0.0.0.0", port=5000, debug=True)
