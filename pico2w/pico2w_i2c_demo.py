from machine import Pin, I2C
import time
import struct

# 设置I2C总线号，通常为1
I2C_BUS = 0

# 设置四路电机驱动模块的I2C地址
MOTOR_ADDR = 0x34 

# 寄存器地址
ADC_BAT_ADDR = 0x00 # ADC 电池采样
MOTOR_TYPE_ADDR = 0x14 # 编码电机类型设置
MOTOR_ENCODER_POLARITY_ADDR = 0x15 #设置编码方向极性，
#如果发现电机转速根本不受控制，要么最快速度转动，要么停止。可以将此地址的值重新设置一下
#范围0或1，默认0
MOTOR_FIXED_PWM_ADDR = 0x1F #固定PWM控制，属于开环控制,范围（-100~100）   
MOTOR_FIXED_SPEED_ADDR = 0x33 #固定转速控制，属于闭环控制，
#单位：脉冲数每10毫秒，范围（根据具体的编码电机来，受编码线数，电压大小，负载大小等影响，一般在±50左右）

MOTOR_ENCODER_TOTAL_ADDR = 0x3C #4个编码电机各自的总脉冲值
# #如果已知电机每转一圈的脉冲数为U，又已知轮子的直径D，那么就可以通过脉冲计数的方式得知每个轮子行进的距离
# #比如读到电机1的脉冲总数为P，那么行进的距离为(P/U) * (3.14159*D)
# #对于不同的电机可以自行测试每圈的脉冲数U，可以手动旋转10圈读出脉冲数，然后取平均值得出


#电机类型具体值
MOTOR_TYPE_WITHOUT_ENCODER = 0
MOTOR_TYPE_TT = 1
MOTOR_TYPE_N20 = 2
MOTOR_TYPE_JGB37_520_12V_110RPM = 3 #磁环每转是44个脉冲   减速比:90  默认

#电机类型及编码方向极性
MotorType = MOTOR_TYPE_JGB37_520_12V_110RPM
MotorEncoderPolarity = 0

speed1 = [50,50,50,50]
speed2 = [-50,-50,-50,-50]
speed3 = [0,0,0,0]

pwm1 = [50,50,50,50]
pwm2 = [-100,-100,-100,-100]
pwm3 = [0,0,0,0]

bus = I2C(0, scl=Pin(5), sda=Pin(4), freq=400_000)
scan = bus.scan()                      # scan for slaves, returning a list of 7-bit addresses
print(scan)

bus.writeto_mem(MOTOR_ADDR, MOTOR_TYPE_ADDR, b'3')  #设置电机类型
time.sleep(0.5)
bus.writeto_mem(MOTOR_ADDR, MOTOR_ENCODER_POLARITY_ADDR, b'0')  #设置编码极性


battery = bus.readfrom_mem(MOTOR_ADDR, ADC_BAT_ADDR,8)
print("V = {0}mV".format(battery[0]+(battery[1]<<8)))

Encode = struct.unpack('iiii',bytes(bus.readfrom_mem(MOTOR_ADDR, MOTOR_ENCODER_TOTAL_ADDR,16)))
print("Encode1 = {0}  Encode2 = {1}  Encode3 = {2}  Encode4 = {3}".format(Encode[0],Encode[1],Encode[2],Encode[3]))
    


bus.writeto_mem(MOTOR_ADDR, MOTOR_FIXED_PWM_ADDR,b'0')
#bus.writeto_mem(MOTOR_ADDR, MOTOR_FIXED_SPEED_ADDR,b"[50,50,50,50]")







