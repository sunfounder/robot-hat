import os

class Devices():
    DEVICES = {
        0: {
            "version": {
                0: {
                    "name":  "generic",
                    "speaker_enbale_pin": None,
                    "motor_mode": 1,
                }
            }
        },
        1902: {
            "version": {
                0: {
                    "name":  "robot_hat",
                    "speaker_enbale_pin": None,
                    "motor_mode": 1,
                },
                40: {
                    "name":  "robot_hat_V4",
                    "speaker_enbale_pin": None,
                    "motor_mode": 1,
                },
                44: {
                    "name":  "robot_hat_V44",
                    "speaker_enbale_pin": 20,
                    "motor_mode": 1,
                },
                50: {
                    "name":  "robot_hat_5",
                    "speaker_enbale_pin": 12,
                    "motor_mode": 2,
                },

            }
        },
        1906: {
            "version": {
                0 : {
                    "name": "servo_hat",
                    "speaker_enbale_pin": 20,
                    "motor_mode": None,
                },
                10 : {
                    "name": "servo_hat",
                    "speaker_enbale_pin": 20,
                    "motor_mode": None,
                }
            }
        },
    }

    product_id = 0
    product_ver = 0
    vendor = ""
    hat_detected = False
    name = ""
    spk_en = 20
    motor_mode = 1

    def __init__(self):
        hat_path = None
        for file in os.listdir('/proc/device-tree/'):
            if file.startswith('hat'):
                hat_path = f"/proc/device-tree/{file}"
                self.hat_detected = True
                break
        else:
            self.hat_detected = False

        if hat_path is not None:
            with open(f"{hat_path}/product_id", "r") as f:
                self.product_id = f.read()[:-1] # [:-1] rm \x00
                self.product_id = int(self.product_id, 16)
                # print(self.product_id)
            with open(f"{hat_path}/product_ver", "r") as f:
                self.product_ver = f.read()[:-1]
                self.product_ver = int(self.product_ver, 16)
                # print(self.product_ver)
            with open(f"{hat_path}/product", "r") as f:
                self.name = f.read()
                # print(self.name)
            with open(f"{hat_path}/vendor", "r") as f:
                self.vendor = f.read()
            device = self.DEVICES[self.product_id]["version"][self.product_ver]
            self.spk_en = device["speaker_enbale_pin"]
            self.motor_mode = device["motor_mode"]
            # print(self.spk_en)
            # print(self.motor_mode)

if __name__ == "__main__":
    device = Devices()
