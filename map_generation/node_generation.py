import numpy as np
import logging
from .collision_detection import add_transform, check_collision, visualise_box, create_sphere, visualise, visualise_sphere, create_box
from utils import load_config, setup_logging

class NodeGenerator:
    def __init__(self, config_file="config.yaml"):
        self.config = load_config(config_file)
        self.WORKSPACE_MIN = np.array(self.config['WORKSPACE_MIN'])
        self.WORKSPACE_MAX = np.array(self.config['WORKSPACE_MAX'])
        setup_logging()

    def sample_outside_cube(self, centre, side_length, theta):
        min_bound = centre - (0.5 * side_length)
        max_bound = centre + (0.5 * side_length)
        extended_min_bound = min_bound - theta
        extended_max_bound = max_bound + theta

        return_data = []
        for i in range(3):
            if np.random.choice(2):
                return_data.append(extended_min_bound[i] - np.random.uniform(0, 1))
            else:
                return_data.append(extended_max_bound[i] + np.random.uniform(0, 1))
        return np.array(return_data)

    def node_exists_near(self, node, nodes, radius):
        for existing_node in nodes:
            distance = np.linalg.norm(node - existing_node)
            if distance < radius:
                return True
        return False

    def generate_random_node(self):
        return np.random.uniform(self.WORKSPACE_MIN, self.WORKSPACE_MAX)

    def check_node_collision(self, node, obstacles, robot_radius):
        sphere = create_sphere(robot_radius)
        sphere_w_tf = add_transform(sphere, translation=node)

        for obstacle in obstacles:
            collision_result = check_collision(obstacle, sphere_w_tf)
            if collision_result.is_collision:
                logging.debug(f"Node {node} collides with an obstacle.")
                return False
        return True

    def generate_nodes(self, num_nodes, obstacles, max_robot_radius, obstacle_data, near_obstacles=False, visualization=False):
        nodes = []
        visual_objects = []

        nodes_near_obstacles = int(num_nodes * self.config['ratio_of_samples_near_obstacles'])
       
        if near_obstacles:
            
            
            num_nodes -= nodes_near_obstacles

            while len(nodes) < nodes_near_obstacles:
                obs = obstacle_data[np.random.choice(len(obstacle_data))]
                center = np.array(obs[:3])
                side_length = obs[3]
                sample_near_obstacle = self.sample_outside_cube(center, side_length, max_robot_radius)

                if self.check_node_collision(sample_near_obstacle, obstacles, max_robot_radius):
                    
                    if not self.node_exists_near(sample_near_obstacle, nodes, self.config['minimum_distance_between_nodes']):
                        nodes.append(sample_near_obstacle)
                        sphere = create_sphere(0.4)
                        visual_objects.append(visualise_sphere(sphere, translation=sample_near_obstacle))
        
        while len(nodes) < num_nodes + nodes_near_obstacles:
            node = self.generate_random_node()

            if self.check_node_collision(node, obstacles, max_robot_radius):
                if not self.node_exists_near(node, nodes, self.config['minimum_distance_between_nodes']):
                    nodes.append(node)
                    sphere = create_sphere(0.4)
                    visual_objects.append(visualise_sphere(sphere, translation=node))

        logging.info(f"Generated {len(nodes)} collision-free nodes.")
        
        if visualization:
            for obstacle in obstacle_data:
                center = obstacle[:3]
                side_length = obstacle[3]
                box = create_box(side_length, side_length, side_length)
                box_mesh = visualise_box(box, translation=center)
                visual_objects.append(box_mesh)
            visualise(*visual_objects)

        return nodes

