import glfw
import numpy as np

from g_utils import GLogger, look_at

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
