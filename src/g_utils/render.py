import math

import numpy as np
from OpenGL.GL import (
    GL_CLAMP_TO_EDGE,
    GL_COMPILE_STATUS,
    GL_FRAGMENT_SHADER,
    GL_LINEAR,
    GL_LINK_STATUS,
    GL_RGB,
    GL_TEXTURE_2D,
    GL_TEXTURE_MAG_FILTER,
    GL_TEXTURE_MIN_FILTER,
    GL_TEXTURE_WRAP_S,
    GL_TEXTURE_WRAP_T,
    GL_UNSIGNED_BYTE,
    GL_VERTEX_SHADER,
    glAttachShader,
    glBindTexture,
    glCompileShader,
    glCreateProgram,
    glCreateShader,
    glDeleteShader,
    glGenTextures,
    glGetProgramInfoLog,
    glGetProgramiv,
    glGetShaderInfoLog,
    glGetShaderiv,
    glLinkProgram,
    glShaderSource,
    glTexImage2D,
    glTexParameteri,
)
from PIL import Image


def normalize(v: np.ndarray) -> np.ndarray:
    """Normalizes a vector."""
    norm = np.linalg.norm(v)
    if norm == 0:
        return v
    return v / norm


def look_at(eye: np.ndarray, target: np.ndarray, up: np.ndarray) -> np.ndarray:
    """Creates a world to view matrix for a camera."""
    zaxis = normalize(target - eye)
    xaxis = normalize(np.cross(zaxis, up))
    yaxis = np.cross(xaxis, zaxis)

    # Create a 4x4 view matrix
    view_matrix = np.array(
        [
            [xaxis[0], yaxis[0], -zaxis[0], 0],
            [xaxis[1], yaxis[1], -zaxis[1], 0],
            [xaxis[2], yaxis[2], -zaxis[2], 0],
            [-np.dot(xaxis, eye), -np.dot(yaxis, eye), np.dot(zaxis, eye), 1],
        ],
        dtype=np.float32,
    )

    return view_matrix


def create_perspective_matrix(
    fov_degrees: float, aspect_ratio: float, near: float, far: float
) -> np.ndarray:
    """
    Creates a perspective projection matrix using NumPy.

    fov_degrees: Field of View in degrees.
    aspect_ratio: The aspect ratio of the viewport (width / height).
    near: The near clipping plane distance.
    far: The far clipping plane distance.

    Returns a 4x4 NumPy array representing the perspective matrix.
    """
    # 1. Convert field of view from degrees to radians
    fov_rad = math.radians(fov_degrees)

    # 2. Calculate the tangent of half the FOV
    tan_half_fov = math.tan(fov_rad / 2.0)

    # 3. Initialize a 4x4 identity matrix
    matrix = np.zeros((4, 4), dtype=np.float32)

    # 4. Set the matrix elements according to the perspective projection formula

    # Scaling factors for x and y coordinates
    matrix[0, 0] = 1.0 / (aspect_ratio * tan_half_fov)
    matrix[1, 1] = 1.0 / (tan_half_fov)

    # Remapping z-coordinate to the [-1, 1] range
    matrix[2, 2] = -(far + near) / (far - near)
    matrix[2, 3] = -1.0  # Used for perspective division
    matrix[3, 2] = -(2.0 * far * near) / (far - near)

    return matrix


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
        raise TypeError(
            "The shader program compilation didn't return an integer assignment!"
        )

    return shader_program


def load_texture(path: str) -> int:
    """Loads a texture from a file and returns the texture ID."""
    texture_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture_id)

    # Set texture wrapping and filtering options
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

    try:
        with Image.open(path) as img:
            # Flip image to match what opengl expects (0,0 is bottom left, not top left)
            img = img.transpose(Image.Transpose.FLIP_TOP_BOTTOM)

            img_data = img.convert("RGB").tobytes()
            width, height = img.size
            glTexImage2D(
                GL_TEXTURE_2D,
                0,
                GL_RGB,
                width,
                height,
                0,
                GL_RGB,
                GL_UNSIGNED_BYTE,
                img_data,
            )
    except FileNotFoundError:
        raise FileNotFoundError(f"Texture file not found at: {path}")

    return texture_id
