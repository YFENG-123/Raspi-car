import schema


class Joystick:
    def __init__(self):
        self.position = [0, 0, 0, 0, -1, -1]
        self.hat = [0, 0]
        self.button = []

    def set_data(self, data:schema.Joystick_data):
        self.position = data.position
        self.hat = data.hat
        self.button = data.buttons
        self.eliminate_dead_zone()

    def eliminate_dead_zone(self):
        for i in range(4):
            if abs(self.position[i]) < 0.075:
                self.position[i] = 0

    def get_left_axis(self):
        return self.position[0], self.position[1]

    def get_right_axis(self):
        return self.position[2], self.position[3]

    def get_trigger(self):
        return self.position[4], self.position[5]
