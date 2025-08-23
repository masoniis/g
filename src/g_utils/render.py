import math

import numpy as np


def normalize(v: np.ndarray) -> np.ndarray:
    """Normalizes a vector."""
    norm = np.linalg.norm(v)
    if norm == 0:
        return v
    return v / norm


def look_at(eye: np.ndarray, target: np.ndarray, up: np.ndarray) -> np.ndarray:
    """Creates a view matrix for a camera."""
    zaxis = normalize(target - eye)
    xaxis = normalize(np.cross(zaxis, up))
    yaxis = np.cross(xaxis, zaxis)

    # Create a 4x4 view matrix
    # yapf: disable
    view_matrix = np.array([
        [xaxis[0], yaxis[0], -zaxis[0], 0],
        [xaxis[1], yaxis[1], -zaxis[1], 0],
        [xaxis[2], yaxis[2], -zaxis[2], 0],
        [-np.dot(xaxis, eye), -np.dot(yaxis, eye), np.dot(zaxis, eye), 1]
    ], dtype=np.float32)
    # yapf: enable

    return view_matrix


def create_perspective_matrix(
    fov_degrees: float, aspect_ratio: float, near: float, far: float
) -> np.ndarray:
    """
    Creates a perspective projection matrix using NumPy.

    :param fov_degrees: Field of View in degrees.
    :param aspect_ratio: The aspect ratio of the viewport (width / height).
    :param near: The near clipping plane distance.
    :param far: The far clipping plane distance.
    :return: A 4x4 NumPy array representing the perspective matrix.
    """
    # 1. Convert field of view from degrees to radians
    fov_rad = math.radians(fov_degrees)

    # 2. Calculate the tangent of half the FOV
    tan_half_fov = math.tan(fov_rad / 2.0)

    # 3. Initialize a 4x4 identity matrix
    matrix = np.zeros((4, 4), dtype=np.float32)

    # 4. Set the matrix elements according to the perspective projection formula

    # Scaling factors for x and y coordinates
    matrix[0, 0] = 1.0 / (aspect_ratio * tan_half_fov)
    matrix[1, 1] = 1.0 / (tan_half_fov)

    # Remapping z-coordinate to the [-1, 1] range
    matrix[2, 2] = -(far + near) / (far - near)
    matrix[2, 3] = -1.0  # Used for perspective division
    matrix[3, 2] = -(2.0 * far * near) / (far - near)

    return matrix
