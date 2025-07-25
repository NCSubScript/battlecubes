import sys
import pygame

class IntroMenu:
    def __init__(self, screen):
        self.screen = screen
        self.w, self.h = screen.get_size()
        self.font = pygame.font.SysFont(None, 48)
        self.options = ["Single Player", "Multiplayer", "Settings", "Quit"]
        self.selected = 0
        self.clock = pygame.time.Clock()

    def run(self):
        running = True
        while running:
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
                        choice = self.options[self.selected]
                        print(f"Menu choice: {choice}")
                        running = False

            self.screen.fill((10, 10, 50))
            for i, opt in enumerate(self.options):
                color = (255, 255, 0) if i == self.selected else (200, 200, 200)
                txt = self.font.render(opt, True, color)
                x = (self.w - txt.get_width()) // 2
                y = self.h // 2 - len(self.options) * 30 + i * 60
                self.screen.blit(txt, (x, y))

            pygame.display.flip()
            self.clock.tick(60)
