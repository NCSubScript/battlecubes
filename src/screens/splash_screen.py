import sys
import pygame

class SplashScreen:
    def __init__(self, screen, image_paths, fade_duration=1000, display_duration=5000, debug=False):
        self.screen = screen
        self.images = image_paths
        self.fd = fade_duration
        self.dd = display_duration
        self.clock = pygame.time.Clock()
        self.debug = debug

    def run(self):
        if self.debug:
            print("Debug mode: Skipping splash screens")
            return

        w, h = self.screen.get_size()
        for path in self.images:
            img = pygame.image.load(path).convert_alpha()
            img = pygame.transform.smoothscale(img, (w, h))

            # Fade In
            start = pygame.time.get_ticks()
            while True:
                t = pygame.time.get_ticks() - start
                if t >= self.fd:
                    break
                alpha = int((t / self.fd) * 255)
                img.set_alpha(alpha)
                self._blit(img)
                self._handle_quit()
                self.clock.tick(60)

            # Full display
            start = pygame.time.get_ticks()
            while pygame.time.get_ticks() - start < self.dd:
                img.set_alpha(255)
                self._blit(img)
                self._handle_quit()
                self.clock.tick(60)

            # Fade Out
            start = pygame.time.get_ticks()
            while True:
                t = pygame.time.get_ticks() - start
                if t >= self.fd:
                    break
                alpha = max(0, 255 - int((t / self.fd) * 255))
                img.set_alpha(alpha)
                self._blit(img)
                self._handle_quit()
                self.clock.tick(60)

    def _blit(self, surf):
        self.screen.fill((0, 0, 0))
        self.screen.blit(surf, (0, 0))
        pygame.display.flip()

    def _handle_quit(self):
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
