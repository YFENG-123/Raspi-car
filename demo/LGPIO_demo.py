from gpiozero.pins.lgpio import LGPIOFactory
from gpiozero import PWMOutputDevice

from signal import pause

factory = LGPIOFactory(chip=0)

frequency = 50
initial_rate = 7.5
P14 = PWMOutputDevice(
    14,
    active_high=True,
    initial_value=initial_rate / 100,
    frequency=frequency,
    pin_factory=factory,
)
P15 = PWMOutputDevice(
    15,
    active_high=True,
    initial_value=initial_rate / 100,
    frequency=frequency,
    pin_factory=factory,
)

P14.value = 7.5 / 100
P15.value = 7.5 / 100
pause()
