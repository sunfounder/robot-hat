#!/usr/bin/env python3
from .basic import _Basic_class
from .utils import run_command
from smbus2 import SMBus
import multiprocessing


def _retry_wrapper(func):

    def wrapper(self, *arg, **kwargs):
        for _ in range(self.RETRY):
            try:
                return func(self, *arg, **kwargs)
            except OSError:
                self._debug(f"OSError: {func.__name__}")
                continue
        else:
            return False

    return wrapper


class I2C(_Basic_class):
    """
    I2C bus read/write functions
    """
    RETRY = 5

    # i2c_lock = multiprocessing.Value('i', 0)

    def __init__(self, address=None, bus=1, *args, **kwargs):
        """
        Initialize the I2C bus

        :param address: I2C device address
        :type address: int
        :param bus: I2C bus number
        :type bus: int
        """
        super().__init__(*args, **kwargs)
        self._bus = bus
        self._smbus = SMBus(self._bus)
        if isinstance(address, list):
            connected_devices = self.scan()
            for _addr in address:
                if _addr in connected_devices:
                    self.address = _addr
                    break
            else:
                self.address = address[0]
        else:
            self.address = address

        # print(f'address: 0x{self.address:02X}')

    @_retry_wrapper
    def _write_byte(self, data):
        # with I2C.i2c_lock.get_lock():
        self._debug(f"_write_byte: [0x{data:02X}]")
        result = self._smbus.write_byte(self.address, data)
        return result

    @_retry_wrapper
    def _write_byte_data(self, reg, data):
        # with I2C.i2c_lock.get_lock():
        self._debug(f"_write_byte_data: [0x{reg:02X}] [0x{data:02X}]")
        return self._smbus.write_byte_data(self.address, reg, data)

    @_retry_wrapper
    def _write_word_data(self, reg, data):
        # with I2C.i2c_lock.get_lock():
        self._debug(f"_write_word_data: [0x{reg:02X}] [0x{data:04X}]")
        return self._smbus.write_word_data(self.address, reg, data)

    @_retry_wrapper
    def _write_i2c_block_data(self, reg, data):
        # with I2C.i2c_lock.get_lock():
        self._debug(
            f"_write_i2c_block_data: [0x{reg:02X}] {[f'0x{i:02X}' for i in data]}"
        )
        return self._smbus.write_i2c_block_data(self.address, reg, data)

    @_retry_wrapper
    def _read_byte(self):
        # with I2C.i2c_lock.get_lock():
        result = self._smbus.read_byte(self.address)
        self._debug(f"_read_byte: [0x{result:02X}]")
        return result

    @_retry_wrapper
    def _read_byte_data(self, reg):
        # with I2C.i2c_lock.get_lock():
        result = self._smbus.read_byte_data(self.address, reg)
        self._debug(f"_read_byte_data: [0x{reg:02X}] [0x{result:02X}]")
        return result

    @_retry_wrapper
    def _read_word_data(self, reg):
        # with I2C.i2c_lock.get_lock():
        result = self._smbus.read_word_data(self.address, reg)
        result_list = [result & 0xFF, (result >> 8) & 0xFF]
        self._debug(f"_read_word_data: [0x{reg:02X}] [0x{result:04X}]")
        return result_list

    @_retry_wrapper
    def _read_i2c_block_data(self, reg, num):
        # with I2C.i2c_lock.get_lock():
        result = self._smbus.read_i2c_block_data(self.address, reg, num)
        self._debug(
            f"_read_i2c_block_data: [0x{reg:02X}] {[f'0x{i:02X}' for i in result]}"
        )
        return result

    @_retry_wrapper
    def is_ready(self):
        """Check if the I2C device is ready

        :return: True if the I2C device is ready, False otherwise
        :rtype: bool
        """
        addresses = self.scan()
        if self.address in addresses:
            return True
        else:
            return False

    def scan(self):
        """Scan the I2C bus for devices

        :return: List of I2C addresses of devices found
        :rtype: list
        """
        cmd = f"i2cdetect -y {self._bus}"
        # Run the i2cdetect command
        _, output = run_command(cmd)

        # Parse the output
        outputs = output.split('\n')[1:]
        addresses = []
        addresses_str = []
        for tmp_addresses in outputs:
            if tmp_addresses == "":
                continue
            tmp_addresses = tmp_addresses.split(':')[1]
            # Split the addresses into a list
            tmp_addresses = tmp_addresses.strip().split(' ')
            for address in tmp_addresses:
                if address != '--':
                    addresses.append(int(address, 16))
                    addresses_str.append(f'0x{address}')
        self._debug(f"Conneceted i2c device: {addresses_str}")
        return addresses

    def write(self, data):
        """Write data to the I2C device

        :param data: Data to write
        :type data: int/list/bytearray
        :raises: ValueError if write is not an int, list or bytearray
        """
        if isinstance(data, bytearray):
            data_all = list(data)
        elif isinstance(data, int):
            if data == 0:
                data_all = [0]
            else:
                data_all = []
                while data > 0:
                    data_all.append(data & 0xFF)
                    data >>= 8
        elif isinstance(data, list):
            data_all = data
        else:
            raise ValueError(
                f"write data must be int, list, or bytearray, not {type(data)}"
            )

        # Write data
        if len(data_all) == 1:
            data = data_all[0]
            self._write_byte(data)
        elif len(data_all) == 2:
            reg = data_all[0]
            data = data_all[1]
            self._write_byte_data(reg, data)
        elif len(data_all) == 3:
            reg = data_all[0]
            data = (data_all[2] << 8) + data_all[1]
            self._write_word_data(reg, data)
        else:
            reg = data_all[0]
            data = list(data_all[1:])
            self._write_i2c_block_data(reg, data)

    def read(self, length=1):
        """Read data from I2C device

        :param length: Number of bytes to receive
        :type length: int
        :return: Received data
        :rtype: list
        """
        if not isinstance(length, int):
            raise ValueError(f"length must be int, not {type(length)}")

        result = []
        for _ in range(length):
            result.append(self._read_byte())
        return result

    def mem_write(self, data, memaddr):
        """Send data to specific register address

        :param data: Data to send, int, list or bytearray
        :type data: int/list/bytearray
        :param memaddr: Register address
        :type memaddr: int
        :raise ValueError: If data is not int, list, or bytearray
        """
        if isinstance(data, bytearray):
            data_all = list(data)
        elif isinstance(data, list):
            data_all = data
        elif isinstance(data, int):
            data_all = []
            if data == 0:
                data_all = [0]
            else:
                while data > 0:
                    data_all.append(data & 0xFF)
                    data >>= 8
        else:
            raise ValueError(
                "memery write require arguement of bytearray, list, int less than 0xFF"
            )
        self._write_i2c_block_data(memaddr, data_all)

    def mem_read(self, length, memaddr):
        """Read data from specific register address

        :param length: Number of bytes to receive
        :type length: int
        :param memaddr: Register address
        :type memaddr: int
        :return: Received bytearray data or False if error
        :rtype: list/False
        """
        result = self._read_i2c_block_data(memaddr, length)
        return result

    def is_avaliable(self):
        """
        Check if the I2C device is avaliable

        :return: True if the I2C device is avaliable, False otherwise
        :rtype: bool
        """
        return self.address in self.scan()


if __name__ == "__main__":
    i2c = I2C(address=[0x17, 0x15], debug_level='debug')