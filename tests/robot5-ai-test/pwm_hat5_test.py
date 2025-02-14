import time
from pwm_hat5 import PWM_GROUP

st = time.time()
pwm_group = PWM_GROUP([0,1,2,3,8,9,10,11,4,5,6,7], freq=50)
print(f'init PWM_GROUP {time.time()-st}')

print(f'freq: {pwm_group.frequency()}Hz, period: {pwm_group.period()}, prescaler: {pwm_group.prescaler()}')
_step = (pwm_group.period()+1) / 12
for i in range(12):
    pwm_group[i] = _step*(i+1)
print(f'pwm_group: {pwm_group.pulse_width_all()}')
pwm_group.write()

try:
    while True:
        time.sleep(3)
        pwm_group.frequency(50)
        time.sleep(3)
        pwm_group.frequency(100)
finally:
    print('reset pwm_group to 0')
    for i in range(12):
        pwm_group[i] = 0
    pwm_group.write()
    print(f'pwm_group: {pwm_group.pulse_width_all()}')





