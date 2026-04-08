#include <rclcpp/rclcpp.hpp>
#include <sensor_msgs/msg/joy.hpp>
#include <geometry_msgs/msg/twist.hpp>

class JoyController : public rclcpp::Node
{
public:
  JoyController() : Node("joy_controller")
  {
    joy_sub_ = this->create_subscription<sensor_msgs::msg::Joy>(
      "/joy", 10,
      std::bind(&JoyController::joy_callback, this, std::placeholders::_1));

    cmd_pub_ = this->create_publisher<geometry_msgs::msg::Twist>("/cmd_vel", 10);

    RCLCPP_INFO(this->get_logger(), "Joy Controller started!");
    RCLCPP_INFO(this->get_logger(), "Hold LB or RB to enable control.");
  }

private:
  void joy_callback(const sensor_msgs::msg::Joy::SharedPtr msg)
  {
    auto twist = geometry_msgs::msg::Twist();

    bool LB = msg->buttons[4] == 1;
    bool RB = msg->buttons[5] == 1;

    if (LB || RB) {
      // Left stick
      double left_x  = msg->axes[0];  // Left stick X → turn
      double left_y  = msg->axes[1];  // Left stick Y → forward/back

      // Right stick
      double right_x = msg->axes[3];  // Right stick X
      double right_y = msg->axes[4];  // Right stick Y

      // Log both sticks
      RCLCPP_INFO(this->get_logger(),
        "LStick X: %.2f  Y: %.2f | RStick X: %.2f  Y: %.2f | LB: %d  RB: %d",
        left_x, left_y, right_x, right_y, LB, RB);

      // Use left stick for movement
      twist.linear.x  = left_y  * max_linear_;
      twist.angular.z = left_x  * max_angular_;

      // Optional: use right stick Y for something else (e.g. arm, camera)
      twist.linear.z  = right_y * max_linear_;
      twist.linear.y  = right_x * max_linear_;

    } else {
      twist.linear.x  = 0.0;
      twist.linear.y  = 0.0;
      twist.linear.z  = 0.0;
      twist.angular.z = 0.0;
    }

    cmd_pub_->publish(twist);
  }

  rclcpp::Subscription<sensor_msgs::msg::Joy>::SharedPtr joy_sub_;
  rclcpp::Publisher<geometry_msgs::msg::Twist>::SharedPtr cmd_pub_;

  const double max_linear_  = 0.5;
  const double max_angular_ = 1.0;
};

int main(int argc, char **argv)
{
  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared<JoyController>());
  rclcpp::shutdown();
  return 0;
}