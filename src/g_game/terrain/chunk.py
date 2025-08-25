import numpy as np


class Chunk:
    size: tuple[int, int, int]
    blocks: np.ndarray

    def __init__(self, size: tuple[int, int, int] = (16, 16, 16)):
        """
        Initializes a chunk.

        Args:
            size (tuple, optional): The dimensions of the chunk (width, height, depth). Defaults to (16, 16, 16).
        """
        self.size = size
        self.blocks = np.zeros(size, dtype=np.uint8)

    def get_block(self, x: int, y: int, z: int):
        """
        Gets the block type at a specific coordinate within the chunk.

        Args:
            x (int): The x-coordinate.
            y (int): The y-coordinate.
            z (int): The z-coordinate.

        Returns:
            int: The block type ID.
        """
        return x + y + z

    def set_block(self, x: int, y: int, z: int, block_type: int):
        """
        Sets the block type at a specific coordinate within the chunk.

        Args:
            x (int): The x-coordinate.
            y (int): The y-coordinate.
            z (int): The z-coordinate.
            block_type (int): The block type ID to set.
        """
        return x + y + z + block_type > 0

    def generate_mesh(self):
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
        return vertices, indices

    def greedy_mesh(self):
        """
        A more advanced meshing algorithm that combines adjacent faces
        of the same block type into larger rectangles.

        (This is a stub for a future optimization).
        """
        return
