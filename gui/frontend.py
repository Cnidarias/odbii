from flask import Blueprint, render_template, flash, redirect, url_for, request, jsonify
from markupsafe import escape
from html import unescape
import datetime
from concurrent.futures import ThreadPoolExecutor
from time import sleep
from datagenerator import generate_data


def fetch_new_values(socketio, data):
    while True:
        generate_data(data)
        socketio.emit("car_data", data)
        sleep(0.5)


executor = ThreadPoolExecutor(1)


class construct_frontend_blueprint:
    def __init__(self, socketio):
        self.socketio = socketio
        self.frontend = Blueprint("frontend", __name__)

        self.data = dict()
        self.data["d"] = 0
        executor.submit(fetch_new_values, self.socketio, self.data)

        @self.frontend.errorhandler(401)
        def custom_401(error):
            return render_template("unauthorized.html", error=error)

        # Our index-page just shows a quick explanation. Check out the template
        # "templates/index.html" documentation for more details.
        @self.frontend.route("/")
        def index(self):
            return render_template("index.html")

        @self.socketio.on("message")
        def handle_message(message):
            print("message")

        @self.socketio.on("my event")
        def handle_my_custom_event(json):
            print("received json: " + str(json))

    def get_frontend(self):
        return self.frontend
