import machine

Pin0 = machine.Pin(0, machine.Pin.OUT)
Pin1 = machine.Pin(1, machine.Pin.IN)
uart = machine.UART(0, baudrate=115200, tx=Pin0, rx=Pin1)


def uart_interrupt_handler(data):
    uart.write("world")
    print(data)


uart.irq(uart_interrupt_handler)
while True:
    pass
