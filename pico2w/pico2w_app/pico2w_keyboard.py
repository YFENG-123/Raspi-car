import schema


class Keyboard:
    def __init__(self):
        self.keys = []

    def set_data(self, data: schema.Keyboard_data):
        self.keys = data.keys
