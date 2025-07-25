import pygame
from pygame import Surface, Rect, Color
from typing import List, Callable, Optional

class IntroMenu:
    """
    Displays a static background, menu options, and a 3D object placeholder.
    Callbacks are invoked when an option is selected.
    """
    def __init__(
        self,
        screen: Surface,
        resource_mgr,
        background_key: str,
        font_key: tuple,  # (font_path, size)
        menu_items: List[str],
        callbacks: List[Callable],
        render_3d: Optional[Callable] = None
    ):
        self.screen = screen
        self.width, self.height = screen.get_size()
        self.rm = resource_mgr
        self.bg = self.rm.get_image(background_key)
        self.font = self.rm.load_font(*font_key)
        self.items = menu_items
        self.callbacks = callbacks
        self.selected = 0
        self.render_3d = render_3d

        # Precompute text surfaces
        self.text_surfs = []
        self.text_rects = []
        for i, label in enumerate(self.items):
            surf = self.font.render(label, True, Color('white'))
            rect = surf.get_rect()
            self.text_surfs.append(surf)
            self.text_rects.append(rect)

        # Layout: center vertically, evenly spaced
        total_h = sum(rect.h for rect in self.text_rects) + (len(self.items)-1)*20
        start_y = (self.height - total_h) // 2
        for i, rect in enumerate(self.text_rects):
            rect.centerx = self.width // 2
            rect.y = start_y + i * (rect.h + 20)

    def update(self, events: List[pygame.event.EventType]):
        for evt in events:
            if evt.type == pygame.KEYDOWN:
                if evt.key in (pygame.K_UP, pygame.K_w):
                    self.selected = (self.selected - 1) % len(self.items)
                elif evt.key in (pygame.K_DOWN, pygame.K_s):
                    self.selected = (self.selected + 1) % len(self.items)
                elif evt.key in (pygame.K_RETURN, pygame.K_SPACE):
                    # Invoke corresponding callback
                    self.callbacks[self.selected]()

    def draw(self):
        # Draw background
        self.screen.blit(self.bg, (0, 0))

        # Draw 3D object (if provided)
        if self.render_3d:
            self.render_3d()

        # Draw menu items
        for idx, surf in enumerate(self.text_surfs):
            rect = self.text_rects[idx]
            if idx == self.selected:
                # Highlight selected item
                pygame.draw.rect(
                    self.screen,
                    Color('dodgerblue'),
                    rect.inflate(20, 10),
                    border_radius=5
                )
            self.screen.blit(surf, rect)
