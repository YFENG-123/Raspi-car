from machine import Pin, PWM
import time

# create PWM object from a pin and set the frequency of slice 0
# and duty cycle for channel A
pwm2 = PWM(Pin(2), freq=50, duty_u16=0)
pwm2.freq()  # get the current frequency of slice 0
pwm2.freq(50)  # set/change the frequency of slice 0
pwm2.duty_u16()  # get the current duty cycle of channel A, range 0-65535
pwm2.duty_u16(int(65535 * 7.5 / 100))  # set the duty cycle of channel A, range 0-65535
# pwm12.duty_u16(0)        # stop the output at channel A
print(pwm2)  # show the properties of the PWM object.
# pwm0.deinit()           # turn off PWM of slice 0, stopping channels A and B
for i in range(int(2.5 / 0.5), int(13.5 / 0.5), int(0.5 / 0.5)):
    pwm2.duty_u16(int(65535 * i * 0.5 / 100))
    print(i)
    time.sleep(1)
