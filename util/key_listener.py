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
        print()

    def format_mapping(self, btn):
        return btn + " –> " + self.key_map[btn]

    def get_exit_button(self):
        return self.key_map["Exit"]

    def on_press(self, btn):
        if not self.roku.settings.get_keyboard_enabled():
            return False
        if btn == self.roku.key_listener.get_exit_button():
            return exit(0)
        if btn in self.key_map:
            self.roku.cmd_keypress(self.key_map[btn])
            return True
        else:
            print("Unrecognized key " + btn)
            return False
