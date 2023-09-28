from machine import Pin

class TableController:
    def __init__(self, up_port: int, down_port: int) -> None:
        self.up_pin = Pin(up_port, Pin.OUT)
        self.down_pin = Pin(down_port, Pin.OUT)

    def drive_up(self):
        self.up_pin.value(1)
        self.down_pin.value(0)
    
    def drive_down(self):
        self.up_pin.value(0)
        self.down_pin.value(1)

    def stop(self):
        self.up_pin.value(0)
        self.down_pin.value(0)
    