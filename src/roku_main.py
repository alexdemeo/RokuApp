import subprocess
import sys

from PyQt5.QtWidgets import QApplication
from src.ui.remote import Remote
from src.ui.warning import show_warning
from src.util.key_listener import KeyListener
from src.util.settings import Settings


class Roku:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.settings = Settings()
        self.key_listener = KeyListener('res/key_cfg.json', self)
        self.ui = Remote(self)
        print("Ready for IP: " + self.settings.get_ip())

    def start(self):
        self.ui.show()
        return self.app.exec_()

    def __shell(self, command):
        print(command)
        try:
            subprocess.check_output(command.split(), stderr=subprocess.DEVNULL,
                                    timeout=self.settings.get_error_timeout())
        except subprocess.TimeoutExpired:
            show_warning(self.settings, "An error occurred communicating with " + self.settings.get_ip(),
                         "Make sure this is your Roku's IP address and that device is on the same WiFi network (or "
                         "try again)")

    def cmd_keypress(self, btn):
        command = "curl -d '' http://" + self.settings.get_ip() + ":8060/keypress/" + btn
        self.__shell(command)

    def cmd_content(self, content_id):
        command = "curl -d '' http://" + self.settings.get_ip() + ":8060/launch/" + content_id
        self.__shell(command)


if __name__ == '__main__':
    roku = Roku()
    sys.exit(roku.start())
