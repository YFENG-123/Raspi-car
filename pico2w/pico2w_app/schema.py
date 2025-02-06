class Joystick_data:
    def __init__(self):
        self.position: list = [0, 0, 0, 0, -1, -1]
        self.hat: list = [0, 0]
        self.buttons: list = []

    def load_data(self, joystick_data):
        self.load_position_data(position_data=joystick_data.get("position"))
        self.load_hat_data(hat_data=joystick_data.get("hat"))
        self.load_buttons_data(buttons_data=joystick_data.get("buttons"))

    def load_position_data(self, position_data):
        if isinstance(position_data, list) and len(position_data) == 6:
            self.position = position_data
        else:
            self.position = [0, 0, 0, 0, -1, -1]
            raise Exception("position data error")

    def load_hat_data(self, hat_data):
        if isinstance(hat_data, list) and len(hat_data) == 2:
            self.hat = hat_data
        else:
            self.hat = [0, 0]
            raise Exception("hat data error")

    def load_buttons_data(self, buttons_data):
        if isinstance(buttons_data, list):
            self.buttons = buttons_data
        else:
            self.buttons = []
            raise Exception("buttons data error")


class Mouse_data:
    def __init__(self):
        self.relative: list = [0, 0]
        self.buttons: list = []
        self.whell: int = 0

    def load_data(self, mouse_data):
        self.load_relative_data(relative_data=mouse_data.get("relative"))
        self.load_whell_data(whell_data=mouse_data.get("whell"))
        self.load_buttons_data(buttons_data=mouse_data.get("buttons"))

    def load_relative_data(self, relative_data):
        if isinstance(relative_data, list) and len(relative_data) == 2:
            self.relative = relative_data
        else:
            self.relative = [0, 0]
            raise Exception("relative data error")

    def load_whell_data(self, whell_data):
        if isinstance(whell_data, int):
            self.whell = whell_data
        else:
            self.whell = 0
            raise Exception("whell data error")

    def load_buttons_data(self, buttons_data):
        if isinstance(buttons_data, list):
            self.buttons = buttons_data
        else:
            self.buttons = []
            raise Exception("buttons data error")


class Keyboard_data:
    def __init__(self):
        self.keys: list = []

    def load_data(self, keyboard_data: dict):
        self.load_keys_data(keys_data=keyboard_data.get("keys"))

    def load_keys_data(self, keys_data):
        if isinstance(keys_data, list):
            self.keys = keys_data
        else:
            self.keys = []
            raise Exception("keys data error")


class Json_data:
    def __init__(self):
        self.mouse_data: Mouse_data = Mouse_data()
        self.joystick_data: Mouse_data | None = Joystick_data()
        self.keyboard_data: Keyboard_data = Keyboard_data()

    def load_data(self, json_data: dict):
        self.load_joystick_data(joystick_data=json_data.get("joystick"))
        self.load_mouse_data(mouse_data=json_data.get("mouse"))
        self.load_keyboard_data(keyboard_data=json_data.get("keyboard"))

    def load_joystick_data(self, joystick_data):
        if isinstance(joystick_data, dict):
            self.joystick_data.load_data(joystick_data=joystick_data)
        else:
            raise Exception("joystick data error")

    def load_mouse_data(self, mouse_data: dict):
        if isinstance(mouse_data, dict):
            self.mouse_data.load_data(mouse_data=mouse_data)
        else:
            raise Exception("mouse data error")

    def load_keyboard_data(self, keyboard_data: dict):
        if isinstance(keyboard_data, dict):
            self.keyboard_data.load_data(keyboard_data=keyboard_data)
        else:
            raise Exception("keyboard data error")
