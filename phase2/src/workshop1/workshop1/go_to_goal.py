import math
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose

GOAL_X = 10.0
GOAL_Y = 10.0
DISTANCE_TOLERANCE = 0.1
ANGLE_TOLERANCE = 0.05
KP_LINEAR = 1.5
KP_ANGULAR = 6.0
MAX_LINEAR_SPEED = 2.0
TIMER_PERIOD = 0.05  # 20 Hz


class GoToGoalNode(Node):

    def __init__(self):
        super().__init__('go_to_goal_node')
        self.current_pose = None

        self.cmd_vel_pub = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)
        self.pose_sub = self.create_subscription(
            Pose, '/turtle1/pose', self.pose_callback, 10)
        self.timer = self.create_timer(TIMER_PERIOD, self.control_loop)

    def pose_callback(self, msg: Pose):
        self.current_pose = msg

    def control_loop(self):
        if self.current_pose is None:
            return

        dx = GOAL_X - self.current_pose.x
        dy = GOAL_Y - self.current_pose.y
        distance_error = math.sqrt(dx ** 2 + dy ** 2)

        twist = Twist()

        if distance_error < DISTANCE_TOLERANCE:
            self.cmd_vel_pub.publish(twist)
            self.get_logger().info('Goal reached!')
            self.timer.cancel()
            return

        desired_heading = math.atan2(dy, dx)
        heading_error = desired_heading - self.current_pose.theta
        heading_error = math.atan2(math.sin(heading_error), math.cos(heading_error))

        if abs(heading_error) > ANGLE_TOLERANCE:
            twist.angular.z = KP_ANGULAR * heading_error
        else:
            twist.linear.x = min(KP_LINEAR * distance_error, MAX_LINEAR_SPEED)
            twist.angular.z = KP_ANGULAR * heading_error

        self.cmd_vel_pub.publish(twist)


def main(args=None):
    rclpy.init(args=args)
    node = GoToGoalNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
