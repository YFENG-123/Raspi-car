#MicroPython REPL 通过 USB 串行端口访问。制表符完成对于找出对象具有哪些方法很有用。粘贴模式 (ctrl-E) 可用于将大量 Python 代码粘贴到 REPL 中。
import machine

machine.freq()          # get the current frequency of the CPU
machine.freq(240000000) # set the CPU frequency to 240 MHz
