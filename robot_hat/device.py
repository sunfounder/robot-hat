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

if __name__ == "__main__":
    device = Devices()
    print(f'name: {device.name}')
    print(f'product_id: {device.product_id}')
    print(f'product_ver: {device.product_ver}')
    print(f'vendor: {device.vendor}')
    print(f'uuid: {device.uuid}')
    print(f'speaker_enbale_pin: {device.spk_en}')
    print(f'motor_mode: {device.motor_mode}')
