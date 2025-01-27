# 见机器.machine.RTC
# machine.RTC http://micropython.com.cn/en/latet/library/machine.RTC.html#machine-rtc

from machine import RTC

rtc = RTC()
rtc.datetime((2017, 8, 23, 2, 12, 48, 0, 0)) # set a specific date and
                                             # time, eg. 2017/8/23 1:12:48
rtc.datetime() # get date and time