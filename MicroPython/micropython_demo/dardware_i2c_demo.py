# 驱动程序通过 machine.I2C类访问，并具有与上述软件 I2C 相同的方法：
# machine.I2C http://micropython.com.cn/en/latet/library/machine.I2C.html#machine-i2c

from machine import Pin, I2C

i2c = I2C(0)   # default assignment: scl=Pin(9), sda=Pin(8)
i2c = I2C(1, scl=Pin(3), sda=Pin(2), freq=400_000)