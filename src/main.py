# ROS 2 Python library
import rclpy
from rclpy.node import Node

from geometry_msgs.msg import Twist
from turtlesim.msg import Pose

from proto.turtle_command_pb2 import TurtleCommand


class TurtleController(Node):
    """Communicates with TurtleSim and decides when movement ends."""

    def __init__(self):
            super().__init__("turtle_controller")
    
            #Store initial coordinates
            self.current_x = 0.0
            self.current_y = 0.0
            self.current_theta = 0.0
    
            #Store distance + velocity (user inputted)
            self.target_distance = 0.0 
            self.speed = 0.0
            self.moving = False
        
    
    def get_Pose(self, pose:Pose):
        #receives latest position and orientation 
        self.current_x = pose.x
        self.current_y = pose.y
        self.current_theta = pose.theta

        self.current_pose = pose

    def handle_command(self, command: TurtleCommand):
        """Reads a protobuf command and starts the requested movement."""



def parse_command(user_input: str) -> TurtleCommand | None:
    """Turn user text into a protobuf TurtleCommand."""

    # Read input and return the completed TurtleCommand.
    pass


def move(self, distance: float, speed: float): #Moves turtle forward/backward
    vel_msg = Twist()

    start_x = self.current_pose.x
    start_y = self.current_pose.y

    target_distance = abs(distance)
    if distance > 0:
        vel_msg.linear.x = abs(speed)
    else:
        vel_msg.linear.x = -abs(speed)

    while rclpy.ok():
        self.velocity

    self.stop_turtle()


def rotate(self, angle: float, angular_speed: float): #Converts proto values into rotational values
    """
    Positive angle = left.
    Negative angle = right.
    """

    vel_msg = Twist()

def main():
    """Start ROS and run the command loop."""
    rclpy.init()

    controller = TurtleController()

    

    try:
        while rclpy.ok():
            user_input = input("> ")

            if user_input == "exit":
                break

            command = parse_command(user_input)

            controller.handle_command(command)

            # Lets ROS receive updated TurtleSim Pose messages.
            rclpy.spin_once(controller, timeout_sec=0.1)

    except KeyboardInterrupt:
        pass

    finally:
        # TODO: Stop turtle before exiting.
        controller.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()