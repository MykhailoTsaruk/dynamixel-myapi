from dynamixel_sdk import *
from enums import *
from math import pi
from cord import Cord

# Initialisation constants
DXL_MINIMUM_POSITION_VALUE  = 0        
DXL_MAXIMUM_POSITION_VALUE  = 4095     

# Macros
TORQUE_ENABLE               = 1  
TORQUE_DISABLE              = 0  

class Motor:

    def __init__(self, ID, packetHandler, portHandler, resolution=4096, c_radius=10, 
                previous_position=0, turn=0):
        '''
        '''
        self.ID                     = ID
        self.packetHandler          = packetHandler
        self.portHandler            = portHandler

        self.present_control_mode   = ControlMode.POSITION
        self.velocity_speed         = 256
        
        self.resolution             = resolution
        
        self.c_radius               = c_radius
        self.c_length               = 2 * pi * self.c_radius
        self.one_pulse              = self.c_length / self.resolution
        
        self.previous_position      = previous_position
        self.turn                   = turn

        self.set_control_mode_extended_position()
        # self.disable_torque()

    # Calculate how many revolutions servo needs to make 
    def calculate_servo_rotation(self, current_length : float, new_length : float):
        length = current_length - new_length

        return int(length / self.one_pulse)
    
    # Calcute new servo position
    def calculate_servo_position(self, current_length : float, new_length : float):
        servo_rotation = self.calculate_servo_rotation(current_length=current_length, new_length=new_length)

        new_servo_position = self.get_present_position + servo_rotation

        return new_servo_position
    

    def set_new_ID(self, new_ID : int):
        if 0 <= new_ID <= 255:
            dxl_comm_result, dxl_error = self.packetHandler.write1ByteTxOnly(self.portHandler, self.ID, Address.ID, new_ID)
            if self.check_error(dxl_comm_result, dxl_error):
                self.ID = new_ID

    # Move commands
    def move_to_position(self, goal_position):
        # TODO: add description
        if self.present_control_mode == ControlMode.POSITION or self.present_control_mode == ControlMode.EXTENDED_POSITION:
            if self.present_control_mode == ControlMode.POSITION and (goal_position < DXL_MINIMUM_POSITION_VALUE or goal_position > DXL_MAXIMUM_POSITION_VALUE): 
                print(f"Goal position must be from {DXL_MINIMUM_POSITION_VALUE} to {DXL_MAXIMUM_POSITION_VALUE} \nbecause present control mode is POSITION")
                return 0
            
            print(f"Move from {self.get_present_position()} to {goal_position}")
            dxl_comm_result, dxl_error = self.packetHandler.write4ByteTxRx(self.portHandler, self.ID, Address.GOAL_POSITION, goal_position)
            self.check_error(dxl_comm_result, dxl_error)
            return 1
        else:
            print(f"Control mode must be POSITION or EXTENDED_POSITION \nPresent control mode: {self.present_control_mode}")
            return 0
    
    def move_use_velocity(self, direction):
        '''
        :param direction: Direction.CW (1) or Direction.CCW (0) Any other number ex. -1 for STOP
        '''
        # TODO: add description
        if self.present_control_mode == ControlMode.VELOCITY:
            if direction == Direction.CW:
                dxl_comm_result, dxl_error = self.packetHandler.write4ByteTxRx(self.portHandler, self.ID, Address.GOAL_VELOCITY, self.velocity_speed)
                self.check_error(dxl_comm_result, dxl_error)
                return 1
            elif direction == Direction.CCW:
                dxl_comm_result, dxl_error = self.packetHandler.write4ByteTxRx(self.portHandler, self.ID, Address.GOAL_VELOCITY, self.velocity_speed)
                self.check_error(dxl_comm_result, dxl_error)
                return 1
            else:
                dxl_comm_result, dxl_error = self.packetHandler.write4ByteTxRx(self.portHandler, self.ID, Address.GOAL_VELOCITY, 0)
                print("Incorrect direction!")
                return 0
        else:
            print(f"Control mode must be VELOCITY \nPresent control mode: {self.present_control_mode}")
            return 0


    # Error checker
    def check_error(self, dxl_comm_result, dxl_error):
        if dxl_comm_result != COMM_SUCCESS:
            print(f"{self.packetHandler.getTxRxResult(dxl_comm_result)}")
            return 1
        elif dxl_error != 0:
            print(f"{self.packetHandler.getRxPacketError(dxl_error)}")
            return 0


    # Torque control
    def enable_torque(self):
        # TODO: add description
        dxl_comm_result, dxl_error = self.packetHandler.write1ByteTxRx(self.portHandler, self.ID, Address.TORQUE_ENABLE, TORQUE_ENABLE)
        self.check_error(dxl_comm_result, dxl_error)        

    def disable_torque(self):
        # TODO: add description
        dxl_comm_result, dxl_error = self.packetHandler.write1ByteTxRx(self.portHandler, self.ID, Address.TORQUE_ENABLE, TORQUE_DISABLE)
        self.check_error(dxl_comm_result, dxl_error)
    

    # Getters
    def get_ID(self):
        return self.ID

    def get_present_control_mode(self):
        return self.present_control_mode    
    
    def get_velocity_speed(self):
        return self.velocity_speed
    
    def get_present_position(self):
        dxl_present_position, dxl_comm_result, dxl_error = self.packetHandler.read4ByteTxRx(self.portHandler, self.ID, Address.PRESENT_POSITION)
        self.check_error(dxl_comm_result, dxl_error)
        
        return dxl_present_position
    

    # Setters
    def set_velocity_speed(self, new_velocity_speed):
        '''
        :param new_velocity_speed: from 1 to 1023
        '''
        if 1 < new_velocity_speed < 1023:
            self.velocity_speed = new_velocity_speed
            return 1
        else:
            print("New velocity speed must be from 1 to 1023!")
            return 0
        
    def set_homing_offset(self, offset : int):
        dxl_comm_result, dxl_error = self.packetHandler.write4ByteTxRx(self.portHandler, self.ID, Address.HOMING_OFFSET, offset)
        if dxl_error == 0: 
            pass
        self.check_error(dxl_comm_result, dxl_error)


    # Control mods
    def set_control_mode_current(self):
        self.disable_torque()
        dxl_comm_result, dxl_error = self.packetHandler.write1ByteTxRx(self.portHandler, self.ID, Address.OPERATING_MODE, ControlMode.CURRENT)
        if dxl_error == 0: 
            self.present_control_mode = ControlMode.CURRENT
        self.check_error(dxl_comm_result, dxl_error)
        self.enable_torque()

    def set_control_mode_velocity(self):
        self.disable_torque()
        dxl_comm_result, dxl_error = self.packetHandler.write1ByteTxRx(self.portHandler, self.ID, Address.OPERATING_MODE, ControlMode.VELOCITY)
        if dxl_error == 0: 
            self.present_control_mode = ControlMode.VELOCITY
        self.check_error(dxl_comm_result, dxl_error)
        self.enable_torque()

    def set_control_mode_position(self):
        self.disable_torque()
        dxl_comm_result, dxl_error = self.packetHandler.write1ByteTxRx(self.portHandler, self.ID, Address.OPERATING_MODE, ControlMode.POSITION)
        if dxl_error == 0: 
            self.present_control_mode = ControlMode.POSITION
        self.check_error(dxl_comm_result, dxl_error)
        self.enable_torque()

    def set_control_mode_extended_position(self):
        self.disable_torque()
        dxl_comm_result, dxl_error = self.packetHandler.write1ByteTxRx(self.portHandler, self.ID, Address.OPERATING_MODE, ControlMode.EXTENDED_POSITION)
        if dxl_error == 0: 
            self.present_control_mode = ControlMode.EXTENDED_POSITION
        self.check_error(dxl_comm_result, dxl_error)        
        self.enable_torque()

    def set_control_mode_current_based(self):
        self.disable_torque()
        dxl_comm_result, dxl_error = self.packetHandler.write1ByteTxRx(self.portHandler, self.ID, Address.OPERATING_MODE, ControlMode.CURRENT_BASED)
        if dxl_error == 0: 
            self.present_control_mode = ControlMode.CURRENT_BASED
        self.check_error(dxl_comm_result, dxl_error)        
        self.enable_torque()

    def set_control_mode_pwm(self):
        self.disable_torque()
        dxl_comm_result, dxl_error = self.packetHandler.write1ByteTxRx(self.portHandler, self.ID, Address.OPERATING_MODE, ControlMode.PWM)
        if dxl_error == 0: 
            self.present_control_mode = ControlMode.PWM
        self.check_error(dxl_comm_result, dxl_error)
        self.enable_torque()
