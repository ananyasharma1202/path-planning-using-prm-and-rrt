import logging
from motion_planning_inputs import MotionPlanningInput
from utils import load_config, setup_logging, path_corrector
from visualizer.scene import create_scene
#from map_generation.node_generation import generate_nodes #, get_collision_free_edges
from map_generation.map_generation import MapGenerator
from visualizer.roadmap_visualizer import GraphVisualizer
from path_planning.prm import PRM
from visualizer.path_visualizer import PathVisualizer
from path_planning.equal_step_path_generator import make_equal_steps
from motion_planning_output import save_paths_to_file
import time
from analysis.time_analysis import save_statistics


def main(input_file, output_file):

    setup_logging()  
    config_file = "config.yaml"  

    try:
       
        config = load_config(config_file)
        if not input_file or not output_file:
            logging.error("Input or output file path not specified in the config file.")
            raise ValueError("Missing input or output file path in config.")
        
        mpi = MotionPlanningInput(input_file)
        mpi.read_input_file()
        data = mpi.get_data()
        logging.info(f"Parsed Data: {data}")
       
        # Create the scene with obstacles
        obstacles = create_scene(data['obstacles'], visualize = config["visualize_obstacles"])

        map_gen = MapGenerator(config_file="config.yaml")
        nodes, edges, edges_pair = map_gen.generate_map(obstacles, 
                                            max(data['robot_radii']) + 0.01,
                                            data['obstacles'])
        logging.info(f"Successfully generated nodes and edges")
         
        if config['visualize_road_map']:
            logging.info(f"Visualizing the roadmap along with obstacles ")
            visualizer = GraphVisualizer(nodes, edges_pair, data['obstacles'])
            visualizer.visualize()

        logging.info(f"Generating the optimal path for all the robots")
    
        prm = PRM(nodes, edges_pair)
        paths = prm.get_path(data['initial_goal_configs'],
                              max(data['robot_radii']) + 0.01, obstacles) #, max(data['robot_radii']))
        
        #path_generator = PathGenerator(paths)
        #paths = path_generator.make_equal_steps()
        #paths = make_equal_steps(paths)
        #exit()

        paths = path_corrector(paths)
        final_paths = make_equal_steps(paths)
        
        if config['visualize_movement']:
            logging.info(f"Visualizing the suggested path constructed ")
            visualizer = PathVisualizer(final_paths, data['obstacles'])
            visualizer.visualize()

        save_paths_to_file(final_paths, output_file)
        logging.info(f"Motion planning completed. Results saved to {output_file}")

    except Exception as e:
        logging.error(f"An error occurred during the execution: {e}")

    
            

if __name__ == "__main__":
    
    config_file = "config.yaml"  # Path to the configuration file
    config = load_config(config_file)  # Load the configuration
    time_list = []  # Initialize a list to store processing times

    # Loop through each input file specified in the config
    for i in range(len(config['input_file'])):
        time_start = time.time()  # Record the start time
        main(config['input_file'][i], config['output_file'][i])  # Call the main function with the current input and output file
        time_end = time.time()  # Record the end time
        time_list.append(time_end - time_start)  # Calculate and store the processing time

    # Save the timing statistics to the specified output file
    save_statistics(time_list, config['time_output_file'])

     




