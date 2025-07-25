import sys
import pygame
from pygame.locals import *
from .gl_renderer import GLRenderer
from OpenGL.GL import *

class IntroMenu:
    def __init__(self, screen, bg_path="assets/images/menu_bg.png"):
        self.screen = screen
        self.w, self.h = screen.get_size()

        # 2D background
        self.bg = pygame.image.load(bg_path).convert()
        self.bg = pygame.transform.smoothscale(self.bg, (self.w, self.h))

        # Text setup
        self.font = pygame.font.SysFont(None, 48)
        self.options = ["Start Game", "Options", "Quit"]
        self.selected = 0

        # OpenGL renderer
        self.renderer = GLRenderer()

    def run(self):
        clock = pygame.time.Clock()

        while True:
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            for ev in pygame.event.get():
                if ev.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif ev.type == pygame.KEYDOWN:
                    if ev.key == pygame.K_UP:
                        self.selected = (self.selected - 1) % len(self.options)
                    elif ev.key == pygame.K_DOWN:
                        self.selected = (self.selected + 1) % len(self.options)
                    elif ev.key == pygame.K_RETURN:
                        self._activate(self.options[self.selected])

            # 1. Draw 2D background
            # Must clear depth only, so our background remains
            glClear(GL_DEPTH_BUFFER_BIT)
            glDepthMask(GL_FALSE)
            self.screen.blit(self.bg, (0, 0))

            # 2. Draw 3D object (cube)
            self.renderer.render()

            # 3. Overlay menu text
            for idx, text in enumerate(self.options):
                color = (255, 255, 0) if idx == self.selected else (200, 200, 200)
                surf = self.font.render(text, True, color)
                x = (self.w - surf.get_width()) // 2
                y = self.h // 2 + idx * 60
                self.screen.blit(surf, (x, y))

            glDepthMask(GL_TRUE)  # Re-enable depth writing
            glFlush()  # Ensure OpenGL commands are executed
            # Swap buffers
            pygame.display.flip()
            clock.tick(60)

    def _activate(self, option):
        if option == "Quit":
            pygame.quit()
            sys.exit()
        # Hook Start Game, Options here…
