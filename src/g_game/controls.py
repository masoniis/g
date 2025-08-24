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
