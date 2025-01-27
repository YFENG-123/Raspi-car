import machine
p12 = machine.Pin(12)
pwm12 = machine.PWM(p12)
pwm12.freq(50)
pwm12.duty(512)