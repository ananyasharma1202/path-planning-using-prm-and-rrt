import numpy as np
from collections import deque, defaultdict
from utils import load_config
from .rrt import add_nodes

class PRM:
    def __init__(self, nodes, edge_pairs, config_file="config.yaml"):
        """
        Initialize the PRM with nodes, edge pairs, and configuration settings.

        :param nodes: List of nodes (3D coordinates as NumPy arrays).
        :param edge_pairs: List of edge pairs where each edge is a tuple of indices (start_index, end_index).
        :param config_file: Path to the configuration file.
        """
        self.original_nodes = [tuple(node) for node in nodes]  # Keep a copy of the original nodes
        self.original_edge_pairs = edge_pairs
        self.config = load_config(config_file)
        self.used_nodes = []
        self.graph = self._create_graph(self.original_nodes, self.original_edge_pairs)

    def _create_graph(self, nodes, edge_pairs):
        """
        Create a graph from the edge pairs.
        
        :param nodes: List of nodes to include in the graph.
        :param edge_pairs: List of edge pairs to include in the graph.
        :return: A dictionary representing the graph.
        """
        graph = defaultdict(list)
        for u, v in edge_pairs:
            node_u = tuple(nodes[u])  # Convert node at index u to tuple
            node_v = tuple(nodes[v])  # Convert node at index v to tuple
            graph[node_u].append(node_v)
            graph[node_v].append(node_u)
        return graph

    @staticmethod
    def euclidean_distance(point1, point2):
        """
        Calculate the Euclidean distance between two points.
        
        :param point1: First point (3D coordinates as a NumPy array).
        :param point2: Second point (3D coordinates as a NumPy array).
        :return: Euclidean distance between the two points.
        """
        return np.linalg.norm(point1 - point2)

    def nearest_point(self, point, nodes):
        """
        Find the nearest node to a given point.
        
        :param point: The reference point (3D coordinates as a NumPy array).
        :param nodes: List of nodes to search.
        :return: Tuple containing the nearest node and its distance to the reference point.
        """
        nearest = None
        min_distance = float('inf')
        
        for node in nodes:
            distance = self.euclidean_distance(point, np.array(node))  # Convert node back to np.array for distance calculation
            if distance < min_distance:
                min_distance = distance
                nearest = node
                
        return nearest, min_distance

    def bfs(self, start, end, graph):
        """
        Perform a BFS traversal to find the shortest path from start to end.
        
        :param start: Start node.
        :param end: End node.
        :param graph: Graph to use for traversal.
        :return: List of nodes representing the shortest path or None if no path exists.
        """
        if start not in graph or end not in graph:
            return None

        queue = deque([start])
        visited = {start: None}

        while queue:
            node = queue.popleft()
            if node == end:
                path = []
                while node is not None:
                    path.append(node)
                    node = visited[node]
                    
                return path[::-1]

            for neighbor in graph[node]:
                if neighbor not in visited:
                    visited[neighbor] = node
                    queue.append(neighbor)
                    
        return None

    def is_collision_free(self, path, obstacles):
        """
        Check if the given path is collision-free with respect to obstacles.
        
        :param path: List of points representing the path.
        :param obstacles: List of obstacles to avoid.
        :return: True if the path is collision-free, False otherwise.
        """
        for point in path:
            for obstacle in obstacles:
                if np.linalg.norm(np.array(point) - np.array(obstacle)) < self.config['obstacle_radius']:
                    return False
        return True

    def get_path(self, robot_configurations, max_radius, obstacles):
        """
        Generate shortest paths for all robot configurations while ensuring unique paths and collision avoidance.
        
        :param robot_configurations: List of tuples containing start and end configurations for each robot.
        :param max_radius: Maximum radius for adding new nodes.
        :param obstacles: List of obstacles to avoid when adding new nodes.
        :return: List of paths for each robot, or a warning if a path does not exist.
        """
        paths = []

        for start_pos, end_pos in robot_configurations:
            # Remove used nodes and create a new graph
            nodes_remaining = [node for node in self.original_nodes if node not in self.used_nodes]
            edge_pairs_remaining = [
                (u, v) for u, v in self.original_edge_pairs
                if tuple(self.original_nodes[u]) not in self.used_nodes and
                   tuple(self.original_nodes[v]) not in self.used_nodes
            ]
            graph = self._create_graph(nodes_remaining, edge_pairs_remaining)

            start_point, dist_start = self.nearest_point(start_pos, nodes_remaining)
            end_point, dist_end = self.nearest_point(end_pos, nodes_remaining)

            if dist_start > self.config['max_node_distance']:
                path_points = add_nodes(start_pos, start_point, max_radius, obstacles)
            else:
                path_points = [start_point]
           
            
            if dist_end > self.config['max_node_distance']:
                end_path_point = add_nodes( end_point,end_pos, max_radius, obstacles)
            else:
                end_path_point = [end_point]
                
            path = self.bfs(start_point, end_point, graph)
            if path:
                path_points.extend(path)
                path_points.extend(end_path_point)

                paths.append(path_points)
                

            else:
                print(f"Warning: No path exists between {start_point} and {end_point}")

                paths.append(None)

        return paths
