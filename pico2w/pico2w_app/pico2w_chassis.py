import machine
import time

# C - A
# D - B
E2A = 6
E2B = 7
E1A = 8
E1B = 12  # 9 -> 12

PWMB = 10
BIN2 = 11
BIN1 = 9  # 12 -> 9
AIN1 = 14  # 13 -> 14
AIN2 = 13  # 14 -> 13
PWMA = 15

E2C = 26
E2D = 4
E1C = 5
E1D = 17  # 16 -> 17

PWMD = 16  # 17 -> 16
DIN2 = 19  # 18 -> 19
DIN1 = 18  # 19 -> 18
CIN1 = 20
CIN2 = 21
PWMC = 22


class Motor:
    def __init__(self, e_a, e_b, pwm, in_1, in_2):
        self.pwm = machine.PWM(
            pwm, freq=10000, duty_u16=int(65535 * 0 / 100)
        )  # 初始化PWM引脚
        self.in_1 = machine.Pin(in_1, machine.Pin.OUT, value=0)  # 初始化IN1引脚
        self.in_2 = machine.Pin(in_2, machine.Pin.OUT, value=1)  # 初始化IN2引脚

    def stop(self):
        self.pwm.duty_u16(int(65535 * 0 / 100))
        self.in_1.value(0)
        self.in_2.value(0)

    def set_pwm(self, duty):
        if duty > 0:
            self.in_1.value(1)
            self.in_2.value(0)
        elif duty < 0:
            self.in_1.value(0)
            self.in_2.value(1)
        else:
            self.in_1.value(0)
            self.in_2.value(0)
        self.pwm.duty_u16(int(65535 * abs(duty) / 100))


class Chassis:
    def __init__(self):
        self.motor_A = Motor(E1A, E1B, PWMA, AIN1, AIN2)
        self.motor_B = Motor(E2A, E2B, PWMB, BIN1, BIN2)
        self.motor_C = Motor(E1C, E1D, PWMC, CIN1, CIN2)
        self.motor_D = Motor(E2C, E2D, PWMD, DIN1, DIN2)
        self.motor_A.set_pwm(10)
        self.motor_B.set_pwm(-10)
        self.motor_C.set_pwm(10)
        self.motor_D.set_pwm(-10)
        time.sleep(0.5)
        self.stop()

    def set_pwm(self, x, y, z1, z2):
        print("x:", x, "y:", y)
        x = x * 100
        y = y * 100
        omega = (z2 - z1) * 50
        print("x:", x, "y:", y)
        self.motor_A.set_pwm(y - x - omega)
        print("y+x : ", y + x)
        self.motor_B.set_pwm(y + x - omega)
        print("y-x : ", y - x)
        print("z1:", z1, "z2:", z2, "omega:", omega)
        self.motor_C.set_pwm(y - x + omega)
        self.motor_D.set_pwm(y + x + omega)

    def stop(self):
        self.motor_A.stop()
        self.motor_B.stop()
        self.motor_C.stop()
        self.motor_D.stop()


if __name__ == "__main__":
    print(time.ticks_cpu())
    print(time.ticks_cpu())
    chassis = Chassis()
    for x in range(0, 10, 1):
        time.sleep(0.1)
    chassis.stop()
