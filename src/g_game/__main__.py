from g_game.game import Game
from g_utils import GLogger

glog = GLogger(name="main")


def main():
    glog.i("Main entrypoint!")
    Game().run()


if __name__ == "__main__":
    main()
