import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Imu

from imu_reader.imu_driver import ISM330DLC


class ImuNode(Node):
    def init(self):
        super().init('imunode')
        self.publisher = self.create_publisher(Imu, '/imu/data_raw', 10)
        self.imu = ISM330DLC()
        self.timer = self.create_timer(0.02, self.publish_imu)

    def publish_imu(self):
        ax, ay, az = self.imu.read_accel_mps2()
        gx, gy, gz = self.imu.read_gyro_radps()

        msg = Imu()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = 'imu_link'

        msg.orientation_covariance[0] = -1.0

        msg.angular_velocity.x = gx
        msg.angular_velocity.y = gy
        msg.angular_velocity.z = gz

        msg.linear_acceleration.x = ax
        msg.linear_acceleration.y = ay
        msg.linearacceleration.z = az

        self.publisher.publish(msg)

    def destroy_node(self):
        try:
            self.imu.close()
        finally:
            super().destroy_node()


def main(args=None):
    rclpy.init(args=args)
    node = ImuNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == 'main':
    main()