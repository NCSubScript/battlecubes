import sys
import pygame

class LoadingScreen:
    def __init__(self, screen, debug=False):
        self.screen = screen
        self.w, self.h = screen.get_size()
        self.font = pygame.font.SysFont(None, 36)
        self.clock = pygame.time.Clock()
        self.debug = debug

    def run(self):
        if self.debug:
            # Draw one quick pass and return
            self._draw_frame(100)
            pygame.time.delay(200)  # tiny pause for visibility
            print("Debug mode: Skipping loading delays")
            return

        progress = 0
        while progress <= 100:
            for ev in pygame.event.get():
                if ev.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            progress += 1
            self._draw_frame(progress)
            self.clock.tick(60)

    def _draw_frame(self, progress):
        self.screen.fill((0, 0, 0))
        text = self.font.render(f"Loading... {progress}%", True, (255, 255, 255))
        tx = (self.w - text.get_width()) // 2
        ty = self.h // 2 - 50
        self.screen.blit(text, (tx, ty))

        bar_w, bar_h = self.w * 0.6, 20
        bx = (self.w - bar_w) // 2
        by = self.h // 2
        pygame.draw.rect(self.screen, (100, 100, 100), (bx, by, bar_w, bar_h), 2)
        inner = (progress / 100) * (bar_w - 4)
        pygame.draw.rect(self.screen, (0, 200, 0), (bx + 2, by + 2, inner, bar_h - 4))

        pygame.display.flip()
