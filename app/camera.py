import pygame
import pygame.camera


class PygameCamera:
    def __init__(self):
        pygame.camera.init()
        print("初始化摄像头...")
        self.camera_list = pygame.camera.list_cameras()  # 摄像头列表
        print("摄像头列表:", self.camera_list)
        print("启动摄像头:", self.camera_list[0])
        self.camera = pygame.camera.Camera(
            self.camera_list[0], (720, 640)
        )  # 获取/注册摄像头
        self.camera.start()  # 启动摄像头
        print("摄像头启动成功")
        print("摄像头分辨率:", self.camera.get_size())

    def get_image(self):
        return self.camera.get_image()
