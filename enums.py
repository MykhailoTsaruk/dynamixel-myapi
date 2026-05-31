class Direction():
    CW  = 1
    CCW = 0

class ControlMode():
    CURRENT             = 0
    VELOCITY            = 1
    POSITION            = 3
    EXTENDED_POSITION   = 4
    CURRENT_BASED       = 5
    PWM                 = 16

class Address():
    ID                      = 7
    OPERATING_MODE          = 11
    HOMING_OFFSET           = 20
    TORQUE_ENABLE           = 64
    GOAL_VELOCITY           = 104
    GOAL_POSITION           = 116   
    PRESENT_POSITION        = 132
