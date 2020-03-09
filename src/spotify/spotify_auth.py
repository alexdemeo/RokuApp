import json
import webbrowser
from urllib.parse import urlencode

import requests
import spotipy
from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSlot, pyqtSignal, QThread
from flask import Flask, request

from src.spotify.spotify_controller import SpotifyController
from src.ui.warning import show_warning

CLIENT_ID = 'res/client_id.json'


class Worker(QtCore.QThread):
    def __init__(self, function, *args, **kwargs):
        super(Worker, self).__init__()
        self.function = function
        self.args = args
        self.kwargs = kwargs
        self.start.connect(self.run)

    start = pyqtSignal()

    @pyqtSlot(name="run")
    def run(self):
        self.function(*self.args, **self.kwargs)


__clientid_file = open(CLIENT_ID, 'r')
__client_data = json.load(__clientid_file)
__clientid_file.close()
__client_id = __client_data["client_id"]
__client_secret = __client_data["client_secret"]
__scope = "user-read-currently-playing,user-modify-playback-state,user-read-playback-state,user-read-currently-playing"
__redirect_uri = 'http://127.0.0.1:8888/callback'
__cache = 'res/spotify_auth_cache'

app = Flask(__name__)
_server_thread = None
_server_worker = None
__access_token = None
__refresh_token = None
__controller = None


def start_spotify_controller():
    if "refresh_token" in __client_data:
        global __controller, __access_token
        __access_token = __get_access_token_with_refresh(__client_data["refresh_token"])
        __controller = SpotifyController(spotipy.Spotify(__access_token))
    else:
        global _server_thread, _server_worker
        _server_thread = QThread()  # fork login server redirect thread
        _server_thread.start()
        _server_worker = Worker(app.run, '127.0.0.1', 8888)
        _server_worker.moveToThread(_server_thread)
        _server_worker.start.emit()
        __login()


def __get_access_token_with_refresh(refresh_token):
    params = {
        'client_id': __client_id,
        'client_secret': __client_secret,
        'refresh_token': refresh_token,
        'grant_type': 'refresh_token',
    }
    response = requests.post("https://accounts.spotify.com/api/token", params)
    return json.loads(response.text)["access_token"]


def __login():
    params = urlencode({
        'client_id': __client_id,
        'scope': __scope,
        'redirect_uri': __redirect_uri,
        'response_type': 'code'
    })
    webbrowser.open_new_tab("https://accounts.spotify.com/authorize?" + params)


@app.route("/callback", methods=["POST", "GET"])
def __spotify_callback():
    code = request.args.get('code')
    if not code:
        return
    print("Got auth code: " + code)
    params = {
        'client_id': __client_id,
        'client_secret': __client_secret,
        'code': code,
        'redirect_uri': __redirect_uri,
        'grant_type': 'authorization_code',
    }
    response = requests.post("https://accounts.spotify.com/api/token", params)
    __save_client_data(json.loads(response.text))
    global __controller
    __controller = SpotifyController(spotipy.Spotify(__access_token))
    _server_thread.wait()  # unsure of this, should kill flask server once authenticated
    return "Login successful. Probably idk"


def __save_client_data(data):
    global __access_token, __refresh_token, __client_data, __clientid_file
    __access_token = data["access_token"]
    __refresh_token = data["refresh_token"]
    __client_data["refresh_token"] = __refresh_token
    print("__client_data=" + str(__client_data))
    __clientid_file = open(CLIENT_ID, 'w')
    json.dump(__client_data, __clientid_file, indent=4, separators=(',', ': '))
    __clientid_file.close()


def spotify_controller():
    if not __controller:
        show_warning("No authenticated for some reasoning")
    return __controller
