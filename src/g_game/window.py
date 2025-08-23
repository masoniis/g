from __future__ import annotations

from typing import Any

import glfw

from g_utils import glog


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

        self.window = glfw.create_window(
            *self.size, title="Hello World", monitor=None, share=None
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
        glfw.make_context_current(window=self.window)
        return self

    def should_close(self) -> bool:
        return glfw.window_should_close(window=self.window)
