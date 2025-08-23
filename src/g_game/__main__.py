from g_game.game import Game
from g_utils import glog


def main():
    glog.i("Main entrypoint!")
    Game().run()


if __name__ == "__main__":
    main()
