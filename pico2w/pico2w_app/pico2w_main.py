import machine
import time
from pico2w_uart import Uart
from pico2w_holder import Holder

class APP:
    def __init__(self):
        self.holder = Holder() # 初始化云台
        self.uart = Uart() # 初始化UART
        self.uart.irq(self._uart_interrupted) # 监听UART
        #self.last_time = time.time_ns() # 记录时间
        #self.time = 0 # 记录时间

    def _uart_interrupted(self,uart_info):
        '''
        # 计算两次中断时间差
        self.time = time.time_ns()
        print("time:", self.time)
        print("time:", self.time - self.last_time)
        self.last_time = self.time
        '''

        #print("uart_info", uart_info)
        data = self.uart.readline()
        #print("data:", data)
        data_format = str(data)[2:-1]
        #print("data_format:",data_format)
        self.holder.readMove(data_format)
        self.holder.update()

    def run(self):
        while True:
            pass


if __name__ == "__main__":
    app = APP()
    app.run()