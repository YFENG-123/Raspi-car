from pydantic import BaseModel  # 引入pydantic用于辅助构建数据，打包json


class Mouse(BaseModel):
    relative: list = [0, 0]
    buttons: list = []
    whell: int = 0


class Joystick(BaseModel):
    position: list = [0, 0, 0, 0, -1, -1]
    hat: list = [0, 0]
    buttons: list = []


class Keyboard(BaseModel):
    keys: list = []


class Virtual_controler(BaseModel):
    holder_control: list = [0, 0]


class Json_buffer(BaseModel):
    mouse: Mouse = Mouse()
    joystick: Joystick | None = Joystick()
    keyboard: Keyboard = Keyboard()
    virtual_controler: Virtual_controler = Virtual_controler()


if __name__ == "__main__":
    print(Json_buffer().model_dump_json())
    {
        "mouse": {
            "relative": [0, 0],
            "button": [],
            "whell_up": 0,
        },
        "joystick": {"position": [0, 0, 0, 0, -1, -1], "hat": [0, 0], "button": []},
        "keyboard": [],
    }
