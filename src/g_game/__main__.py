from typing import Any

import glfw
import numpy as np
from OpenGL.GL import (
    GL_COLOR_BUFFER_BIT,
    GL_FLOAT,
    GL_MODELVIEW,
    GL_PROJECTION,
    GL_TRIANGLES,
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

from g_utils import glog


def main():
    glog.i("Main entrypoint!")

    def error_callback(error_code: Any, description: Any):
        glog.e(f"GLFW Error {error_code}: {description}")

    glfw.set_error_callback(error_callback)

    if not glfw.init():
        glog.e("GLFW failed to initialize!")
        return

    # Create a windowed mode window and its OpenGL context
    window = glfw.create_window(640, 480, "Hello World", None, None)
    if not window:
        glfw.terminate()
        return

    # Make the window's context current
    glfw.make_context_current(window)

    # Triangle vertices
    vertices = np.array(
        [
            [0.0, 0.5, 0.0],  # Top vertex
            [-0.5, -0.5, 0.0],  # Bottom left
            [0.5, -0.5, 0.0],  # Bottom right
        ],
        dtype=np.float32,
    )

    # Triangle indices (just one triangle)
    indices = np.array([0, 1, 2], dtype=np.uint32)

    glEnableClientState(GL_VERTEX_ARRAY)
    glVertexPointer(3, GL_FLOAT, 0, vertices)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(-1, 1, -1, 1, -1, 1)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    # Loop until the user closes the window
    while not glfw.window_should_close(window):
        # Render here, e.g. using pyopengl
        glClear(GL_COLOR_BUFFER_BIT)

        glDrawElements(GL_TRIANGLES, len(indices), GL_UNSIGNED_INT, indices)

        # Swap front and back buffers
        glfw.swap_buffers(window)

        # Poll for and process events
        glfw.poll_events()

    glfw.terminate()


if __name__ == "__main__":
    main()
