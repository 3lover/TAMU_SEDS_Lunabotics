#include <rclcpp/rclcpp.hpp>
#include <sensor_msgs/msg/joy.hpp>

class MotorController : public rclcpp::Node
{
public:
  MotorController() : Node("motor_controller")
  {
    joy_sub_ = this->create_subscription<sensor_msgs::msg::Joy>(
      "/joy", 10,
      std::bind(&MotorController::joy_callback, this, std::placeholders::_1));

    RCLCPP_INFO(this->get_logger(), "Motor Controller started!");
    RCLCPP_INFO(this->get_logger(), "LB = spin left | RB = spin right");
  }

private:
  void joy_callback(const sensor_msgs::msg::Joy::SharedPtr msg)
  {
    bool LB = msg->buttons[4] == 1;
    bool RB = msg->buttons[5] == 1;

    if (LB && !RB) {
      spin_motor("LEFT", set_speed_);
    } else if (RB && !LB) {
      spin_motor("RIGHT", set_speed_);
    } else {
      stop_motor();
    }
  }

  void spin_motor(const std::string &direction, double speed)
  {
    RCLCPP_INFO(this->get_logger(),
      "Motor spinning %s at speed %.2f", direction.c_str(), speed);

    // TODO: replace with your actual motor control code
    // e.g. GPIO, PWM, CAN bus, serial, ROS2 motor driver msg
  }

  void stop_motor()
  {
    RCLCPP_INFO(this->get_logger(), "Motor stopped");

    // TODO: replace with your actual motor stop code
  }

  rclcpp::Subscription<sensor_msgs::msg::Joy>::SharedPtr joy_sub_;

  const double set_speed_ = 1.0;  // Set your desired speed here
};

int main(int argc, char **argv)
{
  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared<MotorController>());
  rclcpp::shutdown();
  return 0;
}