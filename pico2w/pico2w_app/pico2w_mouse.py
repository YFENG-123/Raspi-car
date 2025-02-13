import pico2w_schema


class Mouse:
    def __init__(self):
        self.relative = [0, 0]
        self.button = []
        self.whell = 0

    def set_data(self, data: pico2w_schema.Mouse_data):
        self.relative = data.relative
        self.button = data.buttons
        self.whell = data.whell

    def get_relative(self):
        return self.relative[0], self.relative[1]

    def get_button(self):
        return self.button

    def get_whell(self):
        return self.whell
