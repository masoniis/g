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
        np.array: A numpy array of vertex data.
    """
    # Predefined vertices for a single cube at the origin
    # (x, y, z) coordinates for each vertex
    # fmt: off
    vertices = [
        # Front face
        -0.5, -0.5,  0.5,
         0.5, -0.5,  0.5,
         0.5,  0.5,  0.5,
        -0.5,  0.5,  0.5,
        # Back face
        -0.5, -0.5, -0.5,
        -0.5,  0.5, -0.5,
         0.5,  0.5, -0.5,
         0.5, -0.5, -0.5,
        # Top face
        -0.5,  0.5, -0.5,
        -0.5,  0.5,  0.5,
         0.5,  0.5,  0.5,
         0.5,  0.5, -0.5,
        # Bottom face
        -0.5, -0.5, -0.5,
         0.5, -0.5, -0.5,
         0.5, -0.5,  0.5,
        -0.5, -0.5,  0.5,
        # Right face
         0.5, -0.5, -0.5,
         0.5,  0.5, -0.5,
         0.5,  0.5,  0.5,
         0.5, -0.5,  0.5,
        # Left face
        -0.5, -0.5, -0.5,
        -0.5, -0.5,  0.5,
        -0.5,  0.5,  0.5,
        -0.5,  0.5, -0.5,
    ]
    # fmt: on
    if chunk:
        return np.array(vertices, dtype="f4")


def greedy_mesh(chunk: Chunk):
    """
    A more advanced meshing algorithm that combines adjacent faces
    of the same block type into larger rectangles.

    (This is a stub for a future optimization).
    """
    if chunk:
        return
