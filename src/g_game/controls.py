from typing import Any

import glfw
import numpy as np

from g_game.window import GWin
from g_utils import GLogger, look_at

glog = GLogger(name="camera")


class Camera:
    position: np.ndarray
    world_up: np.ndarray
    front: np.ndarray
    speed: float
    camera_keys: dict[int, bool]
    last_x: float
    last_y: float
    first_mouse: bool

    def __init__(
        self, gwin: GWin, position: np.ndarray, up: np.ndarray, speed: float
    ) -> None:
        self.position = position
        self.world_up = up
        self.front = np.array([0.0, 0.0, 1.0])
        self.speed = speed
        self.camera_keys = {}
        self.last_x = 400
        self.last_y = 300
        self.first_mouse = True

        def mouse_callback(_window: Any, xpos: float, ypos: float) -> None:
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

            self.process_mouse_movement(xoffset, yoffset)

        def key_callback(
            _window: Any, key: Any, _scancode: Any, action: int, _mods: Any
        ) -> None:
            if action == glfw.PRESS:
                self.camera_keys[key] = True
            elif action == glfw.RELEASE:
                self.camera_keys[key] = False

        glfw.set_key_callback(gwin.window, key_callback)
        glfw.set_cursor_pos_callback(gwin.window, mouse_callback)
        glfw.set_input_mode(gwin.window, glfw.CURSOR, glfw.CURSOR_DISABLED)

    def get_view_matrix(self) -> np.ndarray:
        return look_at(self.position, self.position + self.front, self.world_up)

    def process_input(self, delta_time: float) -> None:
        for key, isPressed in self.camera_keys.items():
            if isPressed:
                self.process_keyboard(key, delta_time)

    def process_keyboard(self, key: int, delta_time: float) -> None:
        """
        key is int key code from glfw
        """
        velocity = self.speed * delta_time
        match key:
            case glfw.KEY_W:
                self.position += self.front * velocity
            case glfw.KEY_A:
                self.position -= np.cross(self.front, self.world_up) * velocity
            case glfw.KEY_S:
                self.position -= self.front * velocity
            case glfw.KEY_D:
                self.position += np.cross(self.front, self.world_up) * velocity
            case _:
                glog.i("Unrecognized keycode in process_keyboard:", key)
                pass

    def process_mouse_movement(self, xoffset: float, yoffset: float) -> None:
        sensitivity = 0.1
        xoffset *= sensitivity
        yoffset *= sensitivity

        yaw = np.arctan2(self.front[2], self.front[0]) * (180.0 / np.pi)
        pitch = np.arcsin(self.front[1]) * (180.0 / np.pi)

        yaw += xoffset
        pitch += yoffset

        if pitch > 89.0:
            pitch = 89.0
        if pitch < -89.0:
            pitch = -89.0

        front = np.array(
            [
                np.cos(np.radians(yaw)) * np.cos(np.radians(pitch)),
                np.sin(np.radians(pitch)),
                np.sin(np.radians(yaw)) * np.cos(np.radians(pitch)),
            ]
        )
        self.front = front / np.linalg.norm(front)
