import open3d as o3d
import numpy as np

class PathVisualizer:
    def __init__(self, paths, obstacles):
        """
        Initialize the PathVisualizer with paths, robot radii, and obstacles.

        :param paths: List of paths for each robot (each path is a list of 3D points).
        :param obstacles: List of obstacles (each obstacle is represented as a tuple of (center, side_length)).
        """
        self.paths = paths
        self.obstacles = obstacles

    def create_line(self, start, end):
        """
        Create a 3D line segment between 'start' and 'end'.

        :param start: Start point of the line segment (3D coordinates as a NumPy array).
        :param end: End point of the line segment (3D coordinates as a NumPy array).
        :return: Open3D LineSet representing the line segment.
        """
        line = o3d.geometry.LineSet()
        points = np.vstack((start, end))
        lines = [[0, 1]]
        line.points = o3d.utility.Vector3dVector(points)
        line.lines = o3d.utility.Vector2iVector(lines)
        return line

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

    def generate_random_color(self):
        """
        Generate a random color in RGB format.

        :return: A list of three values representing the RGB color.
        """
        return np.random.rand(3).tolist()

    def visualize(self):
        """
        Visualize the paths, robots, and obstacles in a 3D space with color-coded straight line paths.
        """
        vis = o3d.visualization.Visualizer()
        vis.create_window()

        # Visualize obstacles
        for obstacle in self.obstacles:
            center = np.array(obstacle[:3])
            side_length = obstacle[3]
            box = self.create_box(center, side_length)
            box.paint_uniform_color([1, 0, 0])  # Color obstacles in red
            vis.add_geometry(box)

        # Visualize paths with random colors
        for path in self.paths:
            color = self.generate_random_color()  # Generate a random color
            for i in range(len(path) - 1):
                start_point = path[i]
                end_point = path[i + 1]
                line = self.create_line(start_point, end_point)
                line.paint_uniform_color(color)
                vis.add_geometry(line)

        # Update the visualizer
        vis.update_geometry(None)
        vis.poll_events()
        vis.update_renderer()
        vis.run()
        vis.destroy_window()

