from machine import ADC, Pin
adc = ADC(Pin(26))     # create ADC object on ADC pin
while True:
    print(3.3 *adc.read_u16() / 65535 )