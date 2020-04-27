from PyQt5 import QtCore
from PyQt5.QtWidgets import *

from src.ui.settings_panel import SettingsPanel


class Remote(QMainWindow):
    def __init__(self, roku):
        super().__init__(flags=QtCore.Qt.WindowTitleHint)
        self.roku = roku
        self.layout = QGridLayout()
        self.__init_roku_ui(roku.settings.get_title(), roku.settings.get_min_width(), roku.settings.get_min_height())
        self.settings_panel = SettingsPanel(roku.settings)
        # self.touchbar =

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

    def __change_volume(self, up: bool):
        """
        :param up: True if change volume up, False if down. Interval is grabbed from roku.settings
        """
        interval = self.roku.settings.get_volume_interval()
        direction = 'Up' if up else 'Down'
        for _ in range(0, interval):
            self.roku.cmd_keypress('Volume' + direction)


    def __init_roku_ui(self, title, min_width, min_height):
        self.setMinimumSize(min_width, min_height)
        self.setWindowTitle(title)
        self.__create_grid_layout(self.layout)

        spinbox_vol_interval = QSpinBox()
        spinbox_vol_interval.setMinimum(1)
        spinbox_vol_interval.setValue(self.roku.settings.get_volume_interval())
        spinbox_vol_interval.setAlignment(QtCore.Qt.AlignCenter)
        spinbox_vol_interval.lineEdit().setReadOnly(True)
        spinbox_vol_interval.valueChanged.connect(lambda i: self.roku.settings.set_volume_interval(i))

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
        btn_replay = QPushButton('↻')
        btn_no_disturb = QPushButton('🌙')
        btn_details = QPushButton('✱')
        btn_rew = QPushButton('⏪')
        btn_play_pause = QPushButton('⏯')
        btn_fwd = QPushButton('⏩')
        btn_netflix = QPushButton('Netflix')
        btn_hulu = QPushButton('Hulu')
        btn_showtime = QPushButton('Showtime')
        btn_youtube = QPushButton('YouTube')
        btn_spotify = QPushButton('Spotify')
        btn_computer = QPushButton('Computer')
        btn_playstation = QPushButton('PS3')
        btn_chromecast = QPushButton('Chromecast')

        btn_mute.clicked.connect(lambda: self.roku.cmd_keypress('VolumeMute'))
        btn_pwr.clicked.connect(lambda: self.roku.cmd_keypress('Power'))
        btn_vol_down.clicked.connect(lambda: self.__change_volume(False))
        btn_vol_up.clicked.connect(lambda: self.__change_volume(True))
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
        btn_spotify.clicked.connect(lambda: self.roku.cmd_content('19977'))
        btn_computer.clicked.connect(lambda: self.roku.cmd_keypress('InputHDMI3'))
        btn_playstation.clicked.connect(lambda: self.roku.cmd_keypress('InputHDMI2'))
        btn_chromecast.clicked.connect(lambda: self.roku.cmd_keypress('InputHDMI1'))

        self.layout.addWidget(btn_mute, 0, 0)
        self.layout.addWidget(btn_pwr, 0, 2)
        self.layout.addWidget(btn_vol_down, 1, 0)
        self.layout.addWidget(btn_vol_up, 1, 2)
        self.layout.addWidget(spinbox_vol_interval, 1, 1)

        # slider_vol = QSlider()
        # slider_vol.

        self.layout.addWidget(btn_back, 3, 0)
        self.layout.addWidget(btn_home, 3, 2)
        self.layout.addWidget(btn_arrow_up, 4, 1)
        self.layout.addWidget(btn_arrow_down, 6, 1)
        self.layout.addWidget(btn_arrow_left, 5, 0)
        self.layout.addWidget(btn_arrow_right, 5, 2)
        self.layout.addWidget(btn_ok, 5, 1)
        self.layout.addWidget(btn_replay, 7, 0)
        self.layout.addWidget(btn_no_disturb, 7, 1)
        self.layout.addWidget(btn_details, 7, 2)
        self.layout.addWidget(btn_rew, 8, 0)
        self.layout.addWidget(btn_play_pause, 7, 1)
        self.layout.addWidget(btn_fwd, 8, 2)
        self.layout.addWidget(btn_netflix, 9, 0)
        self.layout.addWidget(btn_hulu, 9, 2)
        self.layout.addWidget(btn_showtime, 10, 2)
        self.layout.addWidget(btn_spotify, 10, 1)
        self.layout.addWidget(btn_youtube, 10, 0)
        self.layout.addWidget(btn_computer, 11, 0)
        self.layout.addWidget(btn_playstation, 11, 1)
        self.layout.addWidget(btn_chromecast, 11, 2)

        btn_settings = QPushButton('⚙')
        btn_settings.clicked.connect(lambda: self.set_display_settings(True))
        self.layout.addWidget(btn_settings, 17, 1)

        qApp.installEventFilter(self)

    def focus(self):
        self.setWindowState(self.windowState() & ~QtCore.Qt.WindowMinimized | QtCore.Qt.WindowActive)
        self.activateWindow()
