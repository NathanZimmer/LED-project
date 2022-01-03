#!/usr/bin/python
# FUNCTION: rainbow effect. pulse optional.
# WARNING: make sure to terminate all other lighting programs before running.
# command line input: brightness [0, 255], rainbow_speed [0, 100], pulse_speed [0, 100] - 0 disables pulse
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

# infinite loop for rainbow (modified version of function from rpi_ws281x strandtest program)
def rainbow_loop():
    while True:
        for i in range(256*iterations):
            for j in range(strip.numPixels()):
                strip.setPixelColor(j, wheel((i+j) & 255))
            strip.show()
            time.sleep(rainbow_speed/1000.0)


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
        rainbow_speed = int(sys.argv[2])

        if rainbow_speed < 0 or rainbow_speed > 100:
            raise IndexError
    except:
        rainbow_speed = 20

    try: 
        pulse_speed = float(sys.argv[3])

        if pulse_speed < 0 or pulse_speed > 100:
            raise IndexError
    except:
        pulse_speed = 0


    # initializing LED strip and running rainbow_loop and pulse_loop in two seperate threads
    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    strip.begin()
    iterations = 1

    thread1 = threading.Thread(target=rainbow_loop)
    thread2 = threading.Thread(target=pulse_loop)

    thread1.start()
    if pulse_speed > 0:
        thread2.start()
