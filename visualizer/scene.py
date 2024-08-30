import numpy as np
import fcl
import logging
from map_generation.collision_detection import create_box, visualise_box, visualise, add_transform
from utils import load_config, setup_logging

# Load configuration and logging
config_file = "config.yaml"  
config = load_config(config_file)
setup_logging()

WORKSPACE_MIN = np.array(config['WORKSPACE_MIN'])
WORKSPACE_MAX = np.array(config['WORKSPACE_MAX'])


def check_workspace_bounds(center, side_length):
    """
    Check if the obstacle is within the defined workspace boundaries.
    :param center: Center of the obstacle (tuple of length 3).
    :param side_length: Side length of the cube obstacle (scalar).
    :return: Boolean indicating if the obstacle is within bounds.
    """
    # Convert center to a NumPy array for easier manipulation
    center = np.array(center)

    # Compute the minimum and maximum coordinates for each dimension
    min_coord = center - (0.5 * side_length)
    max_coord = center + (0.5 * side_length)

    # Check if the obstacle is within the workspace bounds for all dimensions
    within_bounds = True
    
    for dim in range(3): 
        if min_coord[dim] < WORKSPACE_MIN[dim] or max_coord[dim] > WORKSPACE_MAX[dim]:
            logging.error(
                f"Obstacle at center {center} with side length {side_length} is out of bounds in dimension {dim}."
            )
            within_bounds = False
            break
        
    return within_bounds


def create_scene(obstacle_data, visualize = False):
    """
    Create a scene with obstacles based on the provided obstacle data.
    :param obstacle_data: List of tuples containing obstacle center positions and side lengths.
    :return: List of FCL CollisionObject instances representing obstacles.
    """
    obstacles = []
    visual_objects = []

   

    for obstacle in obstacle_data:

        center = obstacle[:3]
        side_length = obstacle[3]

        if check_workspace_bounds(center, side_length):
            box = create_box(side_length, side_length, side_length)
            #box_trans = fcl.Transform(np.eye(3), center)
            trans_box =  center
            box_w_tf = add_transform(box, translation = trans_box )
            obstacles.append(box_w_tf)

            box_mesh = visualise_box(box, translation=center)
            visual_objects.append(box_mesh)

    if visualize:
        visualise(*visual_objects)

    return obstacles
