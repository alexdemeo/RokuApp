from PyQt5 import QtCore
from PyQt5.QtCore import QEvent
from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel, QLineEdit, QPushButton, QCheckBox

from src.util.settings import Settings


class SettingsPanel(QWidget):
    def __init__(self, settings):
        # type: (Settings) -> None
        super(SettingsPanel, self).__init__(flags=QtCore.Qt.Dialog)
        self.settings = settings
        self.__init_ui()

    def __init_ui(self):
        layout = QGridLayout()
        self.setLayout(layout)

        lbl_ip = QLabel('Roku IP: ')
        text_ip = QLineEdit()

        lbl_enable_keyboard = QLabel('Keyboard enabled:')
        checkbox_enable_keyboard = QCheckBox()

        lbl_spotify = QLabel('Spotify enabled: ')
        checkbox_spotify = QCheckBox()

        text_ip.setText(self.settings.get_ip())
        text_ip.textChanged.connect(self.text_ip_edit_done)

        checkbox_enable_keyboard.setChecked(self.settings.get_keyboard_enabled())
        checkbox_enable_keyboard.stateChanged.connect(
            lambda checked: self.settings.set_keyboard_enabled(checked == QtCore.Qt.Checked))

        checkbox_spotify.setChecked(self.settings.get_spotify_enabled())
        checkbox_spotify.stateChanged.connect(
            lambda checked: self.settings.set_spotify_enabled(checked == QtCore.Qt.Checked))

        layout.addWidget(lbl_ip, 0, 0)
        layout.addWidget(text_ip, 0, 1)

        layout.addWidget(lbl_enable_keyboard, 1, 0)
        layout.addWidget(checkbox_enable_keyboard, 1, 1)

        layout.addWidget(lbl_spotify, 2, 0)
        layout.addWidget(checkbox_spotify, 2, 1)

        btn_done = QPushButton('Done')
        btn_done.clicked.connect(self.close_panel)
        layout.addWidget(btn_done, 3, 1)

    def text_ip_edit_done(self, text):
        self.settings.set_ip(text)

    def close_panel(self):
        self.settings.flush_to_file()
        self.close()

    def eventFilter(self, source, event):
        if event.type() == QEvent.KeyPress:
            if not self.roku.settings.get_keyboard_enabled():
                return False
        return super(SettingsPanel, self).eventFilter(source, event)
