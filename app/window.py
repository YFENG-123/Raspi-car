import cv2
import pygame


class Window:
    def __init__(self):
        pygame.init()  # 初始化pygame
        self.display = pygame.display.set_mode((1280, 720))  # 设置窗口

    def update(self, frame):
        frame_transpose = cv2.transpose(frame) # 转置图像
        frame = pygame.surfarray.make_surface(frame_transpose) # 转换为pygame.surfarray格式
        self.display.blit(frame, (0, 0))  # 显示摄像头图像
        pygame.display.flip()  # 更新显示

    def stop(self):
        pass
