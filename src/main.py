import pygame
from screens.splash_screen import SplashScreen
from screens.intro_menu import IntroMenu

def main():
    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    splash = SplashScreen(screen)
    splash.run()

    menu = IntroMenu(screen)
    menu.run()

if __name__ == "__main__":
    main()
