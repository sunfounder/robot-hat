#!/usr/bin/env python3
from .basic import _Basic_class
from smbus import SMBus

def _retry_wrapper(func):
    def wrapper(self, *arg, **kwargs):
        for i in range(self.RETRY):
            try:
                return func(self, *arg, **kwargs)
            except OSError:
                self._debug("OSError: %s" % func.__name__)
                continue
        else:
            return False
    return wrapper

class I2C(_Basic_class):
    """
    I2C bus read/write functions
    """
    RETRY = 5

    def __init__(self, *args, **kargs):
        """Initialize the I2C bus"""
        super().__init__()
        self._bus = 1
        self._smbus = SMBus(self._bus)

    @_retry_wrapper
    def _i2c_write_byte(self, addr, data):   # i2C 写系列函数
        self._debug("_i2c_write_byte: [0x{:02X}] [0x{:02X}]".format(addr, data))
        result = self._smbus.write_byte(addr, data)
        return result
            
    @_retry_wrapper
    def _i2c_write_byte_data(self, addr, reg, data):
        self._debug("_i2c_write_byte_data: [0x{:02X}] [0x{:02X}] [0x{:02X}]".format(addr, reg, data))
        return self._smbus.write_byte_data(addr, reg, data)
    
    @_retry_wrapper
    def _i2c_write_word_data(self, addr, reg, data):
        self._debug("_i2c_write_word_data: [0x{:02X}] [0x{:02X}] [0x{:04X}]".format(addr, reg, data))
        return self._smbus.write_word_data(addr, reg, data)
    
    @_retry_wrapper
    def _i2c_write_i2c_block_data(self, addr, reg, data):
        self._debug("_i2c_write_i2c_block_data: [0x{:02X}] [0x{:02X}] {}".format(addr, reg, data))
        return self._smbus.write_i2c_block_data(addr, reg, data)
    
    @_retry_wrapper
    def _i2c_read_byte(self, addr):
        self._debug("_i2c_read_byte: [0x{:02X}]".format(addr))
        return self._smbus.read_byte(addr)

    @_retry_wrapper
    def _i2c_read_i2c_block_data(self, addr, reg, num):
        self._debug("_i2c_read_i2c_block_data: [0x{:02X}] [0x{:02X}] [{}]".format(addr, reg, num))
        return self._smbus.read_i2c_block_data(addr, reg, num)

    @_retry_wrapper
    def is_ready(self, addr):
        """Check if the I2C device is ready
        
        :param addr: I2C device address
        :type addr: int
        :return: True if the I2C device is ready, False otherwise
        :rtype: bool
        """
        addresses = self.scan()
        if addr in addresses:
            return True
        else:
            return False

    def scan(self):
        """Scan the I2C bus for devices

        :return: List of I2C addresses of devices found
        :rtype: list
        """
        cmd = "i2cdetect -y %s" % self._bus
        # Run the i2cdetect command
        _, output = self.run_command(cmd)
        
        # Parse the output
        outputs = output.split('\n')[1:]
        self._debug("outputs")
        addresses = []
        for tmp_addresses in outputs:
            if tmp_addresses == "":
                continue
            tmp_addresses = tmp_addresses.split(':')[1]
            # Split the addresses into a list
            tmp_addresses = tmp_addresses.strip().split(' ')
            for address in tmp_addresses:
                if address != '--':
                    addresses.append(int(address, 16))
        self._debug("Conneceted i2c device: %s"%addresses)
        return addresses

    def send(self, send, addr):
        """Send data to the I2C device
        
        :param send: Data to send
        :type send: int/list/bytearray
        :param addr: I2C device address
        :type addr: int
        :raises: ValueError if send is not an int, list or bytearray
        """
        if isinstance(send, bytearray):
            data_all = list(send)
        elif isinstance(send, int):
            data_all = []
            d = "{:X}".format(send)
            d = "{}{}".format("0" if len(d)%2 == 1 else "", d)  # format是将()中的内容对应填入{}中，（）中的第一个参数是一个三目运算符，if条件成立则为“0”，不成立则为“”(空的意思)，第二个参数是d，此行代码意思为，当字符串为奇数位时，在字符串最强面添加‘0’，否则，不添加， 方便以下函数的应用
            for i in range(len(d)-2, -1, -2):       # 从字符串最后开始取，每次取2位
                tmp = int(d[i:i+2], 16)             # 将两位字符转化为16进制
                data_all.append(tmp)                # 添加到data_all数组中
            data_all.reverse()
        elif isinstance(send, list):
            data_all = send
        else:
            raise ValueError("send data must be int, list, or bytearray, not {}".format(type(send)))

        # Send the data
        if len(data_all) == 1:
            data = data_all[0]
            self._i2c_write_byte(addr, data)
        elif len(data_all) == 2:
            reg = data_all[0]
            data = data_all[1]
            self._i2c_write_byte_data(addr, reg, data)
        elif len(data_all) == 3:
            reg = data_all[0]
            data = (data_all[2] << 8) + data_all[1]
            self._i2c_write_word_data(addr, reg, data)
        else:
            reg = data_all[0]
            data = list(data_all[1:])
            self._i2c_write_i2c_block_data(addr, reg, data)

    def recv(self, recv, addr):
        """Receive data from I2C device
        
        :param recv: Number of bytes to receive
        :type recv: int
        :param addr: I2C device address
        :type addr: int
        :return: Received data
        :rtype: list
        """
        if isinstance(recv, int):
            result = bytearray(recv)
        elif isinstance(recv, bytearray):
            result = recv
        else:
            return False
        for i in range(len(result)):
            result[i] = self._i2c_read_byte(addr)
        return result

    def mem_write(self, data, addr, memaddr):
        """Send data to specific register of a I2C device
        
        :param data: Data to send, int, list or bytearray
        :type data: int/list/bytearray
        :param addr: I2C device address
        :type addr: int
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
            data = "%x"%data
            if len(data) % 2 == 1:
                data = "0" + data
            for i in range(0, len(data), 2):
                data_all.append(int(data[i:i+2], 16))
        else:
            raise ValueError("memery write require arguement of bytearray, list, int less than 0xFF")
        self._i2c_write_i2c_block_data(addr, memaddr, data_all)

    def mem_read(self, length, addr, memaddr):
        """Read data from specific register of a I2C device

        :param length: Number of bytes to receive
        :type length: int
        :param addr: I2C device address
        :type addr: int
        :param memaddr: Register address
        :type memaddr: int
        :return: Received bytearray data or False if error
        :rtype: bytearray/False
        """
        if isinstance(length, int):
            num = length
        elif isinstance(length, bytearray):
            num = len(length)
        else:
            return False
        result = bytearray(self._i2c_read_i2c_block_data(addr, memaddr, num))
        return result
