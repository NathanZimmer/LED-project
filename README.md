# LED-project
Small project using NeoPixel WS2812 RBG LED strips and rpi_ws281x with a raspberry pi. Follow [this](https://tutorials-raspberrypi.com/connect-control-raspberry-pi-ws2812-rgb-led-strips/) tutorial for setting up the lights and installing rpi_ws281x.

This project currently does not have a GUI, but I am working on both a deskop and mobile GUI. 


How to run:
Make sure rgb.py and rgb_server.py are in the same folder on your raspberry pi and run rgp_server.py (sudo python3 rgb_server.py) Make sure you've followed the guide [here](https://tutorials-raspberrypi.com/connect-control-raspberry-pi-ws2812-rgb-led-strips/) and installed rpi_ws281x. Once the server is running, make sure ClientNonGUI.java and RGBClient.java are in the same folder and compile and run the java file in the terminal (javac ClientNonGUI.java; java ClientNonGUI). 
