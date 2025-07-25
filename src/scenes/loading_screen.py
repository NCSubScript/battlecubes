# scenes/loading_screen.py

import pygame
from pygame import Surface
from typing import List, Tuple, Optional, Callable, Any

class LoadingScreen:
    """
    Sequentially loads assets via a provided ResourceManager.
    asset_manifest entries are tuples:
      - ("image", key,  path)
      - ("sound", key,  path)
      - ("font",  key,  path, [size])
    Calls on_complete() when done.
    """

    def __init__(
        self,
        screen: Surface,
        resource_mgr: Any,
        asset_manifest: List[Tuple],
        on_complete: Optional[Callable] = None
    ):
        self.screen      = screen
        self.rm          = resource_mgr
        self.manifest    = asset_manifest[:]
        self.on_complete = on_complete

        # Progress counters
        self.total  = len(self.manifest)
        self.loaded = 0

        # Precompute bar geometry
        self.width, self.height = screen.get_size()
        self.bar_w, self.bar_h = int(self.width * 0.6), 30
        self.bar_x = (self.width  - self.bar_w) // 2
        self.bar_y = (self.height - self.bar_h) // 2

    def update(self, events):
        # If there are assets left, load one per frame
        if self.loaded < self.total:
            entry = self.manifest[self.loaded]
            kind  = entry[0].lower()

            try:
                if kind == "image":
                    _, key, path = entry
                    self.rm.load_image(key, path)

                elif kind == "sound":
                    _, key, path = entry
                    self.rm.load_sound(key, path)

                elif kind == "font":
                    # entry = ("font", key, path, size?) 
                    if len(entry) == 4:
                        _, key, path, size = entry
                        self.rm.load_font(key, path, size)
                    else:
                        _, key, path     = entry
                        self.rm.load_font(key, path)

                else:
                    print(f"[LoadingScreen] Unknown asset kind '{kind}'")
            except Exception as e:
                print(f"[LoadingScreen] Failed to load {entry}: {e!r}")
            finally:
                self.loaded += 1

        # All done?
        elif self.on_complete:
            # call back once, then drop it
            self.on_complete()
            self.on_complete = None

    def draw(self):
        self.screen.fill((30, 30, 30))

        # border
        pygame.draw.rect(
            self.screen,
            (200, 200, 200),
            (self.bar_x, self.bar_y, self.bar_w, self.bar_h),
            2
        )

        # fill
        if self.total:
            pct = self.loaded / self.total
            fill_w = int((self.bar_w - 4) * pct)
            pygame.draw.rect(
                self.screen,
                (100, 200, 100),
                (self.bar_x + 2, self.bar_y + 2, fill_w, self.bar_h - 4)
            )
