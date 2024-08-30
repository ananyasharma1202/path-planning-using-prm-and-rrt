import open3d as o3d
import numpy as np

class GraphVisualizer:
    def __init__(self, nodes, edges, obstacles):
        """
        Initialize the GraphVisualizer with nodes, edges, and obstacles.

        :param nodes: List of nodes (3D coordinates as NumPy arrays).
        :param edges: List of edges, where each edge is a tuple of indices (start_index, end_index).
        :param obstacles: List of obstacles, where each obstacle is a tuple of (center, side_length).
        """
        self.nodes = np.array(nodes)
        self.edges = edges
        self.obstacles = obstacles

    def create_box(self, center, side_length):
        """
        Create a 3D box centered at 'center' with given 'side_length'.

        :param center: Center of the box (3D coordinates as a NumPy array).
        :param side_length: Length of each side of the box.
        :return: Open3D TriangleMesh representing the box.
        """
        half_length = side_length / 2
        box = o3d.geometry.TriangleMesh.create_box(width=side_length, height=side_length, depth=side_length)
        box.compute_vertex_normals()
        box.translate(center - np.array([half_length, half_length, half_length]))
        return box

    def visualize(self):
        """
        Visualize nodes, edges, and obstacles in a 3D space using Open3D.
        """
        # Create a point cloud for nodes
        point_cloud = o3d.geometry.PointCloud()
        point_cloud.points = o3d.utility.Vector3dVector(self.nodes)
        
        # Create lines for edges
        lines = []
        for edge in self.edges:
            start_idx, end_idx = edge
            lines.append([start_idx, end_idx])
        lines = np.array(lines)

        # Create line set for edges
        line_set = o3d.geometry.LineSet()
        line_set.points = o3d.utility.Vector3dVector(self.nodes)
        line_set.lines = o3d.utility.Vector2iVector(lines)
        line_set.paint_uniform_color([0, 0, 1])  

        obstacle_meshes = []
        for obs in self.obstacles:
            center = np.array(obs[:3])
            side_length = obs[3]
            box_mesh = self.create_box(center, side_length)
            box_mesh.paint_uniform_color([1, 0, 0])  
            obstacle_meshes.append(box_mesh)

        o3d.visualization.draw_geometries([point_cloud, line_set] + obstacle_meshes)

