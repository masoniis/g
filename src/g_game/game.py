from __future__ import annotations

import sys
from typing import Any

import glfw
import numpy as np
from OpenGL.GL import (
    glClearColor,
    glGetUniformLocation,
)

from g_game.controls import Camera
from g_game.draw import GDraw, Mesh
from g_game.window import GWin
from g_utils import GLogger, compile_shader_program, create_perspective_matrix

glog = GLogger(name="game")


class Game:
    gwin: GWin
    gdraw: GDraw
    triangle: Mesh | None
    camera: Camera
    camera_keys: dict[int, bool]
    last_frame_time: float
    last_x: float
    last_y: float
    first_mouse: bool

    def __init__(self) -> None:
        glog.i("Initializing Game...")
        self.gwin = GWin()
        self.gdraw = GDraw()
        self.triangle = None  # Will be set in run()
        self.camera = Camera(
            position=np.array([0.0, 0.0, -3.0]),
            up=np.array([0.0, 1.0, 0.0]),
            speed=2.5,
        )
        self.camera_keys = {}
        self.last_frame_time = 0.0
        self.last_x = 400
        self.last_y = 300
        self.first_mouse = True

    def key_callback(
        self, _window: Any, key: Any, _scancode: Any, action: int, _mods: Any
    ) -> None:
        if action == glfw.PRESS:
            self.camera_keys[key] = True
        elif action == glfw.RELEASE:
            self.camera_keys[key] = False

    def mouse_callback(self, _window: Any, xpos: float, ypos: float) -> None:
        if self.first_mouse:
            self.last_x = xpos
            self.last_y = ypos
            self.first_mouse = False

        xoffset = xpos - self.last_x
        yoffset = (
            self.last_y - ypos
        )  # Reversed since y-coordinates go from bottom to top

        self.last_x = xpos
        self.last_y = ypos

        self.camera.process_mouse_movement(xoffset, yoffset)

    def process_input(self, delta_time: float) -> None:
        for key, isPressed in self.camera_keys.items():
            if isPressed:
                self.camera.process_keyboard(key, delta_time)

    def run(self) -> None:
        self.gwin.set_as_context()
        glfw.set_key_callback(self.gwin.window, self.key_callback)
        glfw.set_cursor_pos_callback(self.gwin.window, self.mouse_callback)
        glfw.set_input_mode(self.gwin.window, glfw.CURSOR, glfw.CURSOR_DISABLED)

        glClearColor(0.1, 0.1, 0.3, 1.0)

        # 1. Compile shaders
        shader = compile_shader_program(
            "src/shaders/simple.vert", "src/shaders/simple.frag"
        )

        # 2. Ask GDraw to create the triangle mesh for us
        self.triangle = self.gdraw.create_pyramid_mesh(shader)

        # 3. Get uniform locations
        projection_loc = glGetUniformLocation(shader, "projection")
        model_view_loc = glGetUniformLocation(shader, "modelView")

        # 4. Create matrices
        # projection = np.identity(4, dtype=np.float32)
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

                self.process_input(delta_time)

                self.gdraw.clear()

                view = self.camera.get_view_matrix()
                model_view = view @ model

                self.gdraw.draw(
                    self.triangle,
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
