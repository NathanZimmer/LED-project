#!/usr/bin/python
# FUNCTION: turns lights on to a solid color. pulse optional.
# WARNING: make sure to terminate all other lighting programs before running.
# command line input: brightness [0, 255], r [0, 255], g [0, 255], b [0, 255], pulse_speed [0, 100] - 0 disables pulse
# ex: sudo python3 color_v2.py 255 255 255 255 0  - will give you white light on full brightness with no pulsing 
import time
import sys
from rpi_ws281x import *
import threading

LED_COUNT      = 300   
LED_PIN        = 18      
LED_FREQ_HZ    = 800000  
LED_DMA        = 10      
LED_INVERT     = False   
LED_CHANNEL    = 0 


# infinte loop for pulsing
def pulse_loop():
    decreasing = True
    while True:
        for i in range(LED_BRIGHTNESS):
            if decreasing:
                strip.setBrightness(LED_BRIGHTNESS - i)
            else: 
                strip.setBrightness(i)
            time.sleep(pulse_speed/1000.0)
        decreasing = not decreasing

# infinte loop for color (color is set continuously instead of once so lights connected to a switch can be turned on and off)
def color_loop():
    while True:
        for i in range(0, strip.numPixels()):
            strip.setPixelColor(i, Color(r, g, b))
        strip.show()
        time.sleep(20/1000.0)  


# main:
if __name__ == "__main__":
    # sets light params based on command line arguments. If input does not fall within a certain value or does not exist defaults will be used
    try:
        LED_BRIGHTNESS = int(sys.argv[1])

        if LED_BRIGHTNESS < 0 or LED_BRIGHTNESS > 255:
            raise IndexError
    except:
        LED_BRIGHTNESS = 255

    try:
        r, g, b = int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
        
        color_list = [r, g, b]
        for i in color_list:
            if i < 0 or i > 255:
                raise IndexError
    except:
        r, g, b = 255, 255, 255

    try:
        pulse_speed = float(sys.argv[5])

        if pulse_speed < 0 or pulse_speed > 100:
            raise IndexError
    except:
        pulse_speed = 0


    # initializing LED strip and running color_loop and pulse_loop in two seperate threads
    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    strip.begin()

    thread1 = threading.Thread(target=color_loop)
    thread2 = threading.Thread(target=pulse_loop)

    thread1.start()
    if pulse_speed > 0:
        thread2.start()