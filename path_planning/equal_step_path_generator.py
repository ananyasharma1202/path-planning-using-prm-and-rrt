from typing import List, Tuple
import numpy as np

def euclidean_distance(point1: Tuple[float, float, float], point2: Tuple[float, float, float]) -> float:
    """
    Calculate the Euclidean distance between two points.
    
    :param point1: First point (3D coordinates).
    :param point2: Second point (3D coordinates).
    :return: Euclidean distance between the two points.
    """
    return np.linalg.norm(np.array(point1) - np.array(point2))

def find_largest_distance_segment(path: List[Tuple[float, float, float]]) -> int:
    """
    Find the index of the consecutive line segment with the largest distance in a list of points.
    
    :param path: List of continuous points.
    :return: Index of the segment with the largest distance.
    """
    if len(path) < 2:
        raise ValueError("Path must have at least two points to calculate distances.")
    
    max_distance = 0
    idx = 0

    for i in range(len(path) - 1):
        distance = euclidean_distance(path[i], path[i + 1])
        if distance > max_distance:
            max_distance = distance
            idx = i
    
    return idx


def make_equal_steps(paths):
    
    max_length = 0
    for path in paths:
        if max_length < len(path):
            max_length = len(path)

    return_path = []
    for path in paths:
        

        while len(path) != max_length:

            idx = find_largest_distance_segment(path)
            
            
            middle_point = [0, 0, 0]
            for i in range(3):
                middle_point[i] = (path[idx][i] + path[idx + 1][i])/2
            middle_point = tuple(middle_point)
            
            path.insert(idx + 1, middle_point)

        return_path.append(path)
    return return_path

            




