from table_controller import TableController
from wifi import CreateWifi

controller = TableController(16, 17)

handlers = {
    "tableup": controller.drive_up,
    "tabledown": controller.drive_down,
    "tablestop": controller.stop,
}

wifi = CreateWifi("", "", handlers)

wifi.initialize_connection()

while True:
    wifi.listen()
