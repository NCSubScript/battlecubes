# scenes/splash_screen.py

import pygame
from pygame import Surface
from typing import List, Optional, Callable

class SplashScreen:
    """
    Displays a sequence of logos:
    - fade-in over fade_time seconds
    - stay fully visible for display_time seconds
    - fade-out over fade_time seconds
    Press any key or click to skip to the next scene.
    """

    def __init__(
        self,
        screen: Surface,
        logo_paths: List[str],
        display_time: float = 2.0,
        fade_time: float = 1.0,
        on_complete: Optional[Callable] = None
    ):
        self.screen = screen
        self.width, self.height = screen.get_size()
        self.on_complete = on_complete

        # Load each logo or warn
        self.logos: List[Surface] = []
        for path in logo_paths:
            try:
                img = pygame.image.load(path).convert_alpha()
            except pygame.error as e:
                print(f"[SplashScreen] Failed to load '{path}': {e}")
            else:
                self.logos.append(img)

        if not self.logos:
            raise RuntimeError("SplashScreen: No logos could be loaded")

        # Center rects for each logo
        self.rects = [
            logo.get_rect(center=(self.width // 2, self.height // 2))
            for logo in self.logos
        ]

        # Timings in milliseconds
        self.display_ms = int(display_time * 1000)
        self.fade_ms = int(fade_time * 1000)
        self.cycle_ms = self.fade_ms * 2 + self.display_ms

        self.start_time = pygame.time.get_ticks()
        self.finished = False

    def update(self, events):
        now = pygame.time.get_ticks()
        elapsed = now - self.start_time

        # Skip to end on any key or mouse press
        for ev in events:
            if ev.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
                elapsed = len(self.logos) * self.cycle_ms
                break

        if elapsed >= len(self.logos) * self.cycle_ms:
            if not self.finished and self.on_complete:
                self.on_complete()
            self.finished = True

    def draw(self):
        if self.finished:
            return

        elapsed = pygame.time.get_ticks() - self.start_time
        idx = min(elapsed // self.cycle_ms, len(self.logos) - 1)
        logo = self.logos[int(idx)]
        rect = self.rects[int(idx)]

        in_cycle = elapsed - int(idx) * self.cycle_ms

        # Determine alpha
        if in_cycle < self.fade_ms:
            alpha = int((in_cycle / self.fade_ms) * 255)
        elif in_cycle > self.fade_ms + self.display_ms:
            tail = in_cycle - (self.fade_ms + self.display_ms)
            alpha = int(((self.fade_ms - tail) / self.fade_ms) * 255)
        else:
            alpha = 255

        alpha = max(0, min(255, alpha))

        # Render
        self.screen.fill((0, 0, 0))
        logo.set_alpha(alpha)
        self.screen.blit(logo, rect)
