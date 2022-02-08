#!/usr/bin/env python3
# class containing lighting functions for rpi_ws281x
import logging
import time
from rpi_ws281x import *


#configs:
LED_COUNT      = 300   
LED_PIN        = 18      
LED_FREQ_HZ    = 800000  
LED_DMA        = 10   
LED_BRIGHTNESS = 255     
LED_INVERT     = False   
LED_CHANNEL    = 0

class RGB:
    # creates and begins the LED strip
    def __init__(self):
        self.strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
        self.strip.begin()


    # takes int list rgb as input and sets lights to a solid color, optional color-chase mode
    def set_color(self, rgb, chase=False, chase_speed=10):
        while True: # color is set continuously instead of once so lights connected to a switch can be turned on and off 
            try:
                for i in range(0, self.strip.numPixels()):
                    self.strip.setPixelColor(i, Color(rgb[0], rgb[1], rgb[2]))
                    
                    if chase:
                        self.strip.show()
                        time.sleep(chase_speed/1000.0)

                self.strip.show()
            except Exception:
                logging.exception("")
                return
            except KeyboardInterrupt:
                return


    # calculates next color on a gradient. takes float list of current rgb, int distance, and int lists of rgb0 and rgb1
    def get_gradient(self, current_color, distance, color_0, color_1):
        if distance < 1:
            distance = 1

        return [current_color[0] + (color_1[0] - color_0[0]) / distance, current_color[1] + (color_1[1] - color_0[1]) / distance, current_color[2] + (color_1[2] - color_0[2]) / distance] 


    # creates a gradient. Takes int list start and end rgb values and offsets for each. Offsets determine how many pixels are a solid color vs how many are part of the gradient
    def set_gradient(self, rgb0, rgb1, offset_0=1, offset_1=1, chase=False, chase_speed=10):
        # preventing user from inputing offsets that are too large
        if offset_0 + offset_1 > self.strip.numPixels():
            offset_0 = int(self.strip.numPixels() / 2)
            offset_1 = int(self.strip.numPixels() / 2)

        gradient_num = self.strip.numPixels() - offset_0 - offset_1

        while True:
            try:
                current_color = rgb0
                for i in range(0, self.strip.numPixels()):
                    # setting to color 0 until offset_0 is reached
                    if i < offset_0:
                        color = Color(rgb0[0], rgb0[1], rgb0[2])

                    # setting to gradient until offset+1 is reached
                    elif i < self.strip.numPixels() - offset_1:
                        current_color = self.get_gradient(current_color, gradient_num, rgb0, rgb1)
                        color = Color(int(current_color[0]), int(current_color[1]), int(current_color[2]))

                    # setting to color 1 until the end of the strip is reached
                    else:
                        color = Color(rgb1[0], rgb1[1], rgb1[2])

                    self.strip.setPixelColor(i, color)
                    
                    if chase:
                        self.strip.show()
                        time.sleep(chase_speed / 1000.0)

                self.strip.show()
            except Exception:
                logging.exception("")
                return
            except KeyboardInterrupt:
                return
    

    # transitions lights between int lists rgb0 to rgb1
    def color_fade(self, rgb0, rgb1, fade_speed=10):
        try:
            current_color = rgb0
            for i in range(0, 256):
                if i != 0:
                    current_color = self.get_gradient(current_color, 255, rgb0, rgb1)
                color = Color(int(current_color[0]), int(current_color[1]), int(current_color[2]))

                for i in range(0, self.strip.numPixels()):
                    self.strip.setPixelColor(i, color)

                self.strip.show()
                time.sleep(fade_speed/1000.0)  
        except Exception:
            logging.exception("")
            return


    # cycles between specified colors. Takes list of int rgb values (Ex: [255, 255, 0, 255, 0, 0] to fade from yellow to red) and float speed
    def set_color_fade(self, color_list, fade_speed=10):
        sorted_list = self.organize_list(color_list)

        # cycling between each color on sorted_list
        while True:
            try:
                for i in range(0, len(sorted_list)):
                    rgb0 = sorted_list[i]
                    try:
                        rgb1 = sorted_list[i+1]
                    except IndexError:
                        rgb1 = sorted_list[0]

                    self.color_fade(rgb0, rgb1, fade_speed)
            except Exception:
                logging.exception("")
                return
            except KeyboardInterrupt:
                return


    # sets multiple bands of color that move along the strip. takes int list of rgb values, number of times each color should repeat, size of the fade between colors (1 means no fade), and speed
    def set_color_band(self, color_list, iterations=1, offset=1, band_speed=10, movement=True):
        color_list = color_list * iterations
        sorted_list = self.organize_list(color_list)
        band_count = len(sorted_list)
        band_size = self.strip.numPixels() / band_count

        if offset > band_size:
            offset = band_size + 1

        pixel_list = []
        current_band = 1
        current_color = sorted_list[current_band - 1]

        # storing each rgb value in a list (a list of lists)
        for i in range(0, self.strip.numPixels()):
            if i > band_size * current_band:
                current_band += 1
                current_color = sorted_list[current_band - 1]

            if i > (band_size * current_band) - offset:
                try:
                    current_color = self.get_gradient(current_color, offset, sorted_list[current_band - 1], sorted_list[current_band])
                except IndexError:
                    current_color = self.get_gradient(current_color, offset, sorted_list[current_band - 1], sorted_list[0])

            pixel_list.append(list(map(int, current_color)))

        # setting strip if movement is false
        if movement != True:
            while True:
                try:
                    for i in range(0, self.strip.numPixels()):
                        self.strip.setPixelColor(i, Color(pixel_list[i][0], pixel_list[i][1], pixel_list[i][2]))
                    self.strip.show()
                except Exception:
                    logging.exception("")
                    return
                except KeyboardInterrupt:
                    return

        # setting strip based off of pixel_list + offset for movement if movement is tre
        while True: 
            try:
                for j in range(0, self.strip.numPixels()):
                    for i in range(0, self.strip.numPixels()):
                        current_pixel = i + j

                        if current_pixel > self.strip.numPixels() - 1:
                            current_pixel = current_pixel - self.strip.numPixels() - 1

                        self.strip.setPixelColor(current_pixel, Color(pixel_list[i][0], pixel_list[i][1], pixel_list[i][2]))

                    self.strip.show()
                    time.sleep(band_speed/1000.0)
            except Exception:
                logging.exception("")
                return
            except KeyboardInterrupt:
                return

    # setter for strip brightness
    def set_brightness(self, brightness):
        self.strip.setBrightness(brightness)
        global LED_BRIGHTNESS
        LED_BRIGHTNESS = brightness


    # takes a list and returns a list containing lists of 3 elements (ex: returns [[x, y, z], [a, b, c]]). Drops remaining elements
    def organize_list(self, color_list):
        sorted_list = []
        for i in range(0, len(color_list), 3):
            if (i + 3) <= len(color_list):
                sorted_list.append(color_list[i:i+3])
        
        return sorted_list