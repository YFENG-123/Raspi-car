import schema


class Virtual_controler:
    def __init__(self):
        self.holder_control = [0, 0]

    def set_data(self, data: schema.Virtual_controler_data):
        self.holder_control = data.holder_control

    def get_holder_control(self):
        return self.holder_control
