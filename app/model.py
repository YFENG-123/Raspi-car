import ultralytics
import threading
import cv2
import ultralytics.engine
import ultralytics.engine.results
import config

MODELPATH = "yolo11n.pt"


class Model:
    def __init__(self):
        """创建模型"""
        self.model = ultralytics.YOLO(MODELPATH)  # 创建模型
        """创建锁"""
        self.result_lock = threading.Lock()  # 创建结果锁
        self.frame_lock = threading.Lock()  # 创建帧锁
        """创建缓存变量"""
        self.frame: cv2.typing.MatLike = None  # 创建帧
        self.result = self.model.predict(source=None)[0]  # 创建结果缓存变量
        """创建线程"""
        self.is_predict_thread_running = True  # 创建预测线程运行标志
        self.is_track_thread_running = False  # 创建跟踪线程运行标志
        self.predict_thread = threading.Thread(
            target=self.predict_thread_func
        )  # 创建线程
        #self.predict_thread.start()  # 启动线程

    """线程函数"""

    def track_thread_func(self):
        while self.is_track_thread_running:
            self.frame_lock.acquire()
            frame = self.frame  # 获取一帧图像
            self.frame_lock.release()
            result = self.model.track(frame, persist=True)[0]  # 模型预测
            self.result_lock.acquire()
            self.result = result  # 将结果保存到self.result变量中
            self.result_lock.release()

    def predict_thread_func(self):
        while self.is_predict_thread_running:
            while config.tag == 1:
                pass
            self.frame_lock.acquire()
            frame = self.frame  # 获取一帧图像
            self.frame_lock.release()
            result = self.model.predict(frame)[0]  # 模型预测
            self.result_lock.acquire()
            self.result = result  # 将结果保存到self.result变量中
            self.result_lock.release()

    """线程管理函数"""

    def start_predict_thread(self):
        self.is_predict_thread_running = True
        self.predict_thread = threading.Thread(target=self.predict_thread_func)
        self.predict_thread.start()

    def stop_predict_thread(self):
        self.is_predict_thread_running = False
        self.predict_thread.join()

    def start_track_thread(self):
        self.is_track_thread_running = True
        self.track_thread = threading.Thread(target=self.track_thread_func)
        self.track_thread.start()

    def stop_track_thread(self):
        self.is_track_thread_running = False
        self.track_thread.join()

    """接口函数"""

    def set_frame(self, frame):  # 设置图像
        self.frame_lock.acquire()
        self.frame = frame
        self.frame_lock.release()

    def get_result(self) -> ultralytics.engine.results.Results:  # 获取结果
        self.result_lock.acquire()
        result = self.result
        self.result_lock.release()
        return result


if __name__ == "__main__":
    model = Model()  # 创建模型实例
    camera = cv2.VideoCapture(0)  # 创建摄像头实例
    model.start_predict_thread()  # 启动模型

    while True:
        _, frame = camera.read()
        # frame = cv2.flip(frame, -1)
        model.set_frame(frame)
        result = model.get_result()
        frame_with_box = result.plot()
        if frame is None:
            continue
        cv2.imshow("frame", frame)
        cv2.waitKey(1)
        if cv2.waitKey(1) & 0xFF == 27:
            model.stop_predict_thread()
            cv2.destroyAllWindows()
            break
