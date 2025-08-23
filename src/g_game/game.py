from __future__ import annotations

import glfw

from g_game.draw import GDraw
from g_game.window import GWin
from g_utils import glog


class Game:
    gwin: GWin
    gdraw: GDraw

    def __init__(self) -> None:
        glog.i("Initializing Game...")
        self.gwin = GWin()
        self.gdraw = GDraw(self.gwin)

    def run(self) -> None:
        self.gwin.set_as_context()

        while not self.gwin.should_close():
            self.gdraw.clear()
            self.gdraw.triangle()

            # Swap front and back buffers
            glfw.swap_buffers(self.gwin)

            # Poll for and process events
            glfw.poll_events()

        glfw.terminate()
