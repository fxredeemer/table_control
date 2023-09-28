from abc import ABC, abstractmethod
import uos
import utime
from machine import Pin
from commands import WifiController, WifiConfiguration

led_state = "OFF"

print()
print("Machine: \t" + uos.uname()[4])
print("MicroPython: \t" + uos.uname()[3])

wifi_configuration = WifiConfiguration("", "")
commands = WifiController()

commands.test_connection()
commands.checkVersion()
commands.checkServerVersion()
commands.resetServer()
commands.restoreDefaultSettings()
commands.queryWifiMode()
commands.setWifiStationMode()
commands.queryWifiMode()
commands.connectWifi(wifi_configuration)
commands.queryIP()
commands.setIPMux()
commands.setIPPort()

print ('Starting connection to ESP8266...')
while True:
    response = ""
    response = recieve_esp_data()
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