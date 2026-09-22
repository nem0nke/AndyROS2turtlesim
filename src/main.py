"""
command-line TurtleSim controller.

User input is expected to be in these exact forms:
forward <distance> <speed>
backward <distance> <speed>
turn <angle_degrees> <angular_speed>
stop
exit
"""

import math

import rclpy
from rclpy.node import Node

from geometry_msgs.msg import Twist
from turtlesim.msg import Pose

from proto.turtle_command_pb2 import TurtleCommand


class TurtleController(Node):
    def __init__(self):
        super().__init__("turtle_controller")

        self.velocity_publisher = self.create_publisher(
            Twist,
            "/turtle1/cmd_vel",
            10,
        )

        self.pose_subscriber = self.create_subscription(
            Pose,
            "/turtle1/pose",
            self.get_pose,
            10,
        )

        self.pose = None

    def get_pose(self, pose: Pose):
        """Save TurtleSim's latest position and orientation."""
        self.pose = pose

    def handle_command(self, command: TurtleCommand):
        if command.type == TurtleCommand.FORWARD:
            self.move(command.value, command.speed)
        elif command.type == TurtleCommand.BACKWARD:
            self.move(-command.value, command.speed)
        elif command.type == TurtleCommand.TURN:
            self.rotate(command.value, command.speed)
        elif command.type == TurtleCommand.STOP:
            self.stop_turtle()

    def move(self, distance: float, speed: float):
        """Move a measured distance; negative distance moves backward."""
        start_x = self.pose.x
        start_y = self.pose.y

        velocity = Twist()
        velocity.linear.x = math.copysign(speed, distance)

        while rclpy.ok():
            self.velocity_publisher.publish(velocity)
            rclpy.spin_once(self, timeout_sec=0.01)

            distance_traveled = math.hypot(
                self.pose.x - start_x,
                self.pose.y - start_y,
            )

            if distance_traveled >= abs(distance):
                break

        self.stop_turtle()

    def rotate(self, angle: float, angular_speed: float):
        """Turn a measured angle in degrees; negative angle turns right."""
        target_angle = math.radians(abs(angle))
        last_theta = self.pose.theta
        total_turn = 0.0

        velocity = Twist()
        velocity.angular.z = math.copysign(angular_speed, angle)

        while rclpy.ok():
            self.velocity_publisher.publish(velocity)
            rclpy.spin_once(self, timeout_sec=0.01)

            angle_change = self.pose.theta - last_theta

            if angle_change > math.pi:
                angle_change -= 2 * math.pi
            elif angle_change < -math.pi:
                angle_change += 2 * math.pi

            total_turn += angle_change
            last_theta = self.pose.theta

            if abs(total_turn) >= target_angle:
                break

        self.stop_turtle()

    def stop_turtle(self):
        self.velocity_publisher.publish(Twist())


def parse_command(user_input: str) -> TurtleCommand:
    """Convert valid terminal input into a TurtleCommand protobuf."""
    parts = user_input.split()
    command = TurtleCommand()

    if parts[0] == "stop":
        command.type = TurtleCommand.STOP
        return command

    command.value = float(parts[1])
    command.speed = float(parts[2])

    if parts[0] == "forward":
        command.type = TurtleCommand.FORWARD
    elif parts[0] == "backward":
        command.type = TurtleCommand.BACKWARD
    elif parts[0] == "turn":
        command.type = TurtleCommand.TURN

    return command


def main():
    rclpy.init()
    controller = TurtleController()

    # Wait for TurtleSim's first pose message.
    while controller.pose is None:
        rclpy.spin_once(controller, timeout_sec=0.1)

    try:
        while rclpy.ok():
            user_input = input("> ")

            if user_input == "exit":
                break

            controller.handle_command(parse_command(user_input))

    finally:
        controller.stop_turtle()
        controller.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
