import pygame
import pygame.camera
import cv2
import numpy 


class PygameCamera:
    '''废弃'''
    def __init__(self):
        pygame.camera.init()
        print("初始化摄像头...")
        self.camera_list = pygame.camera.list_cameras()  # 摄像头列表
        print("摄像头列表:", self.camera_list)
        print("启动摄像头:", self.camera_list[1])
        self.camera = pygame.camera.Camera(
            self.camera_list[0], (1280, 720)
        )  # 获取/注册摄像头
        self.camera.start()  # 启动摄像头
        print("摄像头启动成功")
        print("摄像头分辨率:", self.camera.get_size())

    def get_image(self):
        return self.camera.get_image()

class OpenCVCamera:
    def __init__(self):
        self.camera = cv2.VideoCapture(0)
        self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    def get_frame(self):
        ret, frame = self.camera.read() # 获取一帧
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) # 转换为RGB格式
        frame_rotated = cv2.rotate(frame_rgb, cv2.ROTATE_180) # 旋转图像
        return frame_rotated
