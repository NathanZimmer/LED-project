#!/usr/bin/python
# FUNCTION: turns lights on to a gradient. pulse optional.
# WARNING: make sure to terminate all other lighting programs before running.
# command line input: brightness [0, 255], r [0, 255], g [0, 255], b [0, 255], r1 [0, 255], g1 [0, 255], b1 [0, 255], pulse_speed [0, 100] - 0 disables pulse
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

# infinte loop for color gradient(color is set continuously instead of once so lights connected to a switch can be turned on and off)
def color_gradient_loop():
    color_mod = [(r1 - r) / LED_COUNT, (g1 - g) / LED_COUNT, (b1 - b) / LED_COUNT]
    current_mod = [0, 0, 0]

    while True:
        strip.setPixelColor(0, Color(r, g, b))

        for i in range(1, strip.numPixels()):
            for j in range(0, 3): current_mod[j] += color_mod[j]
            strip.setPixelColor(i, Color(int(r + current_mod[0]), int(g + current_mod[1]), int(b + current_mod[2])))
        current_mod = [0, 0, 0]
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
        r, g, b, r1, g1, b1 = int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5]), int(sys.argv[6]), int(sys.argv[7])
        
        color_list = [r, g, b, r1, g1, b1]
        for i in color_list:
            if i < 0 or i > 255:
                raise IndexError
    except:
        r, g, b, r1, g1, b1 = 0, 0, 0, 255, 255, 255

    try:
        pulse_speed = float(sys.argv[8])

        if pulse_speed < 0 or pulse_speed > 100:
            raise IndexError
    except:
        pulse_speed = 0


    # initializing LED strip and running color_loop and pulse_loop in two seperate threads
    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    strip.begin()

    thread1 = threading.Thread(target=color_gradient_loop)
    thread2 = threading.Thread(target=pulse_loop)

    thread1.start()
    if pulse_speed > 0:
        thread2.start()