import distutils

CFG = 'res/config.txt'

class Settings:
    def __init__(self):
        self.mapping = self.build_map_from_file()

    def get_ip(self):
        return str(self.mapping['IP'])

    def set_ip(self, ip):
        self.mapping['IP'] = str(ip)

    def get_title(self):
        return str(self.mapping['TITLE'])

    def set_title(self, title):
        self.mapping['TITLE'] = title

    def get_min_width(self):
        return int(self.mapping['MIN_WIDTH'])

    def set_min_width(self, min_width):
        self.mapping['MIN_WIDTH'] = min_width

    def get_min_height(self):
        return int(self.mapping['MIN_HEIGHT'])

    def set_min_height(self, min_height):
        self.mapping['MIN_HEIGHT'] = min_height

    def get_keyboard_enabled(self):
        return self.mapping['KEYBOARD_ENABLED'] == 'True'

    def toggle_keyboard_enabled(self):
        self.mapping['KEYBOARD_ENABLED'] = 'False' if self.mapping['KEYBOARD_ENABLED'] == 'True' else 'True'

    def flush_to_file(self):
        file = open(CFG, 'w')
        for key, value in self.mapping.items():
            file.write(key + '=' + value + '\n')

    @staticmethod
    def build_map_from_file():
        mapping = {}
        config = open(CFG, 'r')
        for line in config:
            if "=" in line:
                parts = line.split("=")
                mapping[parts[0]] = parts[1][:-1]
        print(mapping)
        return mapping
