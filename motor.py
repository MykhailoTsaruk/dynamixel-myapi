from dynamixel_sdk import *
from enums import *

# Initialisation constants
DXL_MINIMUM_POSITION_VALUE  = 0        
DXL_MAXIMUM_POSITION_VALUE  = 4095     

# Macros
TORQUE_ENABLE               = 1  
TORQUE_DISABLE              = 0  

class Motor:

    def __init__(self, ID, packetHandler, portHandler):
        '''
        '''
        self.ID = ID
        self.packetHandler = packetHandler
        self.portHandler = portHandler
        self.present_control_mode = ControlMode.POSITION
        self.velocity_speed = 256

        self.set_control_mode_position()
        # self.disable_torque()

    # Move commands
    def move_to_possition(self, goal_position):
        # TODO: add description
        if self.present_control_mode == ControlMode.POSITION or self.present_control_mode == ControlMode.EXTENDED_POSITION:
            if self.present_control_mode == ControlMode.POSITION and (goal_position < DXL_MINIMUM_POSITION_VALUE or goal_position > DXL_MAXIMUM_POSITION_VALUE): 
                print(f"Goal position must be from {DXL_MINIMUM_POSITION_VALUE} to {DXL_MAXIMUM_POSITION_VALUE} \nbecause present control mode is POSITION")
                return 0
            
            dxl_comm_result, dxl_error = self.packetHandler.write4ByteTxRx(self.portHandler, self.ID, Address.GOAL_POSITION, goal_position)
            self.check_error(dxl_comm_result, dxl_error)
            print(f"Move from {self.get_present_possition} to {goal_position}")
            return 1
        else:
            print(f"Control mode must be POSITION or EXTENDED_POSITION \nPresent control mode: {self.present_control_mode}")
            return 0
    
    def move_use_velocity(self, direction):
        '''
        :param direction: Direction.CW or Direction.CCW
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
    
    def get_present_possition(self):
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

