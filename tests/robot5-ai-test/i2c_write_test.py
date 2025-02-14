from robot_hat.i2c import I2C
import time

ADDR = 0x17
i2c = I2C(ADDR)

def write_usr_led(value:None):
    '''
    params: value: None, 0, 1, 2
                 None, return current value
                 0, turn off
                 1, turn on
                 2, toggle
    '''
    REG_USR_LED_ADDR = 0x30

    if value is None:
        return i2c.mem_read(1, REG_USR_LED_ADDR)
    else:
        value = int(value) & 0x0f
        i2c.mem_write(value, REG_USR_LED_ADDR)

def write_spk_en(value:None):
    '''
    params: value: None, 0, 1
                 None, return current value
                 0, enable speaker
                 1, disable speaker
    '''
    REG_SPK_EN_ADDR = 0x31

    if value is None:
        return i2c.mem_read(1, REG_SPK_EN_ADDR)
    else:
        value = int(value) & 0x0f
        i2c.mem_write(value, REG_SPK_EN_ADDR)

if __name__ == '__main__':
    try:
        st = time.time()
        print_st = st
        write_spk_en(1)
        while True:
            if time.time() - st > 0.3:
                write_usr_led(2)
                st = time.time()
            if time.time() - print_st > .5:
                print(f'user_led: {write_usr_led(None)}, spk_en: {write_spk_en(None)}')
                print_st = time.time()


            time.sleep(.1)
    finally:
        write_usr_led(0)
