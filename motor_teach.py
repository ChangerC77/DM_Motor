from DM_motor_class import *
import yaml
import argparse

def main(args):
    motor = DamiaoMotor(port=args.port, slave_id=args.slave_id, master_id=args.master_id)

    try:
        while True:
            motor.teach_mode()
            print(f"current position: {motor.get_position():.2f} rad", end="\r")
    except KeyboardInterrupt:
        print("\n motor stoped")

    finally:
        motor.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', type=str, default='config/config.yaml', help='YAML file path')
    parser.add_argument('--port', type=str, default='/dev/ttyACM0')
    parser.add_argument('--baudrate', type=str, default='115200')
    parser.add_argument('--slave_id', type=str, default='0x01')
    parser.add_argument('--master_id', type=str, default='0x02')
    args = parser.parse_args()

    with open(args.config, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)
        args.port = config['motor']['port']
        args.baudrate = config['motor']['baudrate']
        args.slave_id = config['motor']['slave_id']
        args.master_id = config['motor']['master_id']
    main(args)