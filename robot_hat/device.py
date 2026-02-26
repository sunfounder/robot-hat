import os

class Devices():
    HAT_DEVICE_TREE = "/proc/device-tree/"
    HAT_UUIDs = [
        "9daeea78-0000-076e-0032-582369ac3e02", # robothat5 1902v50
        ]

    DEVICES = {
        "robot_hat_v4x": {
            "uuid": None,
            "speaker_enbale_pin": 20,
            "motor_mode": 1,
        }, 
        "robot_hat_v5x": {
            "uuid": HAT_UUIDs[0],
            "speaker_enbale_pin": 12,
            "motor_mode": 2,
        }
    }

    name = ""
    product_id = 0
    product_ver = 0
    uuid = ""
    vendor = ""
    spk_en = 20
    motor_mode = 1

    def __init__(self):
        hat_path = None
        for file in os.listdir('/proc/device-tree/'):
            if 'hat' in file:
                # print("hat detected")
                if os.path.exists(f"/proc/device-tree/{file}/uuid") \
                    and os.path.isfile(f"/proc/device-tree/{file}/uuid"):
                    # print("uuid detected")
                    with open(f"/proc/device-tree/{file}/uuid", "r") as f:
                        uuid = f.read()[:-1] # [:-1] rm \x00
                        if uuid in self.HAT_UUIDs:
                            hat_path = f"/proc/device-tree/{file}"
                            break

        if hat_path is not None:
            with open(f"{hat_path}/product", "r") as f:
                self.name = f.read()
            with open(f"{hat_path}/product_id", "r") as f:
                self.product_id = f.read()[:-1] # [:-1] rm \x00
                self.product_id = int(self.product_id, 16)
            with open(f"{hat_path}/product_ver", "r") as f:
                self.product_ver = f.read()[:-1]
                self.product_ver = int(self.product_ver, 16)
            with open(f"{hat_path}/uuid", "r") as f:
                self.uuid = f.read()[:-1] # [:-1] rm \x00
            with open(f"{hat_path}/vendor", "r") as f:
                self.vendor = f.read()

            for device in self.DEVICES:
                if self.DEVICES[device]['uuid'] == self.uuid:
                    self.spk_en = self.DEVICES[device]["speaker_enbale_pin"]
                    self.motor_mode = self.DEVICES[device]["motor_mode"]
                    break

BATTERY_ADC_OBJ = None

PIN = {
    "D0": 17,
    "D1": 4,
    "D2": 27,
    "D3": 22,
    "D4": 23,
    "D5": 24,
    "D6": 25,
    "D7": 4,
    "D8": 5,
    "D9": 6,
    "D10": 12,
    "D11": 13,
    "D12": 19,
    "D13": 16,
    "D14": 26,
    "D15": 20,
    "D16": 21,
    "SW": 25,
    "USER": 25,
    "LED": 26,
    "BOARD_TYPE": 12,
    "RST": 16,
    "BLEINT": 13,
    "BLERST": 20,
    "MCURST": 5,
    "CE": 8,
}

def set_pin(pin: int, value: bool):
    """
    Set pin value

    :param pin: pin number
    :type pin: int
    :param value: pin value
    :type value: bool
    """
    from .utils import command_exists, run_command
    pincmd = ''
    if command_exists("pinctrl"):
        pincmd = 'pinctrl'
    elif command_exists("raspi-gpio"):
        pincmd = 'raspi-gpio'
    else:
        error("Can't find `pinctrl` or `raspi-gpio` to enable speaker")
        return

    cmd = f"{pincmd} set {pin} op {'dh' if value else 'dl'}"
    run_command(cmd)

def get_usr_btn() -> bool:
    """ Get user button state
    Get user button state from pinctrl command

    Returns:
        bool: True if pressed
    """
    from .pin import Pin
    pin = Pin("USER")
    return pin.value() == 0

def set_led(state: [int, bool]) -> None:
    """ Set led state

    Args:
        state (int or bool): 0:off, 1:on, True:on, False:off
    """
    from .pin import Pin
    pin = Pin("LED")
    pin.value = state

def get_led() -> bool:
    """ Get led state

    Returns:
        bool: True if on
    """
    from .pin import Pin
    pin = Pin("LED")
    return pin.value() == 1

def enable_speaker():
    """
    Enable speaker
    """
    from . import __device__
    from .utils import run_command
    set_pin(__device__.spk_en, True)
    # play a short sound to fill data and avoid the speaker overheating
    run_command(f"play -n trim 0.0 0.5 2>/dev/null")

def disable_speaker():
    """
    Disable speaker
    """
    from . import __device__
    set_pin(__device__.spk_en, False)

def reset_mcu():
    """
    Reset mcu on Robot Hat.

    This is helpful if the mcu somehow stuck in a I2C data
    transfer loop, and Raspberry Pi getting IOError while
    Reading ADC, manipulating PWM, etc.
    """
    import time
    set_pin(PIN["MCURST"], False)
    time.sleep(0.01)
    set_pin(PIN["MCURST"], True)
    time.sleep(0.01)

def get_battery_voltage():
    """
    Get battery voltage

    :return: battery voltage(V)
    :rtype: float
    """
    global BATTERY_ADC_OBJ
    from .adc import ADC

    if not isinstance(BATTERY_ADC_OBJ, ADC):
        BATTERY_ADC_OBJ = ADC("A4")
    raw_voltage = BATTERY_ADC_OBJ.read_voltage()
    voltage = raw_voltage * 3
    return voltage

if __name__ == "__main__":
    device = Devices()
    print(f'name: {device.name}')
    print(f'product_id: {device.product_id}')
    print(f'product_ver: {device.product_ver}')
    print(f'vendor: {device.vendor}')
    print(f'uuid: {device.uuid}')
    print(f'speaker_enbale_pin: {device.spk_en}')
    print(f'motor_mode: {device.motor_mode}')
