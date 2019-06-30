import subprocess
import sys

from PyQt5.QtWidgets import QApplication

from key_listener import KeyListener
from remote import Remote
from constants import IP, CFG, TITLE, MIN_WIDTH, MIN_HEIGHT


class Roku:
    def __init__(self, ip):
        self.IP = ip
        print("Ready for IP: " + ip)

    def cmd(self, btn):
        command = "curl -d '' http://" + self.IP + ":8060/keypress/" + btn
        print(command)
        # subprocess.Popen(command.split(), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).communicate()


if __name__ == '__main__':
    roku = Roku(IP)
    listener = KeyListener(CFG, roku)
    app = QApplication(sys.argv)
    ui = Remote(listener, roku, TITLE, MIN_WIDTH, MIN_HEIGHT)
    ui.show()
    sys.exit(app.exec_())
