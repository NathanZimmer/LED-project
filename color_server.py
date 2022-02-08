#!/usr/bin/env python3
# FUNCTION: gets rgb value from monitor_lights.py and sets LED strip color. this program should be on the pi while monitor_lights.py is on a seperate machine.
import socket
from rpi_ws281x import *
import time

#configs:
LED_COUNT      = 300   
LED_PIN        = 18      
LED_FREQ_HZ    = 800000  
LED_DMA        = 10    
LED_BRIGHTNESS = 255     
LED_INVERT     = False   
LED_CHANNEL    = 0

# change these values
HOST = '192.168.1.69'  
PORT = 65432 


# main:
if __name__ == "__main__":
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        conn, addr = s.accept()
        with conn:
            strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
            strip.begin()

            while True:
                try:
                    data = conn.recv(1024)

                    if data == b"shutdown":
                        break

                    r = int(data[0:3])
                    g = int(data[3:6])
                    b = int(data[6:])

                    for i in range(0, strip.numPixels()):
                        strip.setPixelColor(i, Color(r, g, b))
                    strip.show()
                except Exception as e:
                    print(e)

