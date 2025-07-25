import sys
import pygame

class LoadingScreen:
    def __init__(self, screen):
        self.screen = screen
        self.w, self.h = screen.get_size()
        self.font = pygame.font.SysFont(None, 36)
        self.clock = pygame.time.Clock()

    def run(self):
        progress = 0

        while progress <= 100:
            for ev in pygame.event.get():
                if ev.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            # simulate load
            progress += 1

            # draw
            self.screen.fill((0, 0, 0))
            text = self.font.render(f"Loading... {progress}%", True, (255, 255, 255))
            tx, ty = (self.w - text.get_width()) // 2, self.h // 2 - 50
            self.screen.blit(text, (tx, ty))

            bar_w, bar_h = self.w * 0.6, 20
            bx, by = (self.w - bar_w) // 2, self.h // 2
            pygame.draw.rect(self.screen, (100, 100, 100), (bx, by, bar_w, bar_h), 2)
            inner = (progress / 100) * (bar_w - 4)
            pygame.draw.rect(self.screen, (0, 200, 0), (bx + 2, by + 2, inner, bar_h - 4))

            pygame.display.flip()
            self.clock.tick(60)
