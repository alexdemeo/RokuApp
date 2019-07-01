from PyQt5 import QtCore
from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel, QLineEdit


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

        text_ip.setText(self.settings.get_ip())

        layout.addWidget(lbl_ip, 0, 0)
        layout.addWidget(text_ip, 0, 1)

        pass

