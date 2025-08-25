import numpy as np

from g_game.terrain.chunk import Chunk


def generate_mesh(chunk: Chunk):
    """
    Generates a mesh for a given chunk.

    This function will eventually iterate through the chunk's blocks
    and generate a mesh of the visible faces.

    For now, it returns a predefined mesh for a single cube for testing.

    Args:
        chunk (Chunk): The chunk to generate a mesh for.

    Returns:
        tuple[np.array, np.array]: A tuple containing the vertex data and the index data.
    """
    # Predefined vertices for a single cube at the origin
    # (x, y, z) coordinates for each vertex
    # fmt: off
    vertices = np.array([
        # Front face
        -0.5, -0.5,  0.5,
         0.5, -0.5,  0.5,
         0.5,  0.5,  0.5,
        -0.5,  0.5,  0.5,
        # Back face
        -0.5, -0.5, -0.5,
         0.5, -0.5, -0.5,
         0.5,  0.5, -0.5,
        -0.5,  0.5, -0.5,
    ], dtype="f4")

    indices = np.array([
        # Front face
        0, 1, 2, 2, 3, 0,
        # Back face
        4, 5, 6, 6, 7, 4,
        # Top face
        3, 2, 6, 6, 7, 3,
        # Bottom face
        0, 1, 5, 5, 4, 0,
        # Right face
        1, 5, 6, 6, 2, 1,
        # Left face
        4, 0, 3, 3, 7, 4,
    ], dtype="uint32")
    # fmt: on
    if chunk:
        return vertices, indices


def greedy_mesh(chunk: Chunk):
    """
    A more advanced meshing algorithm that combines adjacent faces
    of the same block type into larger rectangles.

    (This is a stub for a future optimization).
    """
    if chunk:
        return
