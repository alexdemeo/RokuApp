class Settings:
    def __init__(self, ip):
        self.__ip = ip

    def get_ip(self):
        return self.__ip

    def set_ip(self, ip):
        self.__ip = ip
