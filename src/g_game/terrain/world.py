from g_game.terrain.chunk import Chunk


class World:
    chunks: dict

    def __init__(self):
        """
        Manages the collection of chunks in the world.
        """
        self.chunks = {}
        self.generate_world()

    def add_chunk(self, chunk_position: tuple[int, int, int], chunk: Chunk):
        """
        Adds a chunk to the world.

        Args:
            chunk_position (tuple): The (x, y, z) position of the chunk in the world.
            chunk (Chunk): The chunk object.
        """
        self.chunks[chunk_position] = chunk

    def get_chunk(self, chunk_position: tuple[int, int, int]):
        """
        Gets a chunk from the world.

        Args:
            chunk_position (tuple): The (x, y, z) position of the chunk.

        Returns:
            Chunk: The chunk object, or None if it doesn't exist.
        """
        pass

    def generate_world(self):
        """
        Generates the initial world terrain.

        (This is a stub for procedural generation or loading from a file).
        """
        self.add_chunk((0, 0, 0), Chunk())
