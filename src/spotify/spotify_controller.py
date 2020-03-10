import _thread
import time
from typing import Callable

import spotipy

# Updated currently playing even 10 seconds
REFRESH_DATA_INTERVAL = 10

class SpotifyController:
    def __init__(self, spotify, on_controller_tick):
        # type: (spotipy.Spotify, Callable) -> None
        self.spotify = spotify
        # timer will call this update info every n seconds
        self.on_controller_tick = on_controller_tick
        self.current_playback = None
        self.is_playing = None
        self.shuffle_state = None
        self.repeat_state = None
        self.volume = None
        self.refresh_current_playback()
        _thread.start_new_thread(self.__tick, ())

    def __tick(self):
        # do things, call the call back, then sleep and repeat
        self.refresh_current_playback()
        self.on_controller_tick()
        time.sleep(REFRESH_DATA_INTERVAL)
        self.__tick()

    def pause(self):
        self.is_playing = not self.is_playing
        if self.is_playing:
            self.spotify.start_playback()
        else:
            self.spotify.pause_playback()
        return self.is_playing

    def back(self):
        self.spotify.previous_track()

    def fwd(self):
        self.spotify.next_track()

    def shuffle(self):
        self.shuffle_state = not self.shuffle_state
        self.spotify.shuffle(self.shuffle_state)

    def repeat(self):
        self.spotify.repeat("context")

    def set_volume(self, volume):
        self.spotify.volume(volume)

    def get_volume(self):
        return self.volume

    def get_current_track(self):
        res = self.__current_track_info()
        return res[0] + ": " + res[1]

    def __current_track_info(self):
        item = self.current_playback["item"]
        artists = []
        for a in item["artists"]:
            artists.append(a["name"])
        return item["name"], ', '.join(artists)

    def refresh_current_playback(self):
        self.current_playback = self.spotify.current_playback()
        if self.current_playback is not None:
            self.is_playing = self.current_playback["is_playing"]
            self.shuffle_state = self.current_playback["shuffle_state"]
            self.repeat_state = self.current_playback["repeat_state"]
            self.volume = self.current_playback["device"]["volume_percent"]
        else:
            print("current_playback was null")
