# RP2040 有一个看门狗，它是一个倒数计时器，可以在它达到零时重新启动芯片的某些部分。
# 参见 machine.WDT http://micropython.com.cn/en/latet/library/machine.WDT.html#machine-wdt

from machine import WDT

# enable the WDT with a timeout of 5s (1s is the minimum)
wdt = WDT(timeout=5000)
wdt.feed()

