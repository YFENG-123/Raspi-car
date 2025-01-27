# RP2040 有 2 条硬件 SPI 总线，可通过 machine.SPI c类访问， 方法与上述软件 SPI 相同：
# machine.SPI http://micropython.com.cn/en/latet/library/machine.SPI.html#machine-spi

from machine import Pin, SPI

spi = SPI(1, 10_000_000)  # Default assignment: sck=Pin(10), mosi=Pin(11), miso=Pin(8)
spi = SPI(1, 10_000_000, sck=Pin(14), mosi=Pin(15), miso=Pin(12))
spi = SPI(0, baudrate=80_000_000, polarity=0, phase=0, bits=8, sck=Pin(6), mosi=Pin(7), miso=Pin(4))