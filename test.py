import numpy as np
import matplotlib.pyplot as plt
from itertools import combinations

def is_parallelogram(points, threshold):
    points = np.array(points)
    vectors = np.diff(points, axis=0)

    if len(vectors) >= 4:
        return np.all(np.abs(np.cross(vectors[1], vectors[3])) < threshold)
    else:
        return False

def find_parallelograms(data_points, threshold):
    parallelograms = []

    for combination in combinations(data_points, 4):
        if is_parallelogram(combination, threshold):
            parallelograms.append(combination)

    return parallelograms

def plot_data_and_parallelograms(data_points, parallelograms):
    data_points = np.array(data_points)

    plt.scatter(data_points[:, 0], data_points[:, 1], color='blue', label='Data Points')

    for parallelogram in parallelograms:
        parallelogram = np.array(parallelogram)
        parallelogram = np.vstack([parallelogram, parallelogram[0]])  # Close the loop
        plt.plot(parallelogram[:, 0], parallelogram[:, 1], color='red', linestyle='-', linewidth=2, label='Parallelogram')

    plt.title('Data Points and Parallelograms')
    plt.xlabel('X-axis')
    plt.ylabel('Y-axis')
    plt.legend()
    plt.show()

# Example usage:
data_points = [
    (1, 2), (2, 4), (3, 2),
    (4, 4), (5, 2), (6, 6),
    (7, 4), (8, 6)
]
threshold = 0.1

parallelograms = find_parallelograms(data_points, threshold)
plot_data_and_parallelograms(data_points, parallelograms)
