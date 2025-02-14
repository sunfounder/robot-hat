import os

class Devices():
    HAT_DEVICE_TREE = "/proc/device-tree/"
    HAT_UUIDs = [
        "9daeea78-0000-076e-0032-582369ac3e02", # robothat5 1902v50
        "9daeea78-0000-076e-003c-582369ac3e02" # robothat6 1902v60
        ]

    DEVICES = {
        "base": {
            "name": "base",
            "i2c_addr": 0x14,
            "uuid": None,
            "speaker_enbale_pin": None,
            "motor_mode": 1
        },
        "robot_hat_v4x": {
            "name": "robot_hat_v4x",
            "i2c_addr": 0x14,
            "uuid": None,
            "speaker_enbale_pin": 20,
            "motor_mode": 1,
        }, 
        "robot_hat_v5x": {
            "name": "robot_hat_v5x",
            "i2c_addr": 0x15,
            "uuid": HAT_UUIDs[0],
            "speaker_enbale_pin": 12,
            "motor_mode": 2,
        },
        "robot_hat_v6x": {
            "name": "robot_hat_v6x",
            "i2c_addr": 0x17,
            "uuid": HAT_UUIDs[1],
            "speaker_enbale_pin": "I2C_0x31",
            "motor_mode": 2,
        },
    }

    name = ""
    product_id = 0
    product_ver = 0
    uuid = ""
    vendor = ""
    spk_en = 20
    motor_mode = 1
    i2c_addr = None

    def __init__(self):
        hat = self.check_hat()
        if hat is not None:
            self.name = hat["name"]
            self.i2c_addr = hat["i2c_addr"]
            self.product_id = hat["product_id"]
            self.product_ver = hat["product_ver"]
            self.uuid = hat["uuid"]
            self.vendor = hat["vendor"]
            self.spk_en = hat["speaker_enbale_pin"]
            self.motor_mode = hat["motor_mode"]
        else:
            self.set_hat('robot_hat_v4x')

    def check_hat(self):
        hat_path = None
        hat = {
        }
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
                _name = f.read()
                hat["name"] = _name
            with open(f"{hat_path}/product_id", "r") as f:
                _product_id = f.read()[:-1] # [:-1] rm \x00
                _product_id = int(_product_id, 16)
                hat["product_id"] = _product_id
            with open(f"{hat_path}/product_ver", "r") as f:
                _product_ver = f.read()[:-1]
                _product_ver = int(_product_ver, 16)
                hat["product_ver"] = _product_ver
            with open(f"{hat_path}/uuid", "r") as f:
                _uuid = f.read()[:-1] # [:-1] rm \x00
                hat["uuid"] = _uuid
            with open(f"{hat_path}/vendor", "r") as f:
                _vendor = f.read()
                hat["vendor"] = _vendor

            for device in self.DEVICES:
                if self.DEVICES[device]['uuid'] == hat["uuid"]:
                    hat["i2c_addr"] = self.DEVICES[device]["i2c_addr"]
                    hat["speaker_enbale_pin"] = self.DEVICES[device]["speaker_enbale_pin"]
                    hat["motor_mode"] = self.DEVICES[device]["motor_mode"]
                    break
            return hat
        else:
            return None

    def set_hat(self, name):
        if name in self.DEVICES:
            self.name = name
            self.i2c_addr = self.DEVICES[name]["i2c_addr"]
            self.product_id = 0
            self.product_ver = 0
            self.vendor = ""
            self.uuid = self.DEVICES[name]["uuid"]
            self.spk_en = self.DEVICES[name]["speaker_enbale_pin"]
            self.motor_mode = self.DEVICES[name]["motor_mode"]

__device__ = Devices()


if __name__ == "__main__":
    device = Devices()
    # device.set_hat("robot_hat_v4x")
    print(f'name: {device.name}')
    print(f'i2c_addr: {device.i2c_addr:#02x}')
    print(f'product_id: {device.product_id}')
    print(f'product_ver: {device.product_ver}')
    print(f'vendor: {device.vendor}')
    print(f'uuid: {device.uuid}')
    print(f'speaker_enbale_pin: {device.spk_en}')
    print(f'motor_mode: {device.motor_mode}')
