import utime

from low_level_modem_controller import LowLevelModemController
from configuration import WifiConfiguration

class LowLevelController:
    def __init__(self, configuration: WifiConfiguration) -> None:
        self.modem_controller = LowLevelModemController()
        self.configuration = configuration

    def test_connection(self):
        self.modem_controller.send_command("")

    def check_version(self):
        self.modem_controller.send_command("")

    def checkVersion(self):
        self.modem_controller.send_command("GMR")

    def checkServerVersion(self):
        self.modem_controller.send_command("CIPSERVER=0")

    def resetServer(self):
        self.modem_controller.send_command("RST")
    
    def restoreDefaultSettings(self):
        self.modem_controller.send_command("RESTORE")
    
    def queryWifiMode(self):
        self.modem_controller.send_command("CWMODE?")
    
    def setWifiStationMode(self):
        self.modem_controller.send_command("CWMODE=1")
    
    def queryIP(self):
        self.modem_controller.send_command("CIFSR?", 5000)
    
    def setIPMux(self):
        self.modem_controller.send_command("CIPMUX=1")
        utime.sleep(1.0)
    
    def setIPPort(self):
        self.modem_controller.send_command("CIPSERVER=1,80")
        utime.sleep(1.0)
    
    def connectWifi(self):
        self.modem_controller.send_command(f'CWJAP="{self.configuration.access_point}","{self.configuration.password}"')
        utime.sleep(7.0)
        self.modem_controller.wait_for_response()
        