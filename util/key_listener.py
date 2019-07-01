class KeyListener:
    def __init__(self, cfg, roku):
        self.key_map = dict()
        self.roku = roku
        key_cfg = open(cfg, "r")
        for line in key_cfg:
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
        self.roku.settings.toggle_keyboard_enabled()
        print('Keyboard ' + ('enabled' if self.roku.settings.get_keyboard_enabled() else 'disabled'))

    def on_press(self, btn):
        if not self.roku.settings.get_keyboard_enabled():
            return False

        if btn == "Esc":
            return exit(0)
        if btn in self.key_map:
            self.roku.cmd_keypress(self.key_map[btn])
            return True
        else:
            print("Unrecognized key " + btn)
            return False
