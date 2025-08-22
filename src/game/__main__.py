import glfw
import numpy as np
from OpenGL.GL import (
    GL_COLOR_BUFFER_BIT,
    GL_FLOAT,
    GL_LINES,
    GL_MODELVIEW,
    GL_PROJECTION,
    GL_UNSIGNED_INT,
    GL_VERTEX_ARRAY,
    glClear,
    glDrawElements,
    glEnableClientState,
    glLoadIdentity,
    glMatrixMode,
    glOrtho,
    glVertexPointer,
)

from gutils import eprint


def main():
    def error_callback(error_code, description):
        eprint(f"GLFW Error {error_code}: {description}")

    glfw.set_error_callback(error_callback)

    if not glfw.init():
        eprint("GLFW failed to initialize!")
        return

    # Create a windowed mode window and its OpenGL context
    window = glfw.create_window(640, 480, "Hello World", None, None)
    if not window:
        glfw.terminate()
        return

    # Make the window's context current
    glfw.make_context_current(window)

    # Cube vertices
    vertices = np.array(
        [
            [1, -1, -1],
            [1, 1, -1],
            [-1, 1, -1],
            [-1, -1, -1],
            [1, -1, 1],
            [1, 1, 1],
            [-1, -1, 1],
            [-1, 1, 1],
        ],
        dtype=np.float32,
    )

    # Cube edges
    edges = np.array(
        [
            [0, 1],
            [1, 2],
            [2, 3],
            [3, 0],
            [4, 5],
            [5, 7],
            [7, 6],
            [6, 4],
            [0, 4],
            [1, 5],
            [2, 7],
            [3, 6],
        ],
        dtype=np.uint32,
    )

    glEnableClientState(GL_VERTEX_ARRAY)
    glVertexPointer(3, GL_FLOAT, 0, vertices)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(-2, 2, -2, 2, -2, 2)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    # Loop until the user closes the window
    while not glfw.window_should_close(window):
        # Render here, e.g. using pyopengl
        glClear(GL_COLOR_BUFFER_BIT)

        glDrawElements(GL_LINES, len(edges) * 2, GL_UNSIGNED_INT, edges)

        # Swap front and back buffers
        glfw.swap_buffers(window)

        # Poll for and process events
        glfw.poll_events()

    glfw.terminate()


if __name__ == "__main__":
    main()
