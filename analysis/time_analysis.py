import numpy as np

def calculate_statistics(times):
    """
    Calculate the mean and 95%-confidence interval for a given list of times.
    
    Args:
    - times (list of floats): Time taken in each run.
    
    Returns:
    - mean_time (float): The mean time taken.
    - confidence_interval (tuple of floats): The 95% confidence interval (lower bound, upper bound).
    """
    n = len(times)
    mean_time = np.mean(times)
    std_dev = np.std(times, ddof=1)  # Sample standard deviation (Bessel's correction)
    
    # 95% Confidence Interval calculation
    margin_of_error = 1.96 * (std_dev / np.sqrt(n))
    confidence_interval = (mean_time - margin_of_error, mean_time + margin_of_error)
    
    return mean_time, confidence_interval

def save_statistics(times, filename):
    """
    Save the statistics including each run's time, mean time, and 95%-confidence interval to a text file.
    
    Args:
    - times (list of floats): Time taken in each run.
    - filename (str): The name of the file to save the statistics.
    """
    mean_time, confidence_interval = calculate_statistics(times)
    
    with open(filename, 'w') as f:
        f.write("Time taken for each run (in seconds):\n")
        for i, time in enumerate(times):
            f.write(f"Run {i+1}: {time:.4f} seconds\n")
        
        f.write("\nSummary Statistics:\n")
        f.write(f"Average Time: {mean_time:.4f} seconds\n")
        f.write(f"95%-Confidence Interval: [{confidence_interval[0]:.4f}, {confidence_interval[1]:.4f}] seconds\n")

