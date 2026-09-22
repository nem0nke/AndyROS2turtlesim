"""Basic TurtleSim turning test."""

import rclpy
from rclpy.node import Node

from geometry_msgs.msg import Twist


TURN_SPEED = 0.5       # Radians per second.
TURN_SECONDS = 2.0     # Positive speed turns left.


class TurnTest(Node):
    """Publish one angular velocity command, then stop."""

    def __init__(self):
        super().__init__("turn_test")
        self.publisher = self.create_publisher(Twist, "/turtle1/cmd_vel", 10)

    def turn(self):
        velocity = Twist()
        velocity.angular.z = TURN_SPEED

        start_time = self.get_clock().now()

        while rclpy.ok():
            elapsed = (self.get_clock().now() - start_time).nanoseconds / 1e9

            if elapsed >= TURN_SECONDS:
                break

            self.publisher.publish(velocity)
            rclpy.spin_once(self, timeout_sec=0.01)

        self.publisher.publish(Twist())
        print("Turn test complete.")


def main():
    rclpy.init()
    node = TurnTest()

    try:
        node.turn()
    except KeyboardInterrupt:
        node.publisher.publish(Twist())
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
