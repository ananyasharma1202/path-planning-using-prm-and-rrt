import numpy as np
import yaml
import logging
from map_generation.collision_detection import check_collision, create_sphere
from map_generation.edge_generation import EdgeGenerator

def euclidean_distance(point1: np.ndarray, point2: np.ndarray) -> float:
    """
    Calculate the Euclidean distance between two points.
    
    :param point1: First point (3D coordinates as a NumPy array).
    :param point2: Second point (3D coordinates as a NumPy array).
    :return: Euclidean distance between the two points.
    """
    return np.linalg.norm(point1 - point2)

def load_config(config_file: str) -> dict:
    """
    Load configuration settings from a YAML file.

    :param config_file: Path to the YAML configuration file.
    :return: A dictionary containing the configuration settings.
    """
    try:
        with open(config_file, 'r') as file:
            return yaml.safe_load(file)
    except Exception as e:
        logging.error(f"Failed to load configuration file: {e}")
        raise

def adjust_direction(direction: np.ndarray, angle: float) -> np.ndarray:
    """
    Rotate the direction vector around the Z-axis by the given angle.
    
    :param direction: Original direction vector (3D).
    :param angle: Angle to rotate (in radians).
    :return: Rotated direction vector.
    """
    axis = np.array([0, 0, 1])
    rotation_matrix = np.array([
        [np.cos(angle) + axis[0]**2 * (1 - np.cos(angle)),
         axis[0] * axis[1] * (1 - np.cos(angle)) - axis[2] * np.sin(angle),
         axis[0] * axis[2] * (1 - np.cos(angle)) + axis[1] * np.sin(angle)],
        [axis[1] * axis[0] * (1 - np.cos(angle)) + axis[2] * np.sin(angle),
         np.cos(angle) + axis[1]**2 * (1 - np.cos(angle)),
         axis[1] * axis[2] * (1 - np.cos(angle)) - axis[0] * np.sin(angle)],
        [axis[2] * axis[0] * (1 - np.cos(angle)) - axis[1] * np.sin(angle),
         axis[2] * axis[1] * (1 - np.cos(angle)) + axis[0] * np.sin(angle),
         np.cos(angle) + axis[2]**2 * (1 - np.cos(angle))]
    ])
    return np.dot(rotation_matrix, direction)

def add_nodes(start_pos_, end_pos_, max_radius, obstacles):
    """
    Add nodes to the graph if the path between them is collision-free.
    Gradually move from start_pos to end_pos to create a tree and check if the path is collision-free.
    
    :param start_pos_: Starting position (3D coordinates).
    :param end_pos_: Ending position (3D coordinates).
    :param max_radius: Maximum radius for collision checking.
    :param obstacles: List of obstacles.
    :return: List of new nodes and edge pairs added.
    """
    start_pos = np.array(start_pos_)
    end_pos = np.array(end_pos_)
    
    return_points = []

    # Load configuration and initialize edge generator
    config_file = "config.yaml"
    config = load_config(config_file)
    edge_gen = EdgeGenerator(config_file=config_file)

    # Check if the start and end positions are collision-free
    if not edge_gen.check_node_collision(start_pos, obstacles, max_radius):
        logging.warning(f"Start position {start_pos_} is in collision.")
        return return_points

    if not edge_gen.check_node_collision(end_pos, obstacles, max_radius):
        logging.warning(f"End position {end_pos_} is in collision.")
        return return_points

    '''
    # Check if the direct path between start and end is collision-free
    if edge_gen.is_collision_free_path(start_pos, end_pos,
                                       config['point_check_distance'], obstacles, max_radius):
        return_points.append((start_pos_, end_pos_))
        logging.info(f"Direct path from {start_pos_} to {end_pos_} is collision-free.")
        return return_points
    '''

    # If direct path is not collision-free, attempt to find a path by adjusting the direction
    
    current_pos = start_pos
    direction = end_pos - start_pos
    distance = np.linalg.norm(direction)

    while np.linalg.norm(current_pos - end_pos) > config['point_check_distance']:
        step = min(config['node_steps'], distance)
        direction = end_pos - current_pos
        distance = np.linalg.norm(direction)
        
        if distance < step:
            step = distance
        
        new_pos = current_pos + (direction / distance) * step

        # Check if the new position is collision-free
        if edge_gen.check_node_collision(new_pos, obstacles, max_radius):
            return_points.append((tuple(current_pos), tuple(new_pos)))
            current_pos = new_pos
        else:
            logging.debug(f"Position {new_pos} is in collision. Adjusting direction...")
            for angle in np.linspace(0, 2 * np.pi, num=36):
                rotated_direction = adjust_direction(direction, angle)
                new_pos = current_pos + (rotated_direction / np.linalg.norm(rotated_direction)) * step

                if edge_gen.check_node_collision(new_pos, obstacles, max_radius):
                    return_points.append((tuple(current_pos), tuple(new_pos)))
                    current_pos = new_pos
                    break
            else:
                logging.error(f"No collision-free position found. Adjusting path failed.")
                break

    # Add final edge from last position to end_pos
    if edge_gen.is_collision_free_path(current_pos, end_pos, config['point_check_distance'], obstacles, max_radius):
        return_points.append((tuple(current_pos), end_pos_))
        
  
    return return_points
