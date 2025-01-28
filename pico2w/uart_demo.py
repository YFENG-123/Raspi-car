from machine import UART, Pin
import rp2
import time
uart1 = UART(0, baudrate=115200, tx=Pin(0), rx=Pin(1))
uart1.write('hello')  # write 5 bytes
buf = uart1.read(5)         # read up to 5 bytes
print(buf)
while True:
    uart1.write('hello')  # write 5 bytes
    print(uart1.read(5)) # read up to 5 bytes
    time.sleep(1)