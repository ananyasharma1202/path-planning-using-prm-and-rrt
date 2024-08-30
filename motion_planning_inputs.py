import os
import logging
from typing import List, Tuple

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class MotionPlanningInput:
    def __init__(self, filepath: str):
        self.filepath = filepath
        self.num_robots = 0
        self.num_obstacles = 0
        self.robot_radii = []
        self.initial_goal_configs = []
        self.obstacles = []

    def read_input_file(self):
        if not os.path.exists(self.filepath):
            logging.error(f"Input file '{self.filepath}' does not exist.")
            raise FileNotFoundError(f"File '{self.filepath}' not found.")

        try:
            with open(self.filepath, 'r') as file:
                lines = file.readlines()

            if len(lines) < 3:
                logging.error("Input file has insufficient lines.")
                raise ValueError("Input file is missing necessary data.")

            self.num_robots, self.num_obstacles = self._parse_first_line(lines[0])
            self.robot_radii = self._parse_robot_radii(lines[1])
            self.initial_goal_configs = self._parse_robot_configs(lines[2:2+self.num_robots])
            self.obstacles = self._parse_obstacles(lines[2+self.num_robots:])

            logging.info("Successfully read and parsed the input file.")

        except Exception as e:
            logging.error(f"An error occurred while reading the input file: {e}")
            raise

    def _parse_first_line(self, line: str) -> Tuple[int, int]:
        try:
            num_robots, num_obstacles = map(int, line.split())
            if num_robots <= 0 or num_obstacles < 0:
                raise ValueError
            return num_robots, num_obstacles
        except ValueError:
            logging.error("First line must contain two positive integers: number of robots and number of obstacles.")
            raise

    def _parse_robot_radii(self, line: str) -> List[float]:
        try:
            radii = list(map(float, line.split()))
            if len(radii) != self.num_robots:
                logging.error("The number of robot radii does not match the number of robots.")
                raise ValueError("Mismatch in the number of robot radii.")
            return radii
        except ValueError:
            logging.error("Second line must contain valid floating-point numbers for robot radii.")
            raise

    def _parse_robot_configs(self, lines: List[str]) -> List[Tuple[Tuple[float, float, float], Tuple[float, float, float]]]:
        configs = []
        for i, line in enumerate(lines):
            try:
                parts = line.split(';')
                if len(parts) != 2:
                    raise ValueError
                initial = tuple(map(float, parts[0].split()))
                goal = tuple(map(float, parts[1].split()))
                if len(initial) != 3 or len(goal) != 3:
                    raise ValueError
                configs.append((initial, goal))
            except ValueError:
                logging.error(f"Invalid configuration format on line {i + 3}: {line.strip()}")
                raise
        return configs

    def _parse_obstacles(self, lines: List[str]) -> List[Tuple[float, float, float, float]]:
        obstacles = []
        for i, line in enumerate(lines):
            try:
                parts = list(map(float, line.split()))
                if len(parts) != 4:
                    raise ValueError
                obstacles.append(tuple(parts))
            except ValueError:
                logging.error(f"Invalid obstacle format on line {i + 3 + self.num_robots}: {line.strip()}")
                raise
        return obstacles

    def get_data(self):
        return {
            "num_robots": self.num_robots,
            "num_obstacles": self.num_obstacles,
            "robot_radii": self.robot_radii,
            "initial_goal_configs": self.initial_goal_configs,
            "obstacles": self.obstacles
        }

if __name__ == "__main__":
    input_file = "/Users/ananyasharma/Documents/ANU/semester_3/adv_ml/assignment_1/inputs/test_1.txt"  # Replace with your input file path
    try:
        mpi = MotionPlanningInput(input_file)
        mpi.read_input_file()
        data = mpi.get_data()
        logging.info(f"Parsed Data: {data}")
    except Exception as e:
        logging.error(f"Failed to process the input file: {e}")
