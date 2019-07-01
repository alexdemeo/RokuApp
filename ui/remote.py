from PyQt5 import QtCore
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import *

from ui.settings_panel import SettingsPanel


class Remote(QMainWindow):

    def __init__(self, roku):
        super().__init__()
        self.roku = roku
        self.__init_ui(roku.settings.get_title(), roku.settings.get_min_width(), roku.settings.get_min_height())
        self.settings_panel = SettingsPanel(roku.settings)
        self.__init_settings()

    def __init_settings(self):
        # print(self.roku.settings.get_keyboard_enabled())
        self.checkbox_enable_keyboard.setChecked(self.roku.settings.get_keyboard_enabled())

    def __init_ui(self, title, min_width, min_height):
        self.setMinimumSize(min_width, min_height)
        self.setWindowTitle(title)
        layout = QGridLayout()
        self.create_grid_layout(layout)

        self.btn_mute = QPushButton('🔇')
        self.btn_pwr = QPushButton('🔌')
        self.btn_vol_down = QPushButton('−')
        self.btn_vol_up = QPushButton('＋')
        self.btn_back = QPushButton('↲')
        self.btn_home = QPushButton('⌂')
        self.btn_arrow_down = QPushButton('↓')
        self.btn_arrow_up = QPushButton('↑')
        self.btn_arrow_left = QPushButton('←')
        self.btn_arrow_right = QPushButton('→')
        self.btn_ok = QPushButton('OK')
        self.btn_replay = QPushButton('⟲')
        self.btn_no_disturb = QPushButton('🌙')
        self.btn_details = QPushButton('✱')
        self.btn_rew = QPushButton('⏪')
        self.btn_play_pause = QPushButton('⏯')
        self.btn_fwd = QPushButton('⏩')
        self.btn_netflix = QPushButton('Netflix')
        self.btn_hulu = QPushButton('Hulu')
        self.btn_showtime = QPushButton('Showtime')
        self.btn_youtube = QPushButton('YouTube')
        self.btn_settings = QPushButton('⚙')
        self.checkbox_enable_keyboard = QCheckBox('Enable keyboard')

        self.btn_mute.clicked.connect(lambda: self.roku.cmd_keypress('VolumeMute'))
        self.btn_pwr.clicked.connect(lambda: self.roku.cmd_keypress('Power'))
        self.btn_vol_down.clicked.connect(lambda: self.roku.cmd_keypress('VolumeDown'))
        self.btn_vol_up.clicked.connect(lambda: self.roku.cmd_keypress('VolumeUp'))
        self.btn_back.clicked.connect(lambda: self.roku.cmd_keypress('Back'))
        self.btn_home.clicked.connect(lambda: self.roku.cmd_keypress('Home'))
        self.btn_arrow_down.clicked.connect(lambda: self.roku.cmd_keypress('Down'))
        self.btn_arrow_up.clicked.connect(lambda: self.roku.cmd_keypress('Up'))
        self.btn_arrow_left.clicked.connect(lambda: self.roku.cmd_keypress('Left'))
        self.btn_arrow_right.clicked.connect(lambda: self.roku.cmd_keypress('Right'))
        self.btn_ok.clicked.connect(lambda: self.roku.cmd_keypress('Select'))
        self.btn_replay.clicked.connect(lambda: self.roku.cmd_keypress('InstantReplay'))
        self.btn_no_disturb.clicked.connect(lambda: self.roku.cmd_keypress('?'))
        self.btn_details.clicked.connect(lambda: self.roku.cmd_keypress('Info'))
        self.btn_rew.clicked.connect(lambda: self.roku.cmd_keypress('Rew'))
        self.btn_fwd.clicked.connect(lambda: self.roku.cmd_keypress('Fwd'))

        self.btn_netflix.clicked.connect(lambda: self.roku.cmd_content('12'))
        self.btn_hulu.clicked.connect(lambda: self.roku.cmd_content('2285'))
        self.btn_showtime.clicked.connect(lambda: self.roku.cmd_content('8838'))
        self.btn_youtube.clicked.connect(lambda: self.roku.cmd_content('837'))
        self.btn_settings.clicked.connect(lambda: self.set_display_settings(True))
        self.checkbox_enable_keyboard.stateChanged.connect(self.toggle_keyboard)

        layout.addWidget(self.btn_mute, 0, 0)
        layout.addWidget(self.btn_pwr, 0, 2)
        layout.addWidget(self.btn_vol_down, 1, 0)
        layout.addWidget(self.btn_vol_up, 1, 2)
        layout.addWidget(self.btn_back, 2, 0)
        layout.addWidget(self.btn_home, 2, 2)
        layout.addWidget(self.btn_arrow_up, 3, 1)
        layout.addWidget(self.btn_arrow_down, 5, 1)
        layout.addWidget(self.btn_arrow_left, 4, 0)
        layout.addWidget(self.btn_arrow_right, 4, 2)
        layout.addWidget(self.btn_ok, 4, 1)
        layout.addWidget(self.btn_replay, 6, 0)
        layout.addWidget(self.btn_no_disturb, 6, 1)
        layout.addWidget(self.btn_details, 6, 2)
        layout.addWidget(self.btn_rew, 7, 0)
        layout.addWidget(self.btn_play_pause, 7, 1)
        layout.addWidget(self.btn_fwd, 7, 2)
        layout.addWidget(self.btn_netflix, 8, 0)
        layout.addWidget(self.btn_hulu, 8, 2)
        layout.addWidget(self.btn_showtime, 9, 2)
        layout.addWidget(self.btn_youtube, 9, 0)
        layout.addWidget(self.btn_settings, 10, 1)
        layout.addWidget(self.checkbox_enable_keyboard, 0, 1)

        qApp.installEventFilter(self)

    def set_display_settings(self, flag):
        self.settings_panel.show() if flag else self.settings_panel.hide()

    def toggle_keyboard(self):
        self.roku.key_listener.toggle_enabled()
        self.centralWidget().clearFocus()

    def create_grid_layout(self, layout):
        w = QWidget(self)
        self.setCentralWidget(w)
        w.setLayout(layout)

    def eventFilter(self, source, event):
        if not self.roku.settings.get_keyboard_enabled():
            return False
        if event.type() == QtCore.QEvent.KeyPress:
            key_str = QKeySequence(event.key()).toString()
            if self.roku.key_listener.on_press(key_str):
                # self.statusBar().showMessage(self.roku.key_listener.format_mapping(key_str))
                return True
        return super(Remote, self).eventFilter(source, event)
