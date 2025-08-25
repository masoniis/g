from __future__ import annotations

import sys

import glfw
import numpy as np
from OpenGL.GL import (
    glClearColor,
    glGetUniformLocation,
)

from g_game.controls import Camera
from g_game.draw import GDraw
from g_game.terrain.chunk import Chunk
from g_game.terrain.world import World
from g_game.window import GWin
from g_utils import GLogger, compile_shader_program, create_perspective_matrix

glog = GLogger(name="game")


class Game:
    # Main game objects
    gwin: GWin
    gdraw: GDraw
    camera: Camera

    # Other variables
    last_frame_time: float

    def __init__(self) -> None:
        glog.i("Initializing Game...")
        self.gwin = GWin()
        self.gdraw = GDraw()
        self.camera = Camera(
            gwin=self.gwin,
            position=np.array([0.0, 0.0, -3.0]),
            up=np.array([0.0, 1.0, 0.0]),
            speed=2.5,
        )
        self.last_frame_time = 0.0

    def run(self) -> None:
        self.gwin.set_as_context()

        glClearColor(0.1, 0.1, 0.3, 1.0)

        # 1. Compile shaders
        shader = compile_shader_program(
            "src/shaders/simple.vert", "src/shaders/simple.frag"
        )

        # 2. Create the world and a single chunk
        world = World()
        chunk = Chunk()
        # You can populate the chunk with blocks here later
        # For now, it's empty, but our mesher returns a test cube regardless
        world.add_chunk((0, 0, 0), chunk)

        # 3. Generate a mesh for the chunk and create the renderable mesh object
        chunk_vertices, chunk_indices = chunk.generate_mesh()
        chunk_mesh = self.gdraw.create_mesh(chunk_vertices, chunk_indices, shader)

        # 4. Get uniform locations
        projection_loc = glGetUniformLocation(shader, "projection")
        model_view_loc = glGetUniformLocation(shader, "modelView")

        # 5. Create matrices
        fov = 45.0
        aspect = 800 / 600
        near_plane = 0.1
        far_plane = 100.0
        projection = create_perspective_matrix(
            fov,
            aspect,
            near_plane,
            far_plane,
        )
        model = np.identity(4, dtype=np.float32)

        # --- Main Render Loop ---
        try:
            while not self.gwin.should_close():
                current_frame_time = glfw.get_time()
                delta_time = current_frame_time - self.last_frame_time
                self.last_frame_time = current_frame_time

                self.camera.process_input(delta_time)

                self.gdraw.clear()

                view = self.camera.get_view_matrix()
                model_view = view @ model

                self.gdraw.draw(
                    chunk_mesh,
                    projection_loc,
                    model_view_loc,
                    projection,
                    model_view,
                )

                glfw.swap_buffers(self.gwin.window)
                glfw.poll_events()
            glog.i("Window was closed.")
        except KeyboardInterrupt:
            print()
            glog.i("[b red]KeyboardInterrupt[/] received, exiting...")
            sys.stdout.flush()
        finally:
            glfw.terminate()
            glog.i("[green]Successful cleanup![/]")
