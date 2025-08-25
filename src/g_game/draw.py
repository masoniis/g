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
    GL_TEXTURE0,
    GL_TEXTURE_2D,
    GL_TRIANGLES,
    GL_UNSIGNED_INT,
    glActiveTexture,
    glBindBuffer,
    glBindTexture,
    glBindVertexArray,
    glBufferData,
    glClear,
    glDrawElements,
    glEnableVertexAttribArray,
    glGenBuffers,
    glGenVertexArrays,
    glUniform1i,
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


type BufferID = int


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

        # -------------------
        #   Buffer creation
        # -------------------

        VAO: int = glGenVertexArrays(
            1  # n buffers
        )
        VBO: BufferID = glGenBuffers(
            1  # n buffers
        )
        EBO: BufferID = glGenBuffers(
            1  # n buffers
        )

        # Set the context VAO for subsequent actions
        glBindVertexArray(VAO)

        # Copy mesh vertices into the VBO
        glBindBuffer(GL_ARRAY_BUFFER, VBO)
        glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)

        # Copy indices (drawing order) into the EBO
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices.nbytes, indices, GL_STATIC_DRAW)

        # INFO: Create and enable the attribute pointers
        # These describe how our VBO vertex data is formatted
        # and what gets passed to the vertex shaders' inputs
        glVertexAttribPointer(
            index=0,  # target vertex shader input 'aPos'
            size=3,  # aPos expects (x, y, z) from vertices
            normalized=GL_FALSE,
            stride=5 * vertices.itemsize,  # 5 floats per vertex
            pointer=ctypes.c_void_p(0),
            type=GL_FLOAT,
        )
        glVertexAttribPointer(
            index=1,  # target vertex shader input 'aTexCoord'
            size=2,  # aTexCoord expects (u, v) from vertices
            normalized=GL_FALSE,
            stride=5 * vertices.itemsize,  # 5 floats per vertex
            pointer=ctypes.c_void_p(3 * vertices.itemsize),  # offset by 3 floats
            type=GL_FLOAT,
        )
        glEnableVertexAttribArray(0)
        glEnableVertexAttribArray(1)

        # Unbind all buffers
        glBindBuffer(GL_ARRAY_BUFFER, 0)
        glBindVertexArray(0)

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
        texture_loc: int,
        texture: int,
        projection: np.ndarray,
        model_view: np.ndarray,
    ) -> None:
        """Draws a given mesh object."""
        glUseProgram(mesh.shader_program)

        # Bind the texture and set the uniform
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, texture)
        glUniform1i(texture_loc, 0)

        glUniformMatrix4fv(projection_loc, 1, GL_FALSE, projection)
        glUniformMatrix4fv(model_view_loc, 1, GL_FALSE, model_view)

        glBindVertexArray(mesh.vao)
        glDrawElements(
            GL_TRIANGLES, mesh.vertex_count, GL_UNSIGNED_INT, ctypes.c_void_p(0)
        )
        glBindVertexArray(0)  # Unbind after drawing
