import machine
import utime

class LowLevelModemController():
    def __init__(self) -> None:
        self.uart = machine.UART(0, baudrate=115200)
        
    def send_command(self, command: str, timeout: int = 3000):
        print("Sending Command: " + command)
        encoded = str.encode("AT+" + command + "\r\n") 
        self.uart.write(encoded)
        self.wait_for_response(timeout)

    def write_to_buffer(self, content: str):
        self.uart.write(str.encode(content +'\r\n'))

    def wait_for_response(self, timeout: int = 3000):
        previous_timestamp = utime.ticks_ms()
        response = b""
        while (utime.ticks_ms() - previous_timestamp) < timeout:
            if self.uart.any():
                response = b"".join([response, self.uart.read(1)])
        try:
            print(response.decode())
        except UnicodeError:
            print(response)

    def recieve_data(self) -> str:
        buffer = bytes()
        while self.uart.any() > 0:
            buffer += self.uart.read(1)
        return buffer.decode('utf-8')
    
