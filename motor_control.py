from DM_motor_class import *

def main():
    motor = DamiaoMotor(port='/dev/ttyACM0', slave_id=0x01, master_id=0x02)
    try:
        while True:
            motor.control_pos_force(target_pos=2.94, speed=100, torque_limit=400.0)
            time.sleep(3)
            motor.control_pos_force(target_pos=-0.01, speed=100, torque_limit=400.0)
            time.sleep(3)
    except KeyboardInterrupt:
        print("\n motor stoped")
    finally:
        motor.close()
        
if __name__ == "__main__":
    main()