import datetime
import serial
import time
import binascii

class LEDScreen(object):

    def __init__(self, port="/dev/ttyUSB0", device_id="018", file="01", default_message=["Welcome",""]):

        self.port = port
        self.default_message = default_message
        self.file = file
        self.device_address = "~{}~".format(device_id)
        self.connection = serial.Serial(self.port,
            baudrate=9600
        )


    def calculate_checksum(self, message):
        checksum = 0
        for el in message:
            checksum ^= el
        return chr(checksum).encode()

    def send_raw_message(self, message):
        print(binascii.hexlify(bytearray(message)))
        self.connection.write(message)

    def send_message(self, message):
        prefix = bytes.fromhex('00020103C0303031E0C180')
        end_byte = bytes.fromhex('04')
        message = prefix + message + end_byte
        message = message + self.calculate_checksum(message)
        self.send_raw_message(message)

    def clear_screen(self):
        self.send_two_line_message(["",""])

    def default(self):
        self.send_two_line_message(self.default_message)

    def send_two_line_message(self, lines=["",""]):
        default_command = bytes.fromhex('1C44')
        message = "".encode()
        
        if len(lines) == 0:
            lines = ["",""]
        elif len(lines) == 1:
            lines.append("")
        
        message = message + lines[0].ljust(22).encode() + default_command + lines[1].ljust(22).encode()
        
        self.send_message(message)


    def close(self):
        self.connection.close()

test = LEDScreen()
test.send_two_line_message("hello","world")