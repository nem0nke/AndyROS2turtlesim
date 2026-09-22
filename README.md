# AndyROS2turtlesim

## Overview

The program will be implemented in Python and run inside a Docker environment. Docker is being used because of compatibility issues encountered when attempting to run ROS 2 natively on macOS.

The program will provide a command-line interface for controlling a TurtleSim turtle using higher-level movement commands.

Example: If the user inputs FORWARD 5 1.0, the program will translate that command into the turtle moving forward 5 units at a rate of 1.0 unit per second.
If the user inputs TURN -90 1.0, then program will furthermore translate that command into the turtle turning -90 degrees, or 90 degrees clockwise, at a angular velocity of 1.0 radians per second.

Program Structure
-
The program is broken down into three main components:
### Command Line Interface
* Reads commands from the user
* Uses protobuf to serialize the user command

### ROS 2 Controller
* Receives and deserializes protobuf commands
* Translate commands into movement operation that'll be performed
* Uses TurtleSim position feedback to determine when the movement is complete

### TurtleSim
* Receives velocity commands and outputs its current position and orientation back

Protobuf Communication
-
* Protobuf will serve as a interface between the user and the ROS controller, standardizing commands being sent
* Protobuf will essentially act as a middleman that will translate basic commands into something the ROS controller can read
* [Idea] This creates possibility for upgrades to the user end, such as a GUI or a mobile app

Design / Pseudocode
-
### Main Function

* Read user input from the command line.
* Read the command and its parameters.
* Call the appropriate movement function/s.
* Continue accepting commands until the user chooses to exit.

### Forward / Backward Movement

* Create a function with a distance parameter.
* Convert the requested distance into an appropriate velocity command.
* Publish the velocity to the TurtleSim.
* Use feedback from the turtle's position to determine when the requested distance has been reached.
* Stop the turtle after reaching the target.

### Turning

* Create a function with a angle parameter.
* Convert the requested angle into the appropriate angular velocity.
* Publish the rotation command to the TurtleSim
* Use the turtle's rotation feedback to determine when the requested rotation has been completed.
* Stop the turtle after reaching the target angle.

### Position Feedback

* Continuously read the TurtleSim position as it changes
* Record and output the turtle's current position and orientation.
* Compare the actual position/orientation against the expected position/orientation from the current movement command.
* Use this feedback to determine when a movement is complete.
* Output the turtle's current position to the user.

Project Pipeline
-
1. Implement initial command-line interface (protobuf)
2. Create protobuf command format
3. Create ROS 2 Controller
4. Implement */turtle1/cmd_vel* movement
5. Implement */turtle1/pose* feedback
6. Implement distance based movement and calculations
7. Implement angle-based turning and calculations
8. Connect protobuf with ROS 2 controller
