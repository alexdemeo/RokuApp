import sys

from PyQt5.QtWidgets import QApplication

from util.key_listener import KeyListener
from ui.remote import Remote
from util.constants import ALEXS_IP, CFG, TITLE, MIN_WIDTH, MIN_HEIGHT
from util.settings import Settings


class Roku:
    def __init__(self, ip):
        self.app = QApplication(sys.argv)
        self.key_listener = KeyListener(CFG, self)
        self.ui = Remote(self.key_listener, self, TITLE, MIN_WIDTH, MIN_HEIGHT, None)
        self.settings = Settings(ALEXS_IP)
        print("Ready for IP: " + ip)

    def start(self):
        self.ui.show()
        return self.app.exec_()

    def cmd(self, btn):
        command = "curl -d '' http://" + self.settings.get_ip() + ":8060/keypress/" + btn
        print(command)
        # subprocess.Popen(command.split(), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).communicate()


if __name__ == '__main__':
    roku = Roku(ALEXS_IP)
    sys.exit(roku.start())
