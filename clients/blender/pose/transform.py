import numpy as np

keypoint_joint_map = {
    "R_Shoulder": {
        "id": 2,
        "scale": -0.5,
        "axis": "x",
        "euler": ["neck", "R_Elbow", "R_Shoulder"],
    },
    "R_Elbow": {
        "id": 3,
        "scale": -0.5,
        "axis": "z",
        "euler": ["R_Shoulder", "R_Elbow", "R_Wrist"],
    },
    "R_Wrist": {"id": 4, "scale": -1, "axis": "x", "euler": []},
    "L_Shoulder": {
        "id": 5,
        "scale": -0.5,
        "axis": "x",
        "euler": ["neck", "L_Elbow", "L_Shoulder"],
    },
    "L_Elbow": {
        "id": 6,
        "scale": -0.5,
        "axis": "z",
        "euler": ["L_Shoulder", "L_Elbow", "L_Wrist"],
    },
    "L_Wrist": {"id": 7, "scale": -1, "axis": "x", "euler": []},
    "neck": {"id": 0, "scale": 1, "axis": "x", "euler": []},
}


def unit_vector(vector):
    """Returns the unit vector of the vector."""
    return vector / np.linalg.norm(vector)


def get_angle(k1: np.ndarray, k2: np.ndarray, k3: np.ndarray):
    """
    the keypoints k1, k2, k3 are connected in this order, and the result angle (IN DEGREES) is the angle at joint k2
        ki = (xi, yi); each keypoint is a np array of x and y coords
    """
    v1 = np.subtract(k2, k1)
    v2 = np.subtract(k3, k2)
    v1_u = unit_vector(v1)
    v2_u = unit_vector(v2)
    return np.arccos(np.dot(v1_u, v2_u)) * 180.0 / np.pi
