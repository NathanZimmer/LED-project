#!/usr/bin/python
# FUNCTION: cycles entire strip through color wheel. pulse optional 
# WARNING: make sure to terminate all other lighting programs before running.
# command line input: brightness [0, 255], wheel_speed [0, 100], pulse_speed [0, 100] - 0 disables pulse
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


# color wheel method for rainbow (taken from rpi_ws281x strandtest program)
def wheel(pos):
    if pos < 85.0:
        return Color(pos * 3, 255 - pos * 3, 0)
    elif pos < 170.0:
        pos -= 85
        return Color(255 - pos * 3, 0, pos * 3)
    else:
        pos -= 170
        return Color(0, pos * 3, 255 - pos * 3)

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

# infinte loop for color wheel 
def color_wheel_loop():
    while True:
        for i in range(255):
            for j in range(0, strip.numPixels()):
                strip.setPixelColor(j, wheel(i))
            strip.show()
            time.sleep(wheel_speed/1000.0)  


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
        wheel_speed = float(sys.argv[2])

        if wheel_speed <0 or wheel_speed > 100:
            raise IndexError
    except:
        wheel_speed = 30

    try:
        pulse_speed = float(sys.argv[3])

        if pulse_speed < 0 or pulse_speed > 100:
            raise IndexError
    except:
        pulse_speed = 0


    # initializing LED strip and running color_wheel_loop and pulse_loop in two seperate threads
    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    strip.begin()

    thread1 = threading.Thread(target=color_wheel_loop)
    thread2 = threading.Thread(target=pulse_loop)

    thread1.start()
    if pulse_speed > 0:
        thread2.start()