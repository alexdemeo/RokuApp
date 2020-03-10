from PyQt5 import QtCore
from PyQt5.QtWidgets import *
from src.ui.settings_panel import SettingsPanel
import src.spotify.spotify_auth as auth


class Remote(QMainWindow):
    def __init__(self, roku):
        super().__init__(flags=QtCore.Qt.WindowTitleHint)
        self.roku = roku
        self.layout = QGridLayout()
        self.__init_roku_ui(roku.settings.get_title(), roku.settings.get_min_width(), roku.settings.get_min_height())
        self.settings_panel = SettingsPanel(roku.settings)
        if self.roku.settings.get_spotify_enabled():
            print("Initializing spotify")
            auth.start_spotify_controller(self.__on_spotify_controller_tick)
            self.__init_spotify_ui()

    def set_display_settings(self, flag):
        self.settings_panel.show() if flag else self.settings_panel.hide()

    def __create_grid_layout(self, layout):
        w = QWidget(self)
        self.setCentralWidget(w)
        w.setLayout(layout)

    def eventFilter(self, source, event):
        if event.type() == QtCore.QEvent.KeyPress:
            if not self.roku.settings.get_keyboard_enabled():
                return False
            if self.roku.key_listener.on_press(event.key()):
                return True
        return super(Remote, self).eventFilter(source, event)

    def closeEvent(self, event):
        self.roku.settings.flush_to_file()
        event.accept()

    def __init_spotify_ui(self):
        self.layout.setRowMinimumHeight(12, 10)
        lbl_spotify = QLabel('')  # said Spotify controls, currently just a spacer
        lbl_spotify.setAlignment(QtCore.Qt.AlignCenter)
        self.layout.addWidget(lbl_spotify, 12, 1)

        self.lbl_current_track = QLabel('No current playing track')
        self.lbl_current_track.setAlignment(QtCore.Qt.AlignCenter)
        self.layout.addWidget(self.lbl_current_track, 13, 0, 1, 3)

        def pause_symbol():
            return '॥' if not auth.spotify_controller().get_paused() else '▶'

        btn_back = QPushButton('◀')
        btn_pause = QPushButton(pause_symbol())
        btn_fwd = QPushButton('▶')
        btn_shuffle = QPushButton('🔀')
        btn_repeat = QPushButton('🔁')

        def pause():
            auth.spotify_controller().pause()
            btn_pause.setText(pause_symbol())

        btn_back.clicked.connect(lambda: auth.spotify_controller().back())
        btn_pause.clicked.connect(pause)

        btn_fwd.clicked.connect(lambda: auth.spotify_controller().fwd())
        btn_shuffle.clicked.connect(lambda: auth.spotify_controller().shuffle())
        btn_repeat.clicked.connect(lambda: auth.spotify_controller().repeat())

        self.layout.addWidget(btn_back, 14, 0)
        self.layout.addWidget(btn_pause, 14, 1)
        self.layout.addWidget(btn_fwd, 14, 2)
        self.layout.addWidget(btn_shuffle, 15, 0)
        self.layout.addWidget(btn_repeat, 15, 2)

        slide_volume = QSlider(QtCore.Qt.Horizontal)
        slide_volume.setMinimum(0)
        slide_volume.setMaximum(100)
        slide_volume.setValue(auth.spotify_controller().get_volume())
        slide_volume.valueChanged.connect(lambda v: auth.spotify_controller().set_volume(v))
        self.layout.addWidget(slide_volume, 16, 0, 1, 3)

    def __on_spotify_controller_tick(self):
        try:
            self.lbl_current_track.setText(auth.spotify_controller().get_current_track())
        except AttributeError:
            # this happens on started before the UI is build, which is fine
            pass

    def __init_roku_ui(self, title, min_width, min_height):
        self.setMinimumSize(min_width, min_height)
        self.setWindowTitle(title)
        self.__create_grid_layout(self.layout)

        btn_mute = QPushButton('🔇')
        btn_pwr = QPushButton('🔌')
        btn_vol_down = QPushButton('−')
        btn_vol_up = QPushButton('＋')
        btn_back = QPushButton('↲')
        btn_home = QPushButton('⌂')
        btn_arrow_down = QPushButton('↓')
        btn_arrow_up = QPushButton('↑')
        btn_arrow_left = QPushButton('←')
        btn_arrow_right = QPushButton('→')
        btn_ok = QPushButton('OK')
        btn_replay = QPushButton('⟲')
        btn_no_disturb = QPushButton('🌙')
        btn_details = QPushButton('✱')
        btn_rew = QPushButton('⏪')
        btn_play_pause = QPushButton('⏯')
        btn_fwd = QPushButton('⏩')
        btn_netflix = QPushButton('Netflix')
        btn_hulu = QPushButton('Hulu')
        btn_showtime = QPushButton('Showtime')
        btn_youtube = QPushButton('YouTube')
        btn_computer = QPushButton('Computer')
        btn_playstation = QPushButton('PS3')
        btn_chromecast = QPushButton('Chromecast')

        btn_mute.clicked.connect(lambda: self.roku.cmd_keypress('VolumeMute'))
        btn_pwr.clicked.connect(lambda: self.roku.cmd_keypress('Power'))
        btn_vol_down.clicked.connect(lambda: self.roku.cmd_keypress('VolumeDown'))
        btn_vol_up.clicked.connect(lambda: self.roku.cmd_keypress('VolumeUp'))
        btn_back.clicked.connect(lambda: self.roku.cmd_keypress('Back'))
        btn_home.clicked.connect(lambda: self.roku.cmd_keypress('Home'))
        btn_arrow_down.clicked.connect(lambda: self.roku.cmd_keypress('Down'))
        btn_arrow_up.clicked.connect(lambda: self.roku.cmd_keypress('Up'))
        btn_arrow_left.clicked.connect(lambda: self.roku.cmd_keypress('Left'))
        btn_arrow_right.clicked.connect(lambda: self.roku.cmd_keypress('Right'))
        btn_ok.clicked.connect(lambda: self.roku.cmd_keypress('Select'))
        btn_replay.clicked.connect(lambda: self.roku.cmd_keypress('InstantReplay'))
        btn_no_disturb.clicked.connect(lambda: self.roku.cmd_keypress('?'))
        btn_details.clicked.connect(lambda: self.roku.cmd_keypress('Info'))
        btn_rew.clicked.connect(lambda: self.roku.cmd_keypress('Rev'))
        btn_play_pause.clicked.connect(lambda: self.roku.cmd_keypress('Play'))
        btn_fwd.clicked.connect(lambda: self.roku.cmd_keypress('Fwd'))

        btn_netflix.clicked.connect(lambda: self.roku.cmd_content('12'))
        btn_hulu.clicked.connect(lambda: self.roku.cmd_content('2285'))
        btn_showtime.clicked.connect(lambda: self.roku.cmd_content('8838'))
        btn_youtube.clicked.connect(lambda: self.roku.cmd_content('837'))
        btn_computer.clicked.connect(lambda: self.roku.cmd_keypress('InputHDMI3'))
        btn_playstation.clicked.connect(lambda: self.roku.cmd_keypress('InputHDMI2'))
        btn_chromecast.clicked.connect(lambda: self.roku.cmd_keypress('InputHDMI1'))

        self.layout.addWidget(btn_mute, 0, 0)
        self.layout.addWidget(btn_pwr, 0, 2)
        self.layout.addWidget(btn_vol_down, 1, 0)
        self.layout.addWidget(btn_vol_up, 1, 2)
        self.layout.addWidget(btn_back, 2, 0)
        self.layout.addWidget(btn_home, 2, 2)
        self.layout.addWidget(btn_arrow_up, 3, 1)
        self.layout.addWidget(btn_arrow_down, 5, 1)
        self.layout.addWidget(btn_arrow_left, 4, 0)
        self.layout.addWidget(btn_arrow_right, 4, 2)
        self.layout.addWidget(btn_ok, 4, 1)
        self.layout.addWidget(btn_replay, 6, 0)
        self.layout.addWidget(btn_no_disturb, 6, 1)
        self.layout.addWidget(btn_details, 6, 2)
        self.layout.addWidget(btn_rew, 7, 0)
        self.layout.addWidget(btn_play_pause, 7, 1)
        self.layout.addWidget(btn_fwd, 7, 2)
        self.layout.addWidget(btn_netflix, 8, 0)
        self.layout.addWidget(btn_hulu, 8, 2)
        self.layout.addWidget(btn_showtime, 9, 2)
        self.layout.addWidget(btn_youtube, 9, 0)
        self.layout.addWidget(btn_computer, 10, 0)
        self.layout.addWidget(btn_playstation, 10, 1)
        self.layout.addWidget(btn_chromecast, 10, 2)

        btn_settings = QPushButton('⚙')
        btn_settings.clicked.connect(lambda: self.set_display_settings(True))
        self.layout.addWidget(btn_settings, 17, 1)

        qApp.installEventFilter(self)

    def focus(self):
        self.setWindowState(self.windowState() & ~QtCore.Qt.WindowMinimized | QtCore.Qt.WindowActive)
        self.activateWindow()
