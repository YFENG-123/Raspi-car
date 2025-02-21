import machine

pwm3 = machine.PWM(  # 初始化PWM
    machine.Pin(3), freq=50, duty_u16=int(65535 * 7.5 / 100)
)
pwm2 = machine.PWM(  # 初始化PWM
    machine.Pin(2), freq=50, duty_u16=int(65535 * 7.5 / 100)
)
while True:
    pass