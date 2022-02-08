#!/usr/bin/env python3
# gets rgb value from client and sets lights accordingly
import socket
import logging
import os
import time
import multiprocessing
import copy
from rgb import RGB

#configs:
HOST           = '192.168.1.69' # change this values depending on the ip of your pi
PORT           = 65432          # you may need to change this if this port is already in use


# receives message from client. Return list of bytes
def getMessage():
    data = conn.recv(8) # getting junk byte (see client file for more information)
    data = conn.recv(1024)
    data_list = []

    for byte in data:
        data_list.append(byte)

    log(f"Input from client: {data_list}")
    return data_list


# takes a string input. Prints string + current time in order to log the event
def log(message):
    os.environ['TZ'] = "Eastern Standard Time"
    current_time = time.strftime("%H:%M:%S")

    print(f"[{current_time}] {message}")


# main:
if __name__ == "__main__":
    # creating light object
    strip = RGB()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind((HOST, PORT))
            light_process = None
            copy_process = None

            # server loop
            while True:
                log("Looking for connection")
                s.listen()
                conn, addr = s.accept()

                with conn:
                    log("Client connected")

                    # connection loop
                    while True:
                        try:   
                            # taking input
                            input = getMessage()

                            # freeing microprocess if applicable
                            if light_process != None and (input[0] != 4):
                                light_process.terminate()
                                light_process.join()
                                log(light_process)

                            # interpreting input and assigning process
                            if input[0] == 0:
                                log("Setting strip to solid color")
                                light_process = multiprocessing.Process(target=strip.set_color, args=(input[1:-2], input[-2], input[-1]))
                            elif input[0] == 1:
                                log("Setting gradient")
                                light_process = multiprocessing.Process(target=strip.set_gradient, args=(input[1:4], input[4:-4], input[-4], input[-3], input[-2], input[-1]))
                            elif input[0] == 2:
                                log("Setting color fade")
                                light_process = multiprocessing.Process(target=strip.set_color_fade, args=(input[1:-1], input[-1]))
                            elif input[0] == 3:
                                log("Setting color bands")
                                light_process = multiprocessing.Process(target=strip.set_color_band, args=(input[1:-4], input[-4], input[-3], input[-2], input[-1]))
                            elif input[0] == 4:
                                log("changing brightness")

                                # until I get base manager working- instead of accessing the brightness of the currently running process, a copy is made, brightness is changed, and the process is restarted based on the copy. 
                                # This is dirty, but base managers are confusing.
                                if light_process != None:
                                    light_process.terminate()
                                    light_process.join()

                                if copy_process != None:
                                    light_process = copy.copy(copy_process)
                                
                                strip.set_brightness(input[1])
                            elif input[0] == 5:
                                log("Lights off")
                                strip.set_color([0, 0, 0])
                            
                            # starting process
                            if light_process != None:
                                copy_process = copy.copy(light_process)
                                light_process.start()

                        except ConnectionResetError as e:
                            if e.errno == 104:
                                log("Client has disconnected")
                            else:
                                logging.exception("connection_loop:")
                            break
                        except Exception:
                            logging.exception("connection_loop:")
                            break
        except Exception:
            logging.exception("server_loop:")
        except KeyboardInterrupt:
            log("Shutting down server")