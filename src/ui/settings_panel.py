from PyQt5 import QtCore
from PyQt5.QtCore import QEvent
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel, QLineEdit, QPushButton


class SettingsPanel(QWidget):
    def __init__(self, settings):
        super(SettingsPanel, self).__init__(flags=QtCore.Qt.Dialog)
        self.settings = settings
        self.__init_ui()

    def __init_ui(self):
        layout = QGridLayout()
        self.setLayout(layout)

        text_ip = QLineEdit()
        lbl_ip = QLabel('Roku IP: ')
        btn_done = QPushButton('Done')

        text_ip.setText(self.settings.get_ip())

        btn_done.clicked.connect(self.close_panel)
        text_ip.textChanged.connect(self.text_ip_edit_done)

        layout.addWidget(lbl_ip, 0, 0)
        layout.addWidget(text_ip, 0, 1)
        layout.addWidget(btn_done, 1, 1)

    def text_ip_edit_done(self, text):
        self.settings.set_ip(text)

    def close_panel(self):
        self.settings.flush_to_file()
        self.close()

    def eventFilter(self, source, event):
        if event.type() == QEvent.KeyPress:
            if not self.roku.settings.get_keyboard_enabled():
                return False
            key_str = QKeySequence(event.key()).toString()
        return super(SettingsPanel, self).eventFilter(source, event)
