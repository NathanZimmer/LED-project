#!/usr/bin/python
# FUNCTION: gets average of color on screen and sends it to raspberry pi running color_server.py for display to LEDs. color_server.py should be on the pi, while this program is on a seperate device.
# screenshots of your main monitor are taken, compressed down to a specified size, averaged, and then sent to color_server. optionally, you can crop a set amount of pixels off of the top, bottom, left, and right of the screenshot. these calculations are done before the image is compressed.
import paramiko
import time
from PIL import ImageGrab
import socket

# ssh comfig (change these)
host = "192.168.1.69"
port = 22
username = "pi"
password = "raspberry"
file_location = "RGB/monitor_control/color_server.py" # change this to directory of color_server.py on your raspberry pi

# server config (change these too)
HOST = '192.168.1.69'
PORT = 65432

# color recording settings
# cropping may help image represent colors on screen better. Ex: cropping out UI elements of videogames
verticle_res = 1440
horizontal_res = 2560
width_resize = 16
height_resize = 9
crop_x_left = 500
crop_x_right = 500
crop_y_top = 300
crop_y_bottom = 300
#wait_time = 1 / 60


# starts server using ssh
def start_server():
    # setting up ssh
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(host, port, username, password)

    # starting server and killing other lighing programs
    stdin, stdout, stderr = ssh.exec_command("sudo pkill python; sudo python3 " + file_location)
    ssh.close()
    time.sleep(0.5)


#main logic:
if __name__ == "__main__":
    start_server()
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))

        try:
            while True:
                screenshot = ImageGrab.grab().crop((crop_x_left, crop_y_top, horizontal_res - crop_x_right, verticle_res - crop_y_bottom)).resize((width_resize, height_resize)).convert("RGB")
                r_average = 0
                g_average = 0
                b_average = 0

                for i in range(width_resize):
                    for j in range(height_resize):
                        r, g, b = screenshot.getpixel((i - 1, j - 1))
                        r_average += r
                        g_average += g
                        b_average += b

                r_average = "{0:0=3d}".format(int(r_average / (width_resize * height_resize)))
                g_average = "{0:0=3d}".format(int(g_average / (width_resize * height_resize)))
                b_average = "{0:0=3d}".format(int(b_average / (width_resize * height_resize)))

                package = str(r_average + g_average + b_average)
                s.sendall(package.encode('utf-8'))
                #time.sleep(wait_time)
        except KeyboardInterrupt:
            print("keyboard inturupt, goodbye")
            s.sendall(b"shutdown")
            time.sleep(3)
        except Exception as e:
            print(e)
