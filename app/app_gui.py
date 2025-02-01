import pygame
from app.app_camera_device import PygameCamera

class PygameGUI:
    def __init__(self):
        pygame.init()
        self.camera = PygameCamera()
        self.mouse_visible = False
        self.mouse_grab = True
        pygame.mouse.set_visible(self.mouse_visible)  # 隐藏鼠标
        pygame.event.set_grab(self.mouse_grab)  # 锁定鼠标
        self.display = pygame.display.set_mode((1280, 720))  # 设置窗口
        self.clock = pygame.time.Clock()  # 设置FPS

    def update(self):
        frame = self.camera.get_image()
        self.display.blit(frame, (0, 0))
        pygame.display.flip()
        self.clock.tick(60)  # 60 FPS
        
    def stop(self):
        pass