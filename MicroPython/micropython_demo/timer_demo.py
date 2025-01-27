#RP2040 的系统定时器外设提供全局微秒时基并为其产生中断。软件定时器目前可用，数量不限（内存允许）。不需要指定计时器 id（目前支持 id=-1），因为它会默认为这个。

from machine import Timer

tim = Timer(period=5000, mode=Timer.ONE_SHOT, callback=lambda t:print(1))
tim.init(period=2000, mode=Timer.PERIODIC, callback=lambda t:print(2))