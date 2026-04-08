import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Joy
import serial
import time

class MotorController(Node):
    def __init__(self):
        super().__init__('motor_controller')

        # Serial connection to Pico
        self.ser = serial.Serial('/dev/ttyACM0', 115200, timeout=1)
        time.sleep(2)  # wait for Pico to arm
        self.ser.flush()
        self.get_logger().info('Connected to Pico on /dev/ttyACM0')

        # State tracking to avoid spamming serial
        self.last_command = None

        # Subscribe to joy topic
        self.subscription = self.create_subscription(
            Joy, '/joy', self.joy_callback, 10)
        self.get_logger().info('Motor Controller Node Started!')

    def send_command(self, cmd):
        # Only send if command changed
        if cmd == self.last_command:
            return

        self.last_command = cmd
        self.ser.write(f"{cmd}\n".encode())
        time.sleep(0.1)
        response = self.ser.readline().decode('utf-8').strip()
        self.get_logger().info(f'Command: {cmd} | Pico: {response}')

    def joy_callback(self, msg):
        lb = msg.buttons[4]  # LB button
        rb = msg.buttons[5]  # RB button

        if lb and rb:
            self.send_command("STOP")
        elif lb:
            self.send_command("FORWARD")
        elif rb:
            self.send_command("REVERSE")
        else:
            self.send_command("STOP")

    def destroy_node(self):
        self.send_command("STOP")
        self.ser.close()
        self.get_logger().info('Serial connection closed')
        super().destroy_node()

def main(args=None):
    rclpy.init(args=args)
    node = MotorController()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()