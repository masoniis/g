from __future__ import annotations

import sys

import glfw
import numpy as np
from OpenGL.GL import (
    GL_COMPILE_STATUS,
    GL_FRAGMENT_SHADER,
    GL_LINK_STATUS,
    GL_VERTEX_SHADER,
    glAttachShader,
    glCompileShader,
    glCreateProgram,
    glCreateShader,
    glDeleteShader,
    glGetProgramInfoLog,
    glGetProgramiv,
    glGetShaderInfoLog,
    glGetShaderiv,
    glGetUniformLocation,
    glLinkProgram,
    glShaderSource,
)

from g_game.draw import GDraw, Mesh
from g_game.window import GWin
from g_utils import glog


def compile_shader_program(vertex_path: str, fragment_path: str) -> int:
    # Read shader source code from files
    with open(vertex_path, "r") as f:
        vertex_source = f.read()
    with open(fragment_path, "r") as f:
        fragment_source = f.read()

    # Compile Vertex Shader
    vertex_shader = glCreateShader(GL_VERTEX_SHADER)
    glShaderSource(vertex_shader, vertex_source)
    glCompileShader(vertex_shader)
    if not glGetShaderiv(vertex_shader, GL_COMPILE_STATUS):
        raise Exception(
            f"ERROR: Vertex shader compilation failed\n{glGetShaderInfoLog(vertex_shader)}"
        )

    # Compile Fragment Shader
    fragment_shader = glCreateShader(GL_FRAGMENT_SHADER)
    glShaderSource(fragment_shader, fragment_source)
    glCompileShader(fragment_shader)
    if not glGetShaderiv(fragment_shader, GL_COMPILE_STATUS):
        raise Exception(
            f"ERROR: Fragment shader compilation failed\n{glGetShaderInfoLog(fragment_shader)}"
        )

    # Link shaders into a program
    shader_program = glCreateProgram()
    glAttachShader(shader_program, vertex_shader)
    glAttachShader(shader_program, fragment_shader)
    glLinkProgram(shader_program)
    if not glGetProgramiv(shader_program, GL_LINK_STATUS):
        raise Exception(
            f"ERROR: Shader program linking failed\n{glGetProgramInfoLog(shader_program)}"
        )

    # Delete shaders as they are now linked into the program and no longer necessary
    glDeleteShader(vertex_shader)
    glDeleteShader(fragment_shader)

    if not isinstance(shader_program, int):  # pyright: ignore[reportUnnecessaryIsInstance]
        raise TypeError("Shader program is not an integer!")

    return shader_program


class Game:
    gwin: GWin
    gdraw: GDraw
    triangle: Mesh | None

    def __init__(self) -> None:
        glog.i("Initializing Game...")
        self.gwin = GWin()
        self.gdraw = GDraw()
        self.triangle = None  # Will be set in run()

    def run(self) -> None:
        self.gwin.set_as_context()

        # 1. Compile shaders
        shader = compile_shader_program(
            "src/shaders/simple.vert", "src/shaders/simple.frag"
        )

        # 2. Ask GDraw to create the triangle mesh for us
        self.triangle = self.gdraw.create_triangle_mesh(shader)

        # 3. Get uniform locations
        projection_loc = glGetUniformLocation(shader, "projection")
        model_view_loc = glGetUniformLocation(shader, "modelView")

        # 4. Create matrices
        projection = np.identity(4, dtype=np.float32)
        model_view = np.identity(4, dtype=np.float32)

        # --- Main Render Loop ---
        try:
            while not self.gwin.should_close():
                self.gdraw.clear()

                self.gdraw.draw(
                    self.triangle,
                    projection_loc,
                    model_view_loc,
                    projection,
                    model_view,
                )

                glfw.swap_buffers(self.gwin.window)
                glfw.poll_events()
        except KeyboardInterrupt:
            print()
            glog.i("KeyboardInterrupt received, exiting...")
            sys.stdout.flush()
        finally:
            glog.i("Game loop has ended, cya!")
            glfw.terminate()
