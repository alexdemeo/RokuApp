from util.constants import DEFAULT_KEYBOARD_ENABLED


class KeyListener:
    def __init__(self, cfg, roku):
        self.key_map = dict()
        self.roku = roku
        self.enabled = DEFAULT_KEYBOARD_ENABLED
        config = open(cfg, "r")
        for line in config:
            if ":" in line:
                parts = line.split(":")
                self.key_map[parts[1][:-1]] = parts[0]

        print("Key mappings are:")
        for key in self.key_map:
            print("\t" + self.format_mapping(key))
        print()

    def format_mapping(self, btn):
        return btn + " –> " + self.key_map[btn]

    def toggle_enabled(self):
        self.enabled = not self.enabled
        print('Keyboard ' + ('enabled' if self.enabled else 'disabled'))

    def on_press(self, btn):
        if not self.enabled:
            return False

        if btn == "Esc":
            return exit(0)
        if btn in self.key_map:
            self.roku.cmd_keypress(self.key_map[btn])
            return True
        else:
            print("Unrecognized key " + btn)
            return False
