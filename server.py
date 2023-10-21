import uos
from wifi import CreateWifi

print("Machine: \t" + uos.uname()[4])
print("MicroPython: \t" + uos.uname()[3])


handlers = {
    "tableup": lambda: print("up"),
    "tabledown": lambda: print("down"),
    "tablestop": lambda: print("stop"),
}

wifi = CreateWifi("", "", handlers)

wifi.initialize_connection()

while True:
    wifi.listen()