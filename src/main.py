import sys
import argparse
import pygame

from screens.splash_screen   import SplashScreen
from screens.loading_screen  import LoadingScreen
from screens.intro_menu       import IntroMenu

def parse_args():
    parser = argparse.ArgumentParser(description="BattleCubes Launcher")
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Skip splash screens and loading delays"
    )
    return parser.parse_args()

def main():
    args = parse_args()
    debug = args.debug

    pygame.init()
    pygame.font.init()
    screen = pygame.display.set_mode((1280, 720))
    pygame.display.set_caption("BattleCubes")

    # 1. Splash — skip if debug
    splash = SplashScreen(
        screen,
        image_paths=[
            "assets/images/logo1.png",
            "assets/images/logo2.png",
        ],
        fade_duration=1000,
        display_duration=5000,
        debug=debug
    )
    splash.run()

    # 2. Loading — pass debug to skip delays
    loader = LoadingScreen(screen, debug=debug)
    loader.run()

    # 3. Intro Menu
    menu = IntroMenu(screen)
    menu.run()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()