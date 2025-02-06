import machine
import time
import struct

# 电机类型具体值
MOTOR_TYPE_WITHOUT_ENCODER = 0
MOTOR_TYPE_TT = 1
MOTOR_TYPE_N20 = 2
MOTOR_TYPE_JGB37_520_12V_110RPM = 3  # 磁环每转是44个脉冲   减速比:90  默认

# 电机类型及编码方向极性
MotorType = MOTOR_TYPE_JGB37_520_12V_110RPM
MotorEncoderPolarity = 0


class I2c(machine.I2C):
    def __init__(self):
        pin4 = machine.Pin(4)
        pin5 = machine.Pin(5)
        super().__init__(0, scl=pin5, sda=pin4, freq=400_000)
        self._init_addr()  # 初始化地址
        time.sleep(0.5)
        self.writeto_mem(
            self.main_addr, self.motor_type_addr, b"3"
        )  # 设置电机类型为编码电机
        time.sleep(0.5)
        self.writeto_mem(
            self.main_addr, self.motor_encoder_polarity_addr, b"1"
        )  # 设置编码极性

    def _init_addr(self):
        device_list = self.scan()  # 扫描I2C设备
        print("device_list = {0}".format(device_list))
        # print("main_addr = {0}".format(device_list[0]))
        # print("main_addr_type = {0}".format(type(device_list[0])))
        # self.main_addr = device_list[0]  # 主控板地址
        self.main_addr = 52  # 主控板地址
        self.adc_bat_addr = 0x00  # ADC 电池采样
        self.motor_type_addr = 0x14  # 编码电机类型设置
        self.motor_encoder_polarity_addr = 0x15  # 设置编码方向极性
        """
        如果发现电机转速根本不受控制,要么最快速度转动,要么停止。可以将此地址的值重新设置一下
        范围0或1,默认0
        """
        self.motor_fixed_pwm_addr = 0x1F  # 固定PWM控制,属于开环控制,范围（-100~100）
        self.motor_fixed_speed_addr = 0x33  # 固定转速控制,属于闭环控制
        """
        单位:脉冲数每10毫秒,范围（根据具体的编码电机来,受编码线数,电压大小,负载大小等影响,一般在±50左右）
        """
        self.motor_encoder_total_addr = 0x3C  # 4个编码电机各自的总脉冲值
        """
        如果已知电机每转一圈的脉冲数为U,又已知轮子的直径D,那么就可以通过脉冲计数的方式得知每个轮子行进的距离
        比如读到电机1的脉冲总数为P,那么行进的距离为(P/U) * (3.14159*D)
        对于不同的电机可以自行测试每圈的脉冲数U,可以手动旋转10圈读出脉冲数,然后取平均值得出
        """

    def _reset(self):
        time.sleep(0.5)
        self.writeto_mem(
            self.main_addr, self.motor_encoder_polarity_addr, b"0"
        )  # 设置编码极性
        time.sleep(0.5)
        self.writeto_mem(
            self.main_addr, self.motor_encoder_polarity_addr, b"1"
        )  # 设置编码极性

    def read_battery(self):
        battery = self.readfrom_mem(self.main_addr, self.adc_bat_addr, 8)
        print("V = {0}mV".format(battery[0] + (battery[1] << 8)))

    def read_encoder(self):
        time.sleep(0.5)
        data = self.readfrom_mem(self.main_addr, self.motor_encoder_total_addr, 16)
        print("data = {0}".format(data))
        byte_data = bytes(data)
        print("byte_data = {0}".format(byte_data))
        Encode = struct.unpack("iiii", byte_data)
        print(
            "Encode1 = {0}  Encode2 = {1}  Encode3 = {2}  Encode4 = {3}".format(
                Encode[0], Encode[1], Encode[2], Encode[3]
            )
        )

    def set_pwm(self, pwm):
        pwm1 = bytes([pwm, pwm, pwm, pwm])
        time.sleep(0.5)
        self.writeto_mem(self.main_addr, self.motor_fixed_pwm_addr, pwm1)

    def set_speed(self, spd):
        speed1 = bytearray([50, 50, 50, 50])
        speed2 = bytearray([-50, -50, -50, -50])
        speed3 = bytearray([spd, spd, spd, spd])
        # print("speed1[0] = {0}".format(speed1[0]))
        time.sleep(0.5)
        print(b"50")
        self.writeto_mem(self.main_addr, self.motor_fixed_speed_addr, b"50")


if __name__ == "__main__":
    i2c = I2c()

    time.sleep(1)
    i2c.read_battery()

    time.sleep(1)
    # i2c.set_speed(1)

    time.sleep(1)
    i2c._reset()

    """
    while True:
        i2c.set_speed(100)
        time.sleep(1)
    """

    """
    for i in range(0, 1000):
        i2c.set_speed(i)
        print("i = {0}".format(i))
        time.sleep(0.5)
    """

"""
while True:
    i2c.read_encoder()
    i2c.set_speed(50)
    time.sleep(1)
    i2c.set_speed(-50)
    time.sleep(1)
"""
