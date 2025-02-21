from gpiozero.pins.lgpio import LGPIOFactory
from gpiozero import PWMOutputDevice, DigitalOutputDevice
from gpiozero.pins.rpigpio import RPiGPIOFactory

import time
from signal import pause

factory = RPiGPIOFactory()

p20 = DigitalOutputDevice(20, pin_factory=factory)
p20.on()


frequency = 50
duty = 50


pwm13 = DigitalOutputDevice(13,pin_factory=factory)

while True:
    pwm13.on()
    time.sleep(0.3)
    pwm13.off()
    time.sleep(1)
