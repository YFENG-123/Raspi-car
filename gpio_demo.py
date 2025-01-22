from gpiozero import PWMOutputDevice
from time import sleep
from signal import pause

frequency = 50
initial_value = 0.0 / 100
P14 = PWMOutputDevice(14,active_high=True,initial_value = initial_value,frequency=frequency)

P14.value = 7.5 / 100

pause()