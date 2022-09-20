import numpy as np


def unit_vector(vector):
    """Returns the unit vector of the vector."""
    return vector / np.linalg.norm(vector)


def get_angle(k1: np.ndarray, k2: np.ndarray, k3: np.ndarray):
    """
    the keypoints k1, k2, k3 are connected in this order, and the result angle (IN DEGREES) is the angle at joint k2
        ki = (xi, yi); each keypoint is a np array of x and y coords

    Args:
        k1 (_type_): _description_
        k2 (_type_): _description_
        k3 (_type_): _description_
    """
    v1 = np.subtract(k2, k1)
    v2 = np.subtract(k3, k2)
    v1_u = unit_vector(v1)
    v2_u = unit_vector(v2)
    return np.arccos(np.dot(v1_u, v2_u)) * 180.0 / np.pi
