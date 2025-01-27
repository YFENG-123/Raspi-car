# 软件 I2C（使用 bit-banging）适用于所有具有输出功能的引脚，并通过machine.SoftI2C类访问：
# machine.SoftI2C http://micropython.com.cn/en/latet/library/machine.I2C.html#machine-softi2c


from machine import Pin, SoftI2C

i2c = SoftI2C(scl=Pin(5), sda=Pin(4), freq=100_000)

i2c.scan()              # scan for devices

i2c.readfrom(0x3a, 4)   # read 4 bytes from device with address 0x3a
i2c.writeto(0x3a, '12') # write '12' to device with address 0x3a

buf = bytearray(10)     # create a buffer with 10 bytes
i2c.writeto(0x3a, buf)  # write the given buffer to the peripheral