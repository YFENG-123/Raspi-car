import pico2w_schema


class Keyboard:
    def __init__(self):
        self.keys = []

    def set_data(self, data: pico2w_schema.Keyboard_data):
        self.keys = data.keys
