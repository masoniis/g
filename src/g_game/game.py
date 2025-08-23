from __future__ import annotations

import sys

import glfw
import numpy as np
from OpenGL.GL import (
    glClearColor,
    glGetUniformLocation,
)

from g_game.draw import GDraw, Mesh
from g_game.window import GWin
from g_utils import GLogger, compile_shader_program, create_perspective_matrix, look_at

glog = GLogger(name="game")


class Camera:
    position: np.ndarray
    world_up: np.ndarray
    front: np.ndarray
    speed: float

    def __init__(self, position: np.ndarray, up: np.ndarray, speed: float) -> None:
        self.position = position
        self.world_up = up
        self.front = np.array([0.0, 0.0, 1.0])
        self.speed = speed

    def get_view_matrix(self) -> np.ndarray:
        return look_at(self.position, self.position + self.front, self.world_up)

    def process_keyboard(self, direction: str, delta_time: float) -> None:
        velocity = self.speed * delta_time
        if direction == "FORWARD":
            self.position += self.front * velocity
        if direction == "BACKWARD":
            self.position -= self.front * velocity
        if direction == "LEFT":
            self.position -= np.cross(self.front, self.world_up) * velocity
        if direction == "RIGHT":
            self.position += np.cross(self.front, self.world_up) * velocity


class Game:
    gwin: GWin
    gdraw: GDraw
    triangle: Mesh | None
    camera: Camera
    camera_keys: dict[int, bool]
    last_frame_time: float

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

    def key_callback(self, window, key, scancode, action, mods) -> None:
        if action == glfw.PRESS:
            self.camera_keys[key] = True
        elif action == glfw.RELEASE:
            self.camera_keys[key] = False

    def process_input(self, delta_time: float) -> None:
        if self.camera_keys.get(glfw.KEY_W):
            self.camera.process_keyboard("FORWARD", delta_time)
        if self.camera_keys.get(glfw.KEY_A):
            self.camera.process_keyboard("LEFT", delta_time)
        if self.camera_keys.get(glfw.KEY_S):
            self.camera.process_keyboard("BACKWARD", delta_time)
        if self.camera_keys.get(glfw.KEY_D):
            self.camera.process_keyboard("RIGHT", delta_time)

    def run(self) -> None:
        self.gwin.set_as_context()
        glfw.set_key_callback(self.gwin.window, self.key_callback)

        glClearColor(0.1, 0.1, 0.3, 1.0)

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
