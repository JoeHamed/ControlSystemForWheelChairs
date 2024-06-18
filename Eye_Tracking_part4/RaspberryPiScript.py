import socket
import sys
import os
from gpiozero import Servo
from time import sleep
from gpiozero.pins.pigpio import PiGPIOFactory
from gpiozero import DistanceSensor
from time import sleep

ultrasonic1 = DistanceSensor(echo=17, trigger=4, max_distance=300)
ultrasonic2 = DistanceSensor(echo=27, trigger=23, max_distance=300)
ultrasonic3 = DistanceSensor(echo=22, trigger=25, max_distance=300)
# Use PiGPIOFactory to control servos with gpiozero library
factory = PiGPIOFactory()

# Define the servos
servo1 = Servo(11, pin_factory=factory)  # GPIO17 ----> 11
servo2 = Servo(9, pin_factory=factory)  # GPIO27 ----> 11


def setServo1Angle(direction):
    if direction == 'true':
        angle = 57
    elif direction == 'false':
        angle = 111
    # Convert angle to value between -1 and 1
    value = (angle / 180) * 2 - 1
    servo1.value = value
    sleep(2)
    setDefaultServo1Angle()


def setServo2Angle(direction):
    if direction == 'left':
        angle = 140
    elif direction == 'right':
        angle = 30
    # Convert angle to value between -1 and 1
    value = (angle / 180) * 2 - 1
    servo2.value = value
    sleep(2)
    setDefaultServo2Angle()


def setDefaultServo1Angle():
    angle = 90
    # Convert angle to value between -1 and 1
    value = (angle / 180) * 2 - 1
    servo1.value = value
    sleep(1)


def setDefaultServo2Angle():
    angle = 90
    # Convert angle to value between -1 and 1
    value = (angle / 180) * 2 - 1
    servo2.value = value
    sleep(1)


#          [2]
#           :
#           :
# [1] - - - - - - -(LEFT)
#           :
#           :
#           :
#         (MOVE)
def create_socket():
    try:
        global host
        global port
        global s
        # servo2 at center (-1 0 1)
        initialized = 0  # first itiration
        move_flag = 0  # stopped
        host = "172.20.10.2"  # Replace with the actual IP address or hostname of your server
        port = 9988
        s = socket.socket()
        try:
            s.connect((host, port))
            while True:
                try:

                    data = s.recv(17)

                    recieved_data = data.decode('utf-8')
                    recieved_data = eval(recieved_data)
                    print(recieved_data, len(str(recieved_data)))

                except:
                    print("err")
                # print(recieved_data_decoded[0])
                if initialized == 0:  # initialization for the first time
                    setDefaultServo1Angle()
                    setDefaultServo2Angle()
                    initialized = 1
                try:
                    if not recieved_data:
                        break  # Exit the loop if no data is received
                    if recieved_data[0].lower() == 'right' and recieved_data[1] == True:  # (looking left)
                        if round(ultrasonic1.distance * 100) > 50 and round(ultrasonic2.distance * 100) > 50:
                            setServo2Angle('left')  # directions are reversed in main prog
                            sleep(0.1)
                            setServo1Angle('true')

                    elif recieved_data[0].lower() == 'left' and recieved_data[1] == True:  # (looking right)
                        if round(ultrasonic3.distance * 100) > 50 and round(ultrasonic2.distance * 100) > 50:
                            setServo2Angle('right')
                            sleep(0.1)
                            setServo1Angle('true')
                    elif recieved_data[0].lower() == 'left':
                        if round(ultrasonic3.distance * 100) > 50:
                            setServo2Angle('right')
                    elif recieved_data[0].lower() == 'right':
                        if round(ultrasonic1.distance * 100) > 50:
                            setServo2Angle('left')

                    elif recieved_data[1] == True:
                        if round(ultrasonic2.distance * 100) > 50:
                            setServo1Angle('true')
                except:
                    pass


        except socket.error as msg:
            print("Connection error: " + str(msg))
            sys.exit()

    except socket.error as msg:
        print("Socket creation error: " + str(msg))
        sys.exit()


def main():
    create_socket()


main()
servo1.close()
servo2.close()