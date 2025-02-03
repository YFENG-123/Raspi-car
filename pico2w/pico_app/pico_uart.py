import machine
import time


class Uart(machine.UART):
    def __init__(self):
        pin0 = machine.Pin(0)
        pin1 = machine.Pin(1)
        super().__init__(
            0,
            tx=pin0,
            rx=pin1,
            baudrate=4000000,
            # parity=0,
            # stop=2,
            bits=8,
            timeout=0,
            timeout_char=0,
        )

    def interrupted(self, uart_info):
        print("uart_info", uart_info)
        data = self.readline()
        print("data:", data)

    def irq(self, handler=interrupted, trigger=machine.UART.IRQ_RXIDLE, hard=False):
        super().irq(handler=handler, trigger=trigger, hard=hard)


if __name__ == "__main__":
    uart = Uart()

    def interrupted(uart_info):
        # print("uart_info", uart_info)
        data = uart.readline()
        print("data:", data)

    uart.irq(interrupted)
    while True:
        pass
