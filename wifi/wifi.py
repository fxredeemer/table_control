from typing import Callable, Dict
from low_level_commands import LowLevelController
from wifi.configuration import WifiConfiguration

class Wifi:
    html ='<!DOCTYPE HTML><html> <head> <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\"> <link rel=\"stylesheet\" href=\"https://use.fontawesome.com/releases/v5.7.2/css/all.css\" integrity=\"sha384-fnmOCqbTlWIlj8LyTjo7mOUStjsKC4pOpQbqyi7RrhN7udi9RwhKkMHpvLbHG9Sr\" crossorigin=\"anonymous\"> <style> html { font-family: Arial; display: inline-block; margin: 0px auto; text-align: center; } .button { background-color: #ce1b0e; border: none; color: white; padding: 16px 40px; text-align: center; text-decoration: none; display: inline-block; font-size: 16px; margin: 4px 2px; cursor: pointer; } .button1 { background-color: #000000; } </style> </head> <body> <h2>Raspberry Pi Pico Web Server</h2> <p>LED state: <strong>' + led_state + '</strong></p> <p> <i class=\"fas fa-lightbulb fa-3x\" style=\"color:#c81919;\"></i> <a href=\\\"?led_on\\\"><button class=\"button\">LED ON</button></a> </p> <p> <i class=\"far fa-lightbulb fa-3x\" style=\"color:#000000;\"></i> <a href=\\\"?led_off\\\"><button class=\"button button1\">LED OFF</button></a> </p> </body> </html>'
    
    def __init__(self, low_level_commands: LowLevelController, handlers: Dict[str, Callable[[], None]]) -> None:
        self.commands = low_level_commands
        self.handlers = handlers

    def initialize(self):
        print ('Starting connection to ESP8266...')
        self.commands.test_connection()
        self.commands.checkVersion()
        self.commands.checkServerVersion()
        self.commands.resetServer()
        self.commands.restoreDefaultSettings()
        self.commands.queryWifiMode()
        self.commands.setWifiStationMode()
        self.commands.queryWifiMode()
        self.commands.connectWifi()
        self.commands.queryIP()
        self.commands.setIPMux()
        self.commands.setIPPort()

    def readData(self) -> None:
        print ('Waiting For connection...')
        response = self.commands.receiveData()
        
        if '+IPD' in response: # if the buffer contains IPD(a connection), then respond with HTML handshake
            print("Response:" + response)
            
            # ADD HANDLERS

            for key, value in self.handlers:
                queryPart = "?" + key
                if queryPart in response:
                    value()

            id_index = response.find('+IPD') + 5
            connection_id =  response[id_index]
                
            print("connectionId:" + connection_id)
            self.commands.sendResponse(self.html, connection_id)


def CreateWifi(uuid: str, password: str, handlers: Dict[str, Callable[[], None]]) -> Wifi:
    wifi_configuration = WifiConfiguration(access_point=uuid, password=password)
    low_level_controller = LowLevelController(wifi_configuration)
    return Wifi(low_level_controller, handlers)