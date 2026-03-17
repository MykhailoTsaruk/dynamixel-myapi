from enum import Enum

class Direction(Enum):
    CW  = 1
    CCW = 0

class ControlMode(Enum):
    CURRENT             = 0
    VELOCITY            = 1
    POSITION            = 3
    EXTENDED_POSITION   = 4
    CURRENT_BASED       = 5
    PWM                 = 16

class Address(Enum):
    OPERATING_MODE         = 11
    TORQUE_ENABLE          = 64
    GOAL_VELOCITY          = 104
    GOAL_POSITION          = 116   
    PRESENT_POSITION       = 132
