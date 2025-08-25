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
        # (x, y, z, u, v) coordinates for each vertex
        # fmt: off
        vertices = np.array([
            # Front face
            -0.5, -0.5,  0.5, 0.0, 0.0, # bottom left (looking from +z)
             0.5, -0.5,  0.5, 1.0, 0.0, # bottom right
             0.5,  0.5,  0.5, 1.0, 1.0, # top right
            -0.5,  0.5,  0.5, 0.0, 1.0, # top left
            # Back face
             0.5, -0.5, -0.5, 0.0, 0.0, # bottom left (looking from -z)
            -0.5, -0.5, -0.5, 1.0, 0.0, # bottom right
            -0.5,  0.5, -0.5, 1.0, 1.0, # top right
             0.5,  0.5, -0.5, 0.0, 1.0, # top left
        ], dtype="f4")

        # Indice order for block must be Counter-Clockwise b/c opengl culling.
        indices = np.array([
            # Front face (viewed from +Z)
            0, 1, 2, 2, 3, 0,
            # Back face (viewed from -Z)
            4, 5, 6, 6, 7, 4,
            # Top face (viewed from +Y)
            3, 2, 7, 7, 6, 3,
            # Bottom face (viewed from -Y)
            5, 4, 1, 1, 0, 5,
            # Right face (viewed from +X)
            1, 4, 7, 7, 2, 1,
            # Left face (viewed from -X)
            5, 0, 3, 3, 6, 5,
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
