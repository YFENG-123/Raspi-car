"""
引入库文件
"""
from app.app_gui import PygameGUI
from app.app_holder_device import Holder
from app.app_controler import Controler

# 引入 pygame 相关库
import pygame
import pygame.camera
from pygame.locals import *  # noqa: F403


class APP:
    
    def __init__(self):
        self.gui = PygameGUI()
        self.holder = Holder()
        pygame.time.set_timer(pygame.USEREVENT, 500)  # 配置定时器
        self.Joysticks = {}

    def run(self):
        while True:
            self.gui.update()
            self._event()
            """# 键盘控制移动方式
            keys = pygame.key.get_pressed()  # 轮询取按键方式
            if keys[pygame.K_w]:
                vertical_location -= 0.1
                print("vertical_location:" + str(vertical_location))
            if keys[pygame.K_s]:
                vertical_location += 0.1
                print("vertical_location:" + str(vertical_location))
            if keys[pygame.K_a]:
                horizon_location += 0.1
                print("horizon_location:" + str(horizon_location))
            if keys[pygame.K_d]:
                horizon_location -= 0.1
                print("horizon_location:" + str(horizon_location))"""

    def _event(self):
        for event in pygame.event.get():  # 列表方式
            '''
            窗口关闭方式
            '''
            if event.type == pygame.QUIT:  # 窗口关闭方式
                pygame.quit()
                break
            if event.type == pygame.KEYDOWN:  # 列表按键方式
                if event.mod & pygame.KMOD_LSHIFT:  # 列表取修饰键方式
                    if event.key == pygame.K_ESCAPE:  # 列表取键盘方式
                        pygame.quit()
                        break
            
            '''
            热插拔手柄
            '''
            if event.type == pygame.JOYDEVICEADDED:
                self.joystick = Controler(event.device_index)  # 创建手柄控制对象
                self.Joysticks[self.joystick.get_id()] = self.joystick  # 添加到字典中
                print("手柄【" + str(event.device_index) + "】已连接")
            if event.type == pygame.JOYDEVICEREMOVED:
                del self.Joysticks[event.instance_id]  # 删除字典中手柄对象
                print("手柄【" + str(event.instance_id) + "】已断开")

            '''
            手柄读取
            '''
            if event.type == pygame.JOYAXISMOTION:
                #self.joystick = self.Joysticks[event.instance_id]
                print(str(self.joystick.get_id())+ str(self.joystick.get_joystick_data()))


            '''
            鼠标控制读取
            '''
            if event.type == pygame.MOUSEMOTION:  # 鼠标移动
                #print(event)
                pass

            '''
            键盘读取
            '''
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    mouse_visible = not self.mouse_visible
                    mouse_grab = not self.mouse_grab
                    pygame.mouse.set_visible(mouse_visible)  # 隐藏鼠标
                    pygame.event.set_grab(mouse_grab)  # 锁定鼠标
                if event.key == pygame.K_w:
                    self.holder.turn_up()
                if event.key == pygame.K_s:
                    self.holder.turn_down()
                if event.key == pygame.K_a:
                    self.holder.turn_left()
                if event.key == pygame.K_d:
                    self.holder.turn_right()

    def stop():
        pass





if __name__ == "__main__":
    app = APP()
    app.run()
