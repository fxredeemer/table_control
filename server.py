import uos
import machine
import utime
from machine import Pin

led_state = "OFF"

print()
print("Machine: \t" + uos.uname()[4])
print("MicroPython: \t" + uos.uname()[3])

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


class ModemController():
    def __init__(self) -> None:
        self.timeout = 3000
        self.uart = machine.UART(0, baudrate=115200)
        
    def send_command(self, command):
        print("CMD: " + command)
        self.uart.write(command)
        self.wait_for_esp_response()
        print()

    def wait_for_esp_response(self):
        previous_timestamp = utime.ticks_ms()
        response = b""
        while (utime.ticks_ms() - previous_timestamp) < self.timeout:
            if self.uart.any():
                response = b"".join([response, self.uart.read(1)])
        print("resp:")
        try:
            print(response.decode())
        except UnicodeError:
            print(response)

    def recieve_esp_data(self):
        recv=bytes()
        while self.uart.any()>0:
            recv+=self.uart.read(1)
        res=recv.decode('utf-8')
        return res

    def connect_wifi(self, cmd):
        print("CMD: " + cmd)
        self.uart.write(cmd)
        utime.sleep(7.0)
        self.wait_for_esp_response()
        print()

    

send_command('AT\r\n')          #Test AT startup
send_command('AT+GMR\r\n')      #Check version information
send_command('AT+CIPSERVER=0\r\n')      #Check version information
send_command('AT+RST\r\n')      #Check version information
send_command('AT+RESTORE\r\n')  #Restore Factory Default Settings
send_command('AT+CWMODE?\r\n')  #Query the Wi-Fi mode
send_command('AT+CWMODE=1\r\n') #Set the Wi-Fi mode = Station mode
send_command('AT+CWMODE?\r\n')  #Query the Wi-Fi mode again
connect_wifi('AT+CWJAP="A1601","123456789104"\r\n', timeout=5000) #Connect to AP
send_command('AT+CIFSR\r\n',timeout=5000)    #Obtain the Local IP Address
send_command('AT+CIPMUX=1\r\n')    #Obtain the Local IP Address
utime.sleep(1.0)
send_command('AT+CIPSERVER=1,80\r\n')    #Obtain the Local IP Address
utime.sleep(1.0)


print ('Starting connection to ESP8266...')
while True:
    response =""
    response=recieve_esp_data()

    utime.sleep(2.0)
    if '+IPD' in response: # if the buffer contains IPD(a connection), then respond with HTML handshake
        id_index = response.find('+IPD')
        if '?led_on' in response:
            print('LED ON')
            led_state = "ON"
            led.value(1)            #Set led turn on
        if '?led_off' in response:
            print('LED OFF')
            led.value(0)            #Set led turn on
            led_state = "OFF"
        print("resp:")
        print(response)
        connection_id =  response[id_index+5]
        print("connectionId:" + connection_id)
        print ('! Incoming connection - sending webpage')
        uart0.write('AT+CIPSEND='+connection_id+',1082'+'\r\n')  #Send a HTTP response then a webpage as bytes the 108 is the amount of bytes you are sending, change this if you change the data sent below
        utime.sleep(1.0)
        uart0.write('HTTP/1.1 200 OK'+'\r\n')
        uart0.write('Content-Type: text/html'+'\r\n')
        uart0.write('Connection: close'+'\r\n')
        uart0.write(''+'\r\n')
        uart0.write('<!DOCTYPE HTML>'+'\r\n')
        html ='<html> <head> <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\"> <link rel=\"stylesheet\" href=\"https://use.fontawesome.com/releases/v5.7.2/css/all.css\" integrity=\"sha384-fnmOCqbTlWIlj8LyTjo7mOUStjsKC4pOpQbqyi7RrhN7udi9RwhKkMHpvLbHG9Sr\" crossorigin=\"anonymous\"> <style> html { font-family: Arial; display: inline-block; margin: 0px auto; text-align: center; } .button { background-color: #ce1b0e; border: none; color: white; padding: 16px 40px; text-align: center; text-decoration: none; display: inline-block; font-size: 16px; margin: 4px 2px; cursor: pointer; } .button1 { background-color: #000000; } </style> </head> <body> <h2>Raspberry Pi Pico Web Server</h2> <p>LED state: <strong>' + led_state + '</strong></p> <p> <i class=\"fas fa-lightbulb fa-3x\" style=\"color:#c81919;\"></i> <a href=\\\"?led_on\\\"><button class=\"button\">LED ON</button></a> </p> <p> <i class=\"far fa-lightbulb fa-3x\" style=\"color:#000000;\"></i> <a href=\\\"?led_off\\\"><button class=\"button button1\">LED OFF</button></a> </p> </body> </html>'
        uart0.write(html +'\r\n')
        utime.sleep(6.0)
        send_command('AT+CIPCLOSE='+ connection_id+'\r\n') # once file sent, close connection
        utime.sleep(6.0)
        response="" #reset buffer
        print ('Waiting For connection...')