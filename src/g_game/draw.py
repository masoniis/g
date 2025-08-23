import ctypes
from dataclasses import dataclass

import numpy as np
from OpenGL.GL import (
    GL_ARRAY_BUFFER,
    GL_COLOR_BUFFER_BIT,
    GL_FALSE,
    GL_FLOAT,
    GL_STATIC_DRAW,
    GL_TRIANGLES,
    glBindBuffer,
    glBindVertexArray,
    glBufferData,
    glClear,
    glClearColor,
    glDrawArrays,
    glEnableVertexAttribArray,
    glGenBuffers,
    glGenVertexArrays,
    glUseProgram,
    glVertexAttribPointer,
    glUniformMatrix4fv,
)

from g_utils import glog


@dataclass
class Mesh:
    vao: int
    vbo: int
    vertex_count: int
    shader_program: int


class GDraw:
    def __init__(self) -> None:
        glog.i("Initializing GDraw...")
        glClearColor(0.1, 0.1, 0.9, 1.0)

    def clear(self) -> None:
        """Clears the color buffer."""
        glClear(GL_COLOR_BUFFER_BIT)

    def create_triangle_mesh(self, shader_program: int) -> Mesh:
        """Creates the buffers and vertex layout for a simple triangle."""
        vertices = np.array(
            [
                # top vert
                0.0,  # x
                0.5,  # y
                0.0,  # z
                # bottom left
                -0.5,
                -0.5,
                0.0,
                # bottom right
                0.5,
                -0.5,
                0.0,
            ],
            dtype=np.float32,
        )

        VAO = glGenVertexArrays(1)
        VBO = glGenBuffers(1)

        glBindVertexArray(VAO)
        glBindBuffer(GL_ARRAY_BUFFER, VBO)
        glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)

        glVertexAttribPointer(
            0, 3, GL_FLOAT, GL_FALSE, 3 * vertices.itemsize, ctypes.c_void_p(0)
        )
        glEnableVertexAttribArray(0)

        glBindBuffer(GL_ARRAY_BUFFER, 0)
        glBindVertexArray(0)

        # Return a Mesh object containing all the necessary handles
        return Mesh(vao=VAO, vbo=VBO, vertex_count=3, shader_program=shader_program)

    def draw(self, mesh: Mesh, projection_loc: int, model_view_loc: int, projection: np.ndarray, model_view: np.ndarray) -> None:
        """Draws a given mesh object."""
        glUseProgram(mesh.shader_program)

        glUniformMatrix4fv(projection_loc, 1, GL_FALSE, projection)
        glUniformMatrix4fv(model_view_loc, 1, GL_FALSE, model_view)

        glBindVertexArray(mesh.vao)
        glDrawArrays(GL_TRIANGLES, 0, mesh.vertex_count)
        glBindVertexArray(0)  # Unbind after drawing
