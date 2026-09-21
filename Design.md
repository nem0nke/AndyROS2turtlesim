# AndyROS2turtlesim

## Overview

The program will be implemented in Python and run inside a Docker environment. Docker is being used because of compatibility issues encountered when attempting to run ROS 2 natively on macOS.

The program will provide a command-line interface for controlling a TurtleSim turtle using higher-level movement commands.

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
