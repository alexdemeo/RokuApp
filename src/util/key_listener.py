import json
import urllib.parse

from PyQt5.QtGui import QKeySequence


class KeyListener:
    def __init__(self, cfg, roku):
        self.key_map = dict()
        self.roku = roku
        key_cfg = open(cfg, "r")
        self.key_map = {v: k for k, v in json.load(key_cfg).items()}
        # print("Key mappings are:")

        self.key_map["Space"] = 'Lit_%20'
        for key in self.key_map:
            print("\t" + key + " –> " + self.key_map[key])

        self.ascii_map = dict()
        for e in [x for x in range(0, 255)]:  # A to z
            self.ascii_map[e] = "Lit_" + urllib.parse.quote(chr(e))
            # print("\t" + str(e) + " –> " + "Lit_" + urllib.parse.quote(chr(e)))
        print()

    def on_press(self, btn):
        btn_str = QKeySequence(btn).toString()
        if not self.roku.settings.get_keyboard_enabled():
            return False
        if btn_str in self.key_map:
            self.roku.cmd_keypress(self.key_map[btn_str])
            return True
        elif btn in self.ascii_map:
            self.roku.cmd_keypress(self.ascii_map[btn])
            return True
        else:
            print("No mapping for key: " + str(btn))
            return False
