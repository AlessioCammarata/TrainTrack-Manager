import serial
import time

command = 'get_name\n'
ser = serial.Serial("COM5", 115200, timeout=51)


ser.write(command.encode())

response = ser.readline().decode().strip() if ser.isOpen() else ''

print(f"response : {response}")