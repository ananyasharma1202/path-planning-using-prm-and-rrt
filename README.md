

# Path Planning Using PRM and RRT

## Overview

This project combines Probabilistic Roadmaps (PRM) and Rapidly-exploring Random Trees (RRT) to achieve optimal path planning for multiple robots in a 3D workspace. The roadmap is constructed by generating nodes near obstacles to ensure all paths remain accessible. Once the roadmap is created, the nodes closest to the robot's start and end configurations are identified, and the path is mapped from these configurations to the nearest nodes. Breadth-First Search (BFS) is used for path searching within the PRM, ensuring no common nodes are shared between the paths of the two robots.

## What is PRM?

Probabilistic Roadmaps (PRM) is a path planning method that involves two main phases:

1. **Roadmap Construction**: Random nodes are generated in the free space of the environment. These nodes are then connected based on certain criteria (e.g., distance between nodes) to form a roadmap.
2. **Query Phase**: Given start and goal configurations, the nearest nodes in the roadmap are found. A path is then searched within the roadmap to connect the start and goal configurations using algorithms like BFS.

## What is RRT?

Rapidly-exploring Random Trees (RRT) is a path planning algorithm that:

1. **Explores Space Rapidly**: The tree grows by randomly sampling points in the space and extending the nearest node in the tree towards these points.
2. **Ensures Feasibility**: The algorithm ensures that the path remains feasible by checking for collisions at each step.

## How to Run the Code

### Prerequisites

- Python 3.x
- `pyyaml` package
- `fcl` package
- `open3d` package

Install the `pyyaml` package if you haven't already:
```sh
pip install pyyaml
```
```sh
pip install fcl-python
```
```sh
pip install open3d
```

### Steps to Run

1. **Clone the Repository**:
   ```sh
   git clone https://github.com/yourusername/path-planning-using-prm-and-rrt.git
   cd path-planning-using-prm-and-rrt
   ```

2. **Update the Configuration File**:
   Edit the `config.yaml` file to specify the paths to your input and output files, workspace dimensions, and other parameters. Here is a sample configuration:
   ```yaml
   input_file: 
     [ 
       "/inputs/test_1.txt", 
       "/inputs/test_2.txt"
     ]  
   output_file: 
     [ 
       "/outputs/test_1.txt",
       "/outputs/test_2.txt"
     ]  
   WORKSPACE_MIN: [-50, -50, -50]
   WORKSPACE_MAX: [50, 50, 50]
   num_nodes: 3000
   minimum_distance_between_nodes: 0.2
   sampling_near_obstacles: False
   ratio_of_samples_near_obstacles: 0.1
   visualize_obstacles: False
   visualize_nodes: False
   nearest_nodes: 5
   point_check_distance: 1
   visualize_road_map: False
   max_node_distance: 0.1
   visualize_movement: False
   node_steps: 1.0
   time_output_file: './time_analysis_1k.txt'
   ```

3. **Run the Script**:
   Execute the main script with the following command:
   ```sh
   python run_motion_planning.py
   ```

### Input and Output File Formats

#### Input File Format:
The input to your program must be a text (.txt) file and follows the format below:
1. The file consists of `K + |Obs| + 2` lines, where `K` is the number of robots and `|Obs|` is the number of obstacles in the environment.
2. The first line contains two numbers separated by a single white space. The first number is the number of robots, and the second number is the number of obstacles.
3. The second line consists of `K` numbers, each separated by a white space. The `i-th` number in this line is the radius of robot-i.
4. Each of lines `3` to `K + 2` contains 6 numbers, specifying the initial and goal configurations of the `i-th` robot. The format of each line is:
   ```
   InitialConf_X InitialConf_Y InitialConf_Z ; GoalConf_X GoalConf_Y GoalConf_Z
   ```
5. Each of lines `K + 3` to `K + |Obs| + 2` contains 4 numbers separated by a white space, specifying the position of the center point and side length of the `j-th` obstacle. The format of each line is:
   ```
   CenterPt_X CenterPt_Y CenterPt_Z SideLength
   ```

#### Output File Format:
The output of your program must be a text (.txt) file that specifies the collision-free path (a sequence of line segments) for the robots to move from the given initial to goal configurations.
1. The file consists of `n + 2` lines, where `n` is the number of line segments in your path.
2. The first line is the number of line-segments.
3. The second line consists of `3K` numbers, specifying the initial configuration of each of the `K` robots. Each configuration is separated by a semicolon, while each number in a configuration is separated by a white space. The format of line-2 is:
   ```
   ConfRobot-1_X ConfRobot-1_Y ConfRobot-1_Z ; ConfRobot-2_X ConfRobot-2_Y ConfRobot-2_Z ; ... ; ConfRobot-K_X ConfRobot-K_Y ConfRobot-K_Z
   ```
4. The next `n` lines are the end configuration of each line segment. Each of these lines consists of `3K` numbers and follows the format specified for line-2 of the output file.

### Sample Input File
A sample input file is provided at `/path-planning-using-prm-and-rrt/inputs/sample.txt`.

### Visualization
A visualization example is given in the form of a video. You can refer to this video for a better understanding of how the robots move within the workspace.

<video src="https://github.com/ananyasharma1202/path-planning-using-prm-and-rrt/blob/main/inputs/1725013335.MP4" width="300" />
ffmpeg -i inputs/1725013335.MP4 -vf "fps=10,scale=320:-1:flags=lanczos" output.gif
