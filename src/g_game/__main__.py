from g_game.draw import GDraw
from g_game.window import GWin
from g_utils import glog


def main():
    glog.i("Main entrypoint!")

    gwin = GWin().set_as_context()
    gdraw = GDraw(gwindow=gwin)

    gdraw.triangle()


if __name__ == "__main__":
    main()
