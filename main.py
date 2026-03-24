from enums import *
from motor import *
from dynamixel_sdk import *

DEVICENAME              = 'COM3'
PROTOCOL_VERSION        = 2.0
BAUDRATE                = 57600

portHandler = PortHandler(DEVICENAME)
packetHandler = PacketHandler(PROTOCOL_VERSION)

# Open port
if portHandler.openPort():
    print("Succeeded to open the port")
else:
    print("Failed to open the port")
    quit()

# Set port baudrate
if portHandler.setBaudRate(BAUDRATE):
    print("Succeeded to change the baudrate")
else:
    print("Failed to change the baudrate")
    quit()

motors = []

for i in range(1, 10, 1):
    motors.append(Motor(i, packetHandler, portHandler))

input()

for motor in motors:
    motor.move_to_possition(0)

input()

for motor in motors:
    motor.disable_torque()

portHandler.closePort()
