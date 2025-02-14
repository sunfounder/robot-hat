from robot_hat.i2c import I2C
import time

ADDR = 0x17
i2c = I2C(ADDR)

def get_board_id():
    BOARD_ID_REG_ADDR = 0x04
    # i2c = I2C(ADDR)
    board_id = i2c.mem_read(1, BOARD_ID_REG_ADDR)
    return board_id

def get_firmware_version():
    VERSSION_REG_ADDR = 0x05
    # i2c = I2C(ADDR)
    version = i2c.mem_read(3, VERSSION_REG_ADDR)
    return version

def get_mcu_main_freq():
    MAIN_FREQ_REG_ADDR = 0x08
    # i2c = I2C(ADDR)
    main_freq = i2c.mem_read(2, MAIN_FREQ_REG_ADDR)
    main_freq = (main_freq[0] << 8) + main_freq[1]
    return main_freq * 10000 # Hz

def get_usr_btn():
    BTN_REG_ADDR = 0x24
    btn = i2c.mem_read(1, BTN_REG_ADDR)
    return btn

def get_chg_state():
    CHG_REG_ADDR = 0x25
    chg = i2c.mem_read(1, CHG_REG_ADDR)
    return chg

def get_all_adc():
    BTN_REG_ADDR = 0x10
    res = i2c.mem_read(10, BTN_REG_ADDR) # 2 * 5
    a0 = (res[0] << 8) + res[1]
    a1 = (res[2] << 8) + res[3]
    a2 = (res[4] << 8) + res[5]
    a3 = (res[6] << 8) + res[7]
    bat = (res[8] << 8) + res[9]
    return (a0, a1, a2, a3, bat)

def get_all_adc_voltage():
    BTN_REG_ADDR = 0x10
    res = i2c.mem_read(10, BTN_REG_ADDR) # 2 * 5
    a0 = ((res[0] << 8) + res[1]) * 3.3 / 4095
    a1 = ((res[2] << 8) + res[3]) * 3.3 / 4095
    a2 = ((res[4] << 8) + res[5]) * 3.3 / 4095
    a3 = ((res[6] << 8) + res[7]) * 3.3 / 4095
    bat = ((res[8] << 8) + res[9]) * 3.3 / 4095
    return (a0, a1, a2, a3, bat)

if __name__ == '__main__':
    print('Board ID: ', get_board_id())
    print('Firmware version: ', get_firmware_version())
    print('MCU main frequency: ', get_mcu_main_freq())
    time.sleep(1)
    while True:
        usr_btn = get_usr_btn()
        chg_state = get_chg_state()
        a0, a1, a2, a3, bat = get_all_adc_voltage()
        print(f'User button: {usr_btn}, isCharging: {chg_state}, ADC: {a0:.3f}, {a1:.3f}, {a2:.3f}, {a3:.3f}, {bat*3:.3f}')
        time.sleep(0.01)
