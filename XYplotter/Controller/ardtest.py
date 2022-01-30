# Importing Libraries
import serial
import time

#TODO!!! XOR CONTROL BIT 

arduino = serial.Serial(port='COM7', baudrate=9600, timeout=.5)


def waitForDone():
    data = arduino.read(1)
    while not bool(data):
        data = arduino.read(1)
    print(data)


queSize = 0
def write_read(cmd, l1, l2):
    global queSize
    arduino.write((cmd).to_bytes(1, byteorder="big"))
    arduino.write(l1.to_bytes(3, byteorder="big", signed=True))
    arduino.write(l2.to_bytes(3, byteorder="big", signed=True))
    queSize += 1
    if queSize == 10:
        queSize = 0
        waitForDone()
    print("DONE!")


while True:
    nums = input("data: ").split(' ')
    cmd = int(nums[0])
    l1 = int(nums[1])
    l2 = int(nums[2])
    if cmd==3: 
        queSize=0 #thats how it's done on arduino
    value = write_read(cmd, l1, l2)
