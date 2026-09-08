import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose

LINEAR_SPEED = 2.0
ANGULAR_SPEED = 1.0
TIMER_PERIOD = 0.5


class TurtleController(Node):

    def __init__(self):
        super().__init__('turtle_controller')
        self.current_pose = None

        self.cmd_vel_pub = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)
        self.pose_sub = self.create_subscription(
            Pose, '/turtle1/pose', self.pose_callback, 10)
        self.timer = self.create_timer(TIMER_PERIOD, self.timer_callback)

    def pose_callback(self, msg: Pose):
        self.current_pose = msg

    def timer_callback(self):
        twist = Twist()
        twist.linear.x = LINEAR_SPEED
        twist.angular.z = ANGULAR_SPEED
        self.cmd_vel_pub.publish(twist)

        if self.current_pose is not None:
            self.get_logger().info(
                f'x={self.current_pose.x:.2f} '
                f'y={self.current_pose.y:.2f} '
                f'theta={self.current_pose.theta:.2f}'
            )


def main(args=None):
    rclpy.init(args=args)
    node = TurtleController()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
