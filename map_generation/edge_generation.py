import numpy as np
import logging
from .collision_detection import add_transform, check_collision, create_sphere
from .utils import load_config, setup_logging

class EdgeGenerator:
    """
    Class to generate edges between nodes in a map and ensure they are collision-free.

    Attributes:
        config (dict): Configuration parameters loaded from a YAML file.
        max_robot_radius (float): Maximum radius of the robot used for collision checking.
    """

    def __init__(self, config_file):
        """
        Initialize the EdgeGenerator with a configuration file and robot radius.

        :param config_file: Path to the configuration YAML file.
        :param max_robot_radius: Maximum radius of the robot used for collision checking.
        """
        self.config = load_config(config_file)

    def check_node_collision(self, node, obstacles, max_robot_radius):
        """
        Check if a node collides with any obstacles.

        :param node: Coordinates of the node.
        :param obstacles: List of FCL CollisionObject instances representing obstacles.
        :return: Boolean indicating if the node is collision-free.
        """
        sphere = create_sphere(max_robot_radius)
        sphere_w_tf = add_transform(sphere, translation=node)

        for obstacle in obstacles:
            collision_result = check_collision(obstacle, sphere_w_tf)
            if collision_result.is_collision:
                return False
        return True

    def generate_points(self, node1, node2, distance):
        """
        Generate points on the line from node1 to node2 with each point separated by the specified distance.

        :param node1: Starting point (3D coordinates as a NumPy array).
        :param node2: Ending point (3D coordinates as a NumPy array).
        :param distance: Distance between each generated point.
        :return: List of points (3D coordinates as NumPy arrays) on the line.
        """
        direction = node2 - node1
        length = np.linalg.norm(direction)
        unit_direction = direction / length

        num_points = int(length // distance)
        points = [node1 + i * distance * unit_direction for i in range(1, num_points + 1)]
        
        return points

    def is_collision_free_path(self, node1, node2, point_check_distance, obstacles, max_robot_radius):
        """
        Check if the path between two nodes is collision-free.

        :param node1: Starting node (3D coordinates as a NumPy array).
        :param node2: Ending node (3D coordinates as a NumPy array).
        :param point_check_distance: Distance between each point to be checked along the path.
        :param obstacles: List of FCL CollisionObject instances representing obstacles.
        :return: Boolean indicating if the path is collision-free.
        """
        points = self.generate_points(node1, node2, point_check_distance)
        
        for point in points:
            if not self.check_node_collision(point, obstacles, max_robot_radius):
                return False
        return True

    def generate_edges(self, nodes, obstacles, max_radius):
        """
        Generate edges between nodes and check for collision-free paths.

        :param nodes: List of nodes (3D coordinates as NumPy arrays).
        :param obstacles: List of FCL CollisionObject instances representing obstacles.
        :return: List of edges where each edge is represented by a tuple of node indices.
        """
        edges = []
        edges_pair = []
        for i in range(len(nodes)):
            nearest_node_indices = self.get_nearest_nodes_brute(nodes[i], nodes, self.config['nearest_nodes'])
            path_nodes_indices = []
            for nearest_node_index in nearest_node_indices:
                
                
                if nearest_node_index < i:
                    if i in edges[nearest_node_index]:
                        path_nodes_indices.append(nearest_node_index)
                else:
                    if self.is_collision_free_path(nodes[nearest_node_index], nodes[i],
                                                   self.config['point_check_distance'], obstacles, 
                                                   max_radius):
                        path_nodes_indices.append(nearest_node_index)
                        edges_pair.append((i, nearest_node_index))
            edges.append(path_nodes_indices)
        
        return edges, edges_pair

    def get_nearest_nodes_brute(self, node, nodes, k):
        """
        Find the k nearest nodes to the given node using a brute-force approach, excluding the node itself.

        :param node: The reference node (3D coordinates as a NumPy array).
        :param nodes: List of nodes to search.
        :param k: Number of nearest nodes to return.
        :return: List of indices of the k nearest nodes.
        """
        distances = np.linalg.norm(nodes - node, axis=1)
        
        # Get indices of the nearest nodes, including the node itself
        nearest_indices = np.argpartition(distances, k + 1)[:k + 1]
        
        # Exclude the node itself by removing its index (0th index)
        if len(nearest_indices) > 0:
            nearest_indices = nearest_indices[nearest_indices != np.argmin(distances)]
        
        # Ensure we have exactly k nearest nodes
        nearest_indices = nearest_indices[np.argsort(distances[nearest_indices])]
        nearest_indices = nearest_indices[:k]

        return nearest_indices


