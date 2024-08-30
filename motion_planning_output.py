def format_path(points):
    """
    Format a list of tuples into a string where each tuple is a set of coordinates,
    separated by spaces and joined by colons.

    :param points: List of tuples, where each tuple contains coordinates.
    :return: Formatted string.
    """
    # Convert each tuple to a string with coordinates separated by spaces
    formatted_points = " ; ".join(" ".join(f"{coord:.1f}" for coord in point) for point in points)
    return formatted_points

def save_paths_to_file(final_paths, file_path):
    """
    Save the paths and initial configurations to a text file in the specified format.

    :param final_paths: List of lists containing the path steps for each robot.
    :param file_path: Path to the output text file.
    """
   
    with open(file_path, 'w') as file:
        
        num_robots = len(final_paths)
        file.write(f"{num_robots}\n")

        for i in range(len(final_paths[0])):

            configuration = [path[i] for path in final_paths] 
            add_line = format_path(configuration)
            file.write(f"{add_line}\n")
   

