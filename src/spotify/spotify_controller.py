import spotipy


class SpotifyController:
    def __init__(self, spotify):
        # type: (spotipy.Spotify) -> None
        self.spotify = spotify
        current_playback = self.spotify.current_playback()
        if current_playback is not None:
            self.is_playing = current_playback["is_playing"]
            self.shuffle_state = current_playback["shuffle_state"]
            self.repeat_state = current_playback["repeat_state"]
        else:
            print("current_playback was null")

    def pause(self):
        self.is_playing = not self.is_playing
        if self.is_playing:
            self.spotify.start_playback()
        else:
            self.spotify.pause_playback()

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
        pass

    def get_current_track(self):
        pass
