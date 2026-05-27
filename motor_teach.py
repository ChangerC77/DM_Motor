from DM_motor_class import *

def main():
    motor = DamiaoMotor(port='/dev/ttyACM0', slave_id=0x01, master_id=0x02)

    try:
        while True:
            motor.teach_mode()
            print(f"current position: {motor.get_position():.2f} rad", end="\r")
    except KeyboardInterrupt:
        print("\n motor stoped")

    finally:
        motor.close()

if __name__ == "__main__":
    main()