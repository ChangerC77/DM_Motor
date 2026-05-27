import serial
import time
from DM_CAN import *

class DamiaoMotor:
    def __init__(self, port='/dev/ttyACM0', baudrate=115200, slave_id=0x01, master_id=0x02):
        self.SERIAL_PORT = port
        self.BAUD_RATE = baudrate
        
        # motor initialization (DM4310, CAN ID: 0x01, Master ID: 0x02)
        self.Motor1 = Motor(DM_Motor_Type.DM4310, slave_id, master_id)
        self.serial_device = serial.Serial(self.SERIAL_PORT, self.BAUD_RATE, timeout=0.5)
        self.MotorControl1 = MotorControl(self.serial_device)
        self.MotorControl1.addMotor(self.Motor1)

        # 默认先切到 Torque_Pos 模式并使能
        if self.MotorControl1.switchControlMode(self.Motor1, Control_Type.Torque_Pos):
            print("successfully switch to Torque_Pos mode")
        else:
            print("failed switch to Torque_Pos mode")
            exit()

        print("enable motor ...")
        self.MotorControl1.enable(self.Motor1)
        time.sleep(0.5)

    def get_position(self):
        current_pos = self.Motor1.getPosition()
        return current_pos

    def get_torque(self):
        current_torque = self.Motor1.getTorque()
        return current_torque

    def control_pos_force(self, target_pos, speed, torque_limit):
        # 确保当前在 Torque_Pos 模式
        if self.Motor1.NowControlMode != Control_Type.Torque_Pos:
            self.MotorControl1.switchControlMode(self.Motor1, Control_Type.Torque_Pos)
        
        self.MotorControl1.control_pos_force(self.Motor1, target_pos, speed, torque_limit)
        time.sleep(0.01)


    def teach_mode(self, label="当前点"):
        print(f"\n👉 teach mode")
        
        while True:
            # teach mode (发送 0 阻尼，使电机可完全用手自由移动)
            self.MotorControl1.control_pos_force(self.Motor1, 0.0, 0.0, 0.0)
            time.sleep(0.01)
            
            pos = self.get_position()
            torque = self.get_torque()
            print(f"  🔍 motor current position: {pos:.2f} rad | torque: {torque:.2f} N·m", end="\r")

    def close(self):
        """close safely"""
        self.MotorControl1.disable(self.Motor1)
        self.serial_device.close()
        print("motor stopped")
