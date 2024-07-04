import numpy as np

def add_noise_to_points(points, amount):
    noise = np.random.normal(0, amount, points.shape)
    return points + noise

def vary_points_from_edges(points, amount):
    variation = np.random.uniform(-amount, amount, points.shape)
    return points + variation