import json

CFG = 'res/config.json'


class Settings:
    def __init__(self):
        self.mapping = {}
        file = open(CFG, 'r')
        config = json.load(file)
        for k, v in config.items():
            self.mapping[k] = v
        print(config)

    def get_ip(self):
        return self.mapping['ip']

    def set_ip(self, ip):
        self.mapping['ip'] = str(ip)

    def get_title(self):
        return self.mapping['title']

    def set_title(self, title):
        self.mapping['title'] = title

    def get_min_width(self):
        return self.mapping['min_width']

    def set_min_width(self, min_width):
        self.mapping['min_width'] = min_width

    def get_min_height(self):
        return int(self.mapping['min_height'])

    def set_min_height(self, min_height):
        self.mapping['min_height'] = min_height

    def get_keyboard_enabled(self):
        return self.mapping['keyboard_enabled']

    def toggle_keyboard_enabled(self):
        self.mapping['keyboard_enabled'] = not self.mapping['keyboard_enabled']

    def flush_to_file(self):
        file = open(CFG, 'w')
        json.dump(self.mapping, file)
        print('Flushed config.json to file for contents: ' + str(self.mapping))
