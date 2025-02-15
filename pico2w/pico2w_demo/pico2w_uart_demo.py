import machine
import rp2
import time

Pin0 = machine.Pin(0, machine.Pin.OUT)
Pin1 = machine.Pin(1, machine.Pin.IN)
uart = machine.UART(0, baudrate=115200, tx=Pin0, rx=Pin1, parity=0)


def uart_interrupt_handler(p):
    print(p)
    # state = machine.disable_irq()
    buf = uart.read()
    print(buf)  # read up to 5 bytes
    if buf is None:
        return
    uart.write(str(buf))  # write 5 bytes
    # machine.enable_irq(state)


# Pin1.irq(trigger = machine.Pin.IRQ_FALLING , handler = uart_interrupt_handler)

buffer = ""
while True:
    uart.write(b"hello")  # write 5 bytes

    b = uart.read(1)
    if b is None:
        continue
    elif b == b"\n":
        print(buffer)
        bufffer = ""
        continue
    else:
        bufffer += str(b)[2]
        # print(str(b)[2])

    # print(bufffer) # read up to 5 bytes
    # time.sleep(1)
    pass
