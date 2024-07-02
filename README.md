# AST_SS24
Repository for AST_SS24 assignment projects

## Team Members

- Alisha
- Maira
- Khawaja Saad
- Subash 

# Project Setup

## Prerequisites

- ROS 2 Humble
- Python 3.10 (tested on it)

## Installation

### Install ROS 2 Packages

Install the required ROS 2 packages for `smach`:

```bash
sudo apt update
sudo apt install ros-humble-smach ros-humble-smach-msgs ros-humble-smach-ros
```
Install required libraries from the requirements.txt file:

```
pip install -r requirements.txt
```

## Script Execution

Run the following command to run the test files:

```
python3 -m unittest test_robot_logic.py 
```