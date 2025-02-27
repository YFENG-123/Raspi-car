# Raspi-car
- 测试环境：Windows 11

- 运行环境：树莓派5（8GB RAM） arm64 aarch64 PIOS 64位
  - 运行环境下引入pygame库需要 ``conda install -c conda-forge gcc`` 否则会报错。
  - pyaudio库需要安装前置库pyaudio，使用``sudo apt install portaudio19-dev``
  - conda安装后使用/Home YFENG/anaconda3/bin/conda init初始化，然后conda config --set auto_activate_base false关闭自动启动

- 关于GPIO
  - 用gpiozero库操作GPIO默认工厂为PRI.gpio，其输出的PWM抖动非常大，舵机无法正常使用。
  - pigpio，rpi.gpio，均不可用，只能使用lgpio，使用前需要安装pip install rpi-lgpio
- 关于UART
  - 需要安装minicom才能正常使用``sudo apt install minicom``
  - GPIO14和GPIO15为默认开启的uart，设备名为ttyAMA0

- 树莓派5 风扇全速模式
  ```
  sudo nano /boot/firmware/config.txt
  ```
  末尾插入
  ```
  dtparam=cooling_fan=on
  dtparam=fan_temp3=35000,fan_temp3_hyst=5000,fan_temp3_speed=255
  ```

- pygame.makesurface()会对图像进行一次转置，导致图像显示不正常，因此需要提前对图像进行一次转置

- pyserial发现的串口设备号可能不是真实的串口设备号，先使用minicom测试通信找到串口号