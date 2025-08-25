import ctypes
from dataclasses import dataclass

import numpy as np
from OpenGL.GL import (
    GL_ARRAY_BUFFER,
    GL_COLOR_BUFFER_BIT,
    GL_ELEMENT_ARRAY_BUFFER,
    GL_FALSE,
    GL_FLOAT,
    GL_STATIC_DRAW,
    GL_TRIANGLES,
    GL_UNSIGNED_INT,
    glBindBuffer,
    glBindVertexArray,
    glBufferData,
    glClear,
    glDrawArrays,
    glDrawElements,
    glEnableVertexAttribArray,
    glGenBuffers,
    glGenVertexArrays,
    glUniformMatrix4fv,
    glUseProgram,
    glVertexAttribPointer,
)

from g_utils import GLogger

glog = GLogger(name="gdraw")


@dataclass
class Mesh:
    vao: int
    vbo: int
    ebo: int
    vertex_count: int
    shader_program: int


class GDraw:
    def __init__(self) -> None:
        glog.i("Initializing GDraw...")

    def clear(self) -> None:
        """Clears the color buffer."""
        glClear(GL_COLOR_BUFFER_BIT)

    def create_mesh(
        self,
        vertices: np.ndarray,
        indices: np.ndarray,
        shader_program: int,
    ) -> Mesh:
        """Creates the buffers and vertex layout for a given set of vertices."""

        VAO: int = glGenVertexArrays(1)
        VBO: int = glGenBuffers(1)
        EBO: int = glGenBuffers(1)

        glBindVertexArray(VAO)
        glBindBuffer(GL_ARRAY_BUFFER, VBO)
        glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)

        # Configure the EBO (Element Buffer Object)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices.nbytes, indices, GL_STATIC_DRAW)

        glVertexAttribPointer(
            0,  # loc 0 in the shader
            3,  # 3 components per vertex
            GL_FLOAT,
            GL_FALSE,  # no normalizing
            3 * vertices.itemsize,
            ctypes.c_void_p(0),
        )
        glEnableVertexAttribArray(0)

        glBindBuffer(GL_ARRAY_BUFFER, 0)
        glBindVertexArray(0)

        # Return a Mesh object containing all the necessary handles
        return Mesh(
            vao=VAO,
            vbo=VBO,
            ebo=EBO,
            vertex_count=len(indices),
            shader_program=shader_program,
        )

    def draw(
        self,
        mesh: Mesh,
        projection_loc: int,
        model_view_loc: int,
        projection: np.ndarray,
        model_view: np.ndarray,
    ) -> None:
        """Draws a given mesh object."""
        glUseProgram(mesh.shader_program)

        glUniformMatrix4fv(projection_loc, 1, GL_FALSE, projection)
        glUniformMatrix4fv(model_view_loc, 1, GL_FALSE, model_view)

        glBindVertexArray(mesh.vao)
        if False:
            glDrawArrays(GL_TRIANGLES, 0, mesh.vertex_count)
        glDrawElements(GL_TRIANGLES, mesh.vertex_count, GL_UNSIGNED_INT, ctypes.c_void_p(0))
        glBindVertexArray(0)  # Unbind after drawing
