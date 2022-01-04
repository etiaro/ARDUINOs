# Importing Libraries
import serial
import time

arduino = serial.Serial(port='COM7', baudrate=9600, timeout=.5)


def waitForDone():
    data = arduino.read(1)
    while not bool(data):
        data = arduino.read(1)
    print(data)


def write_read(cmd, l1, l2):
    arduino.write((cmd).to_bytes(1, byteorder="big"))
    arduino.write(l1.to_bytes(4, byteorder="big", signed=True))
    arduino.write(l2.to_bytes(4, byteorder="big", signed=True))
    waitForDone()
    print("DONE!")


while True:
    nums = input("data: ").split(' ')
    cmd = int(nums[0])
    l1 = int(nums[1])
    l2 = int(nums[2])
    value = write_read(cmd, l1, l2)
