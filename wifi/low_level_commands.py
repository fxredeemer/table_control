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

    header = 'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nConnection: close\r\n'

    def sendResponse(self, html: str, connection_id: str):
        lenght = len(self.header + html)
        self.modem_controller.send_command("AT+CIPSEND=" + connection_id + "," + str(lenght) + "\r\n")  #Send a HTTP response then a webpage as bytes the 108 is the amount of bytes you are sending, change this if you change the data sent below
        utime.sleep(1.0)
        self.modem_controller.write_to_buffer(self.header)
        self.modem_controller.write_to_buffer(html)
        utime.sleep(6.0)
        self.modem_controller.send_command('AT+CIPCLOSE=' + connection_id + '\r\n')
        utime.sleep(6.0)


    def receiveData(self) -> str:
        return self.modem_controller.recieve_data()
        