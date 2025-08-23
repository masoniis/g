from __future__ import annotations

from typing import Any

import glfw
from OpenGL.GL import GL_TRUE

from g_utils import GLogger

glog = GLogger(name="gwin")


class GWin:
    window: Any

    size: tuple[int, int] = (768, 576)

    def __init__(self) -> None:
        glog.i("Initializing GWindow...")

        def error_callback(error_code: Any, description: Any) -> None:
            glog.e(f"GLFW Error {error_code}: {description}")

        glfw.set_error_callback(cbfun=error_callback)

        if not glfw.init():
            raise RuntimeError("GLFW Initialization Failed")

        # Give a hint to set the context version to 330 for shaders
        glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
        glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
        glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
        glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, GL_TRUE)

        self.window = glfw.create_window(
            *self.size, title="g", monitor=None, share=None
        )

        if not self.window:
            glfw.terminate()
            raise RuntimeError("GLFW window failed to spawen.")

    @property
    def _as_parameter_(self) -> Any:
        """
        Allows this entire object to be passed directly to ctypes functions,
        which will use the internal window pointer.
        """
        return self.window

    def set_as_context(self) -> GWin:
        """Makes the context current and returns self for method chaining"""
        glfw.make_context_current(window=self)
        return self

    def should_close(self) -> bool:
        """Returns whether the window should close"""
        return glfw.window_should_close(window=self)
