from utils import load_config
from .node_generation import NodeGenerator
from .edge_generation import EdgeGenerator


class MapGenerator:
    def __init__(self, config_file="config.yaml"):
        self.config_data = load_config(config_file)
        self.node_gen = NodeGenerator(config_file=config_file)
        self.edge_gen = EdgeGenerator(config_file=config_file)
    
    def generate_map(self, obstacles, max_radius, obstacle_data):
        nodes = self.node_gen.generate_nodes(
            num_nodes=self.config_data['num_nodes'],
            obstacles=obstacles,
            max_robot_radius=max_radius,
            obstacle_data=obstacle_data,
            near_obstacles=self.config_data['sampling_near_obstacles'],
            visualization=self.config_data['visualize_nodes']
        )
       
        edges, edges_pair = self.generate_edges(nodes, obstacles, max_radius)

        return nodes, edges, edges_pair

    def generate_edges(self, nodes, obstacles, max_radius):
        
        edges = self.edge_gen.generate_edges(nodes, obstacles, max_radius)
        return edges


