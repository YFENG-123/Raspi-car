# RP2040 共有五个 ADC 通道，其中四个是基于 12 位 SAR 的 ADC：GP26、GP27、GP28 和 GP29。ADC0、ADC1、ADC2、ADC3的输入信号可以分别接GP26、GP27、GP28、GP29（Pico板上GP29接VSYS）。标准的 ADC 范围是 0-3.3V。第五个通道连接到内置温度传感器，可用于测量温度。
# 更多 http://micropython.com.cn/en/latet/library/machine.ADC.html#machine-adc
from machine import ADC, Pin
while True:
    adc = ADC(Pin(26))     # create ADC object on ADC pin
    adc.read_u16()         # read value, 0-65535 across voltage range 0.0v - 3.3v