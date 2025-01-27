# 有两个 UART，UART0 和 UART1。UART0 可以映射到 GPIO 0/1、12/13 和 16/17，UART1 可以映射到 GPIO 4/5 和 8/9。
# 参见http://micropython.com.cn/en/latet/library/machine.UART.html#machine-uart
# 认情况下禁用通过 UART 的 REPL。您可以在RP2xxx 上查看MicroPython 入门以了解有关如何通过 UART 启用 REPL 的详细信息。
# RP2xxx 上查看MicroPython 入门 http://micropython.com.cn/en/latet/rp2/tutorial/intro.html#rp2-intro
from machine import UART, Pin
uart1 = UART(1, baudrate=9600, tx=Pin(4), rx=Pin(5))
uart1.write('hello')  # write 5 bytes
uart1.read(5)         # read up to 5 bytes