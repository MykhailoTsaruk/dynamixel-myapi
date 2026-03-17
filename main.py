from enums import *
from motor import *
from dynamixel_sdk import *

DEVICENAME              = '/dev/ttyUSB0'
PROTOCOL_VERSION        = 2.0
LEN_GOAL_POSITION       = 4
LEN_PRESENT_POSITION    = 4
BAUDRATE                = 57600

portHandler = PortHandler(DEVICENAME)
packetHandler = PacketHandler(PROTOCOL_VERSION)

groupSyncWrite = GroupSyncWrite(portHandler, packetHandler, Address.GOAL_POSITION, LEN_GOAL_POSITION)
groupSyncRead = GroupSyncRead(portHandler, packetHandler, Address.PRESENT_POSITION, LEN_PRESENT_POSITION)

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

motors = {}

for i in range(9):
    motors[i] = Motor(i, packet_handler, port_handler)