import sys
import pygame

from screens.splash_screen   import SplashScreen
from screens.loading_screen  import LoadingScreen
from screens.intro_menu       import IntroMenu

def main():
    pygame.init()
    pygame.font.init()
    screen = pygame.display.set_mode((1280, 720))
    pygame.display.set_caption("BattleCubes")

    # 1. Splash — list your image files here
    splash = SplashScreen(
        screen,
        image_paths=[
            "assets/images/logo1.png",
            "assets/images/logo2.png",
        ],
        fade_duration=1000,
        display_duration=5000
    )
    splash.run()

    # 2. Loading
    loader = LoadingScreen(screen)
    loader.run()

    # 3. Intro Menu
    menu = IntroMenu(screen)
    menu.run()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
