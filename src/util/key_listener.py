import json


class KeyListener:
    def __init__(self, cfg, roku):
        self.key_map = dict()
        self.roku = roku
        key_cfg = open(cfg, "r")
        self.key_map = {v: k for k, v in json.load(key_cfg).items()}
        print("Key mappings are:")
        for key in self.key_map:
            print("\t" + self.format_mapping(key))
        for e in range(0, 255):
            self.key_map[chr(e)] = "Lit_" + chr(e)
        self.key_map["Space"] = 'Lit_%20'
        print()

    def format_mapping(self, btn):
        return btn + " –> " + self.key_map[btn]

    def on_press(self, btn):
        if not self.roku.settings.get_keyboard_enabled():
            return False
        if btn == self.key_map["Exit"]:
            return exit(0)
        if btn in self.key_map:
            self.roku.cmd_keypress(self.key_map[btn])
            return True
        else:
            print("Unrecognized key " + btn)
            return False
