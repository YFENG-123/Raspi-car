from machine import Pin, PWM

# create PWM object from a pin and set the frequency of slice 0
# and duty cycle for channel A
pwm12 = PWM(Pin(12), freq=2000, duty_u16=1024)
pwm12.freq()             # get the current frequency of slice 0
pwm12.freq(50)         # set/change the frequency of slice 0
pwm12.duty_u16()         # get the current duty cycle of channel A, range 0-65535
pwm12.duty_u16(int(65535 * 7.5 /100))      # set the duty cycle of channel A, range 0-65535
#pwm12.duty_u16(0)        # stop the output at channel A
print(pwm12)             # show the properties of the PWM object.
#pwm0.deinit()           # turn off PWM of slice 0, stopping channels A and B
while True:
    pass