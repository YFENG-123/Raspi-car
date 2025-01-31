
import machine
import json

pwm2 = machine.PWM(machine.Pin(2), freq=50, duty_u16=1024)
pwm3 = machine.PWM(machine.Pin(3), freq=50, duty_u16=1024)

Pin0 = machine.Pin(0, machine.Pin.OUT)
Pin1 = machine.Pin(1, machine.Pin.IN)
uart = machine.UART(0, baudrate=115200, tx=Pin0, rx=Pin1)


Left_duty_X = 7.5
Left_duty_Y = 7.5

Left_spd_X = 0
Left_spd_Y = 0


buffer = ""
while True:
    b = uart.read(1)
    if b is None:
        continue
    elif b == b"\n":
        print(buffer)
        buffer = buffer.split(";")
        print(buffer)
        try:
            Left_spd_X = float(buffer[0])
            Left_spd_Y = float(buffer[1])
        except Exception as e:
            print(e)
        print(Left_spd_X, Left_spd_Y)
        buffer = ""

        Left_duty_X = Left_duty_X - Left_spd_X * 0.15
        Left_duty_Y = Left_duty_Y + Left_spd_Y * 0.15

        if Left_duty_X > 12.5:
            Left_duty_X = 12.5
        elif Left_duty_X < 2.5:
            Left_duty_X = 2.5
        if Left_duty_Y > 12.5:
            Left_duty_Y = 12.5
        elif Left_duty_Y < 2.5:
            Left_duty_Y = 2.5

        pwm2.duty_u16(
            int(65535 * Left_duty_X / 100)
        )  # set the duty cycle of channel A, range 0-65535
        pwm3.duty_u16(
            int(65535 * Left_duty_Y / 100)
        )  # set the duty cycle of channel A, range 0-65535
        continue
    else:
        buffer += str(b)[2]

