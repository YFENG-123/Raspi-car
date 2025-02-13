import pygame


class PygameGUI:
    def __init__(self):
        pygame.init()  # 初始化pygame
        self.mouse_visible = False  # 鼠标是否可见
        self.mouse_grab = True  # 鼠标是否锁定
        pygame.mouse.set_visible(self.mouse_visible)  # 隐藏鼠标
        pygame.event.set_grab(self.mouse_grab)  # 锁定鼠标
        self.display = pygame.display.set_mode((1280, 720))  # 设置窗口

    def update(self, frame):
        self.display.blit(frame, (0, 0))  # 显示摄像头图像
        pygame.display.flip()  # 更新显示

    def stop(self):
        pass
