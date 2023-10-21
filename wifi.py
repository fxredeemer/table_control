import socket
import network
from dataclasses import dataclass
from typing import Callable, Dict


@dataclass
class WifiConfiguration:
    access_point: str
    password: str


class Wifi:
    def __init__(self, configuration: WifiConfiguration, handlers: Dict[str, Callable[[], None]]) -> None:
        self.handlers = handlers
        self.configuration = configuration
        self.connected = False

    def initialize_connection(self):
        print("Starting connection to ESP8266...")
        self.wlan = network.WLAN(network.STA_IF)
        self.wlan.active(True)
        self.wlan.connect(self.configuration.access_point,
                          self.configuration.password)

        print(self.wlan.ifconfig()[0])

        address = socket.getaddrinfo("0.0.0.0", 80)[0][-1]
        self.socket = socket.socket()
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind(address)
        self.socket.listen(1)

        page = open("index.html", "r")
        self.html = page.read()
        self.connected = True

    def listen(self) -> bool:
        if not self.connected:
            print("Not Connected Yet!")
            return False

        print("Waiting For connection...")
        connection, address = self.socket.accept()
        request = self.read_request(connection)
        print("client connected from", address)

        connection.send("HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n")
        connection.send(self.html)
        connection.close()

        for key, value in self.handlers.items():
            queryPart = "?" + key
            if queryPart in request:
                value()

        return True

    def read_request(self, connection):
        buffer = connection.recv(1024)
        print(buffer)
        return str(buffer)


def CreateWifi(uuid: str, password: str, handlers: Dict[str, Callable[[], None]]) -> Wifi:
    wifi_configuration = WifiConfiguration(
        access_point=uuid, password=password)
    return Wifi(wifi_configuration, handlers)
