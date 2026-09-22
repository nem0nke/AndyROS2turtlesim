"""Basic TurtleSim movement and pose-feedback test."""

import rclpy
from rclpy.node import Node

from geometry_msgs.msg import Twist
from turtlesim.msg import Pose


MOVE_SPEED = 1.0       # TurtleSim units per second.
MOVE_SECONDS = 2.0     # Positive speed moves forward.


class MoveAndReadTest(Node):
    """Move the turtle briefly and print each reported pose."""

    def __init__(self):
        super().__init__("move_and_read_test")

        self.publisher = self.create_publisher(Twist, "/turtle1/cmd_vel", 10)
        self.subscription = self.create_subscription(
            Pose,
            "/turtle1/pose",
            self.read_pose,
            10,
        )

    def read_pose(self, pose: Pose):
        """Print TurtleSim's changing position and orientation."""
        print(f"x={pose.x:.2f}, y={pose.y:.2f}, theta={pose.theta:.2f}")

    def move(self):
        velocity = Twist()
        velocity.linear.x = MOVE_SPEED

        start_time = self.get_clock().now()

        while rclpy.ok():
            elapsed = (self.get_clock().now() - start_time).nanoseconds / 1e9

            if elapsed >= MOVE_SECONDS:
                break

            self.publisher.publish(velocity)
            rclpy.spin_once(self, timeout_sec=0.01)

        self.publisher.publish(Twist())
        print("Move-and-read test complete.")


def main():
    rclpy.init()
    node = MoveAndReadTest()

    try:
        node.move()
    except KeyboardInterrupt:
        node.publisher.publish(Twist())
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
