from PyQt5 import QtCore
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import *

from ui.settings_panel import SettingsPanel


class Remote(QMainWindow):

    def __init__(self, roku, title, width, height):
        super().__init__(None)
        self.roku = roku
        self.__init_ui(title, width, height)
        self.settings_panel = SettingsPanel(roku.settings)

    def __init_ui(self, title, min_width, min_height):
        self.setMinimumSize(min_width, min_height)
        self.setWindowTitle(title)
        layout = QGridLayout()
        self.create_grid_layout(layout)

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
        btn_settings = QPushButton('⚙')
        checkbox_enable_keyboard = QCheckBox('Enable keyboard')

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
        btn_rew.clicked.connect(lambda: self.roku.cmd_keypress('Rew'))
        btn_fwd.clicked.connect(lambda: self.roku.cmd_keypress('Fwd'))

        btn_netflix.clicked.connect(lambda: self.roku.cmd_content('12'))
        btn_hulu.clicked.connect(lambda: self.roku.cmd_content('2285'))
        btn_showtime.clicked.connect(lambda: self.roku.cmd_content('8838'))
        btn_youtube.clicked.connect(lambda: self.roku.cmd_content('837'))
        btn_settings.clicked.connect(self.display_settings)
        checkbox_enable_keyboard.stateChanged.connect(self.toggle_keyboard)

        layout.addWidget(btn_mute, 0, 0)
        layout.addWidget(btn_pwr, 0, 2)
        layout.addWidget(btn_vol_down, 1, 0)
        layout.addWidget(btn_vol_up, 1, 2)
        layout.addWidget(btn_back, 2, 0)
        layout.addWidget(btn_home, 2, 2)
        layout.addWidget(btn_arrow_up, 3, 1)
        layout.addWidget(btn_arrow_down, 5, 1)
        layout.addWidget(btn_arrow_left, 4, 0)
        layout.addWidget(btn_arrow_right, 4, 2)
        layout.addWidget(btn_ok, 4, 1)
        layout.addWidget(btn_replay, 6, 0)
        layout.addWidget(btn_no_disturb, 6, 1)
        layout.addWidget(btn_details, 6, 2)
        layout.addWidget(btn_rew, 7, 0)
        layout.addWidget(btn_play_pause, 7, 1)
        layout.addWidget(btn_fwd, 7, 2)
        layout.addWidget(btn_netflix, 8, 0)
        layout.addWidget(btn_hulu, 8, 2)
        layout.addWidget(btn_showtime, 9, 2)
        layout.addWidget(btn_youtube, 9, 0)
        layout.addWidget(btn_settings, 10, 1)
        layout.addWidget(checkbox_enable_keyboard, 0, 1)

        # self.setFixedSize(self.size())
        qApp.installEventFilter(self)

    def display_settings(self):
        self.settings_panel.show()

    def toggle_keyboard(self):
        self.listener.toggle_enabled()
        self.centralWidget().clearFocus()

    def create_grid_layout(self, layout):
        w = QWidget(self)
        self.setCentralWidget(w)
        w.setLayout(layout)

    def eventFilter(self, source, event):
        if not self.roku.key_listener.enabled:
            return False
        if event.type() == QtCore.QEvent.KeyPress:
            key_str = QKeySequence(event.key()).toString()
            if self.roku.key_listener.on_press(key_str):
                self.statusBar().showMessage(self.listener.format_mapping(key_str))
                return True
        return super(Remote, self).eventFilter(source, event)
