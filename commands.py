import utime

from abc import ABC, abstractmethod
from dataclasses import dataclass
from modem_controller import LowLevelModemController

@dataclass
class WifiConfiguration:
    access_point: str
    password: str

class ICommand(ABC):
    def __init__(self, modem_controller: LowLevelModemController) -> None:
        super().__init__()
        self.modem_controller = modem_controller
        self.timeout: int = 3000

    @abstractmethod
    def execute(self):
        pass

class TestCommand(ICommand):
    def execute(self):
        self.modem_controller.send_command("")

class CheckVersion(ICommand):
    def execute(self):
        self.modem_controller.send_command("GMR")

class CheckServerVersion(ICommand):
    def execute(self):
        self.modem_controller.send_command("CIPSERVER=0")

class ResetServer(ICommand):
    def execute(self):
        self.modem_controller.send_command("RST")

class RestoreDefaultSettings(ICommand):
    def execute(self):
        self.modem_controller.send_command("RESTORE")

class QueryWifiMode(ICommand):
    def execute(self):
        self.modem_controller.send_command("CWMODE?")

class SetWifiStationMode(ICommand):
    def execute(self):
        self.modem_controller.send_command("CWMODE=1")

class QueryIP(ICommand):
    def __init__(self, modem_controller: LowLevelModemController) -> None:
        super().__init__(modem_controller)
        self.timeout = 5000

    def execute(self):
        self.modem_controller.send_command("CIFSR?")

class SetIPMux(ICommand):
    def execute(self):
        self.modem_controller.send_command("CIPMUX=1")
        utime.sleep(1.0)

class SetIPPort(ICommand):
    def execute(self):
        self.modem_controller.send_command("CIPSERVER=1,80")
        utime.sleep(1.0)

class ConnectWifi(ICommand):

    def __init__(self, modem_controller: LowLevelModemController, wifi_configuration: WifiConfiguration) -> None:
        super().__init__(modem_controller)
        self.wifi_configuration = wifi_configuration

    def execute(self):
        self.modem_controller.send_command(f'CWJAP="{self.wifi_configuration.access_point}","{self.wifi_configuration.password}"')
        utime.sleep(7.0)
        self.modem_controller.wait_for_response()


class WifiController:
    def __init__(self) -> None:
        self.modem_controller = LowLevelModemController()

    def test_connection(self):
        TestCommand(self.modem_controller).execute()

    def check_version(self):
        TestCommand(self.modem_controller).execute()

    def checkVersion(self):
        CheckVersion(self.modem_controller).execute()

    def checkServerVersion(self):
        CheckServerVersion(self.modem_controller).execute()

    def resetServer(self):
        ResetServer(self.modem_controller).execute()
    
    def restoreDefaultSettings(self):
        RestoreDefaultSettings(self.modem_controller).execute()
    
    def queryWifiMode(self):
        QueryWifiMode(self.modem_controller).execute()
    
    def setWifiStationMode(self):
        SetWifiStationMode(self.modem_controller).execute()
    
    def queryIP(self):
        QueryIP(self.modem_controller).execute()
    
    def setIPMux(self):
        SetIPMux(self.modem_controller).execute()
    
    def setIPPort(self):
        SetIPPort(self.modem_controller).execute()
    
    def connectWifi(self, wifi_configuration: WifiConfiguration):
        ConnectWifi(self.modem_controller, wifi_configuration)
        