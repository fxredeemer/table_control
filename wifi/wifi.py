from low_level_commands import LowLevelController
from wifi.configuration import WifiConfiguration

class Wifi:
    def __init__(self, low_level_commands: LowLevelController) -> None:
        self.commands = low_level_commands

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

def CreateWifi(uuid: str, password: str) -> Wifi:
    wifi_configuration = WifiConfiguration(access_point=uuid, password=password)
    low_level_controller = LowLevelController(wifi_configuration)
    return Wifi(low_level_controller)