import uos
from wifi.wifi import CreateWifi

led_state = "OFF"

print()
print("Machine: \t" + uos.uname()[4])
print("MicroPython: \t" + uos.uname()[3])


handlers = {
    "tableup": lambda: print("up"),
    "tabledown": lambda: print("down"),
    "tablestop": lambda: print("stop"),
}

wifi = CreateWifi("", "", handlers)

wifi.initialize()

while True:
    response = wifi.readData()