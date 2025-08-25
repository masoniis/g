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
