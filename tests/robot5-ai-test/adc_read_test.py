from robot_hat import ADC
import time

addr = 0x17
# a0 = ADC(0, addr)
# a1 = ADC(1, addr)
# a2 = ADC(2, addr)
# a3 = ADC(3, addr)
# bat_lv = ADC(4, addr)

a0 = ADC(0)
a1 = ADC(1)
a2 = ADC(2)
a3 = ADC(3)
bat_lv = ADC(4)


while True:
    v0 = a0.read_voltage()
    v1 = a1.read_voltage()
    v2 = a2.read_voltage()
    v3 = a3.read_voltage()
    vbat = bat_lv.read_voltage() * 3
    print(f'{time.time():.3f}  a0: {v0:.3f}, a1: {v1:.3f}, a2: {v2:.3f}, a3: {v3:.3f}, bat: {vbat:.3f}')
    time.sleep(0.1)

