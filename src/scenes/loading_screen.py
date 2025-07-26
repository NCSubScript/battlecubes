# scenes/loading_screen.py

import pygame
from typing import List, Tuple, Optional, Callable, Any
from gl_ui   import GLUI
from resource_manager import ResourceManager

class LoadingScreen:
    """
    Loads assets via ResourceManager, shows a GL‐drawn progress bar.
    """

    def __init__(
        self,
        ctx,
        screen_size: tuple,
        resource_mgr: ResourceManager,
        asset_manifest: List[Tuple],
        on_complete: Optional[Callable] = None
    ):
        self.ctx   = ctx
        self.ui    = GLUI(ctx)
        self.w, self.h = screen_size
        self.rm    = resource_mgr
        self.man   = asset_manifest[:]
        self.on_complete = on_complete

        self.total  = len(self.man)
        self.loaded = 0
        self.done   = False

    def update(self, events):
        if self.loaded < self.total:
            entry = self.man[self.loaded]
            kind  = entry[0].lower()
            try:
                if kind == 'image':
                    _, key, path = entry
                    self.rm.load_image(key, path)
                    self.rm.load_texture(key, path)

                elif kind == 'sound':
                    _, key, path = entry
                    self.rm.load_sound(key, path)

                elif kind == 'font':
                    _, key, path, size = entry
                    self.rm.load_font(key, path, size)

                else:
                    print(f"[Loading] unknown kind {kind}")
            except Exception as e:
                print(f"[Loading] failed {entry}: {e}")
            finally:
                self.loaded += 1

        elif not self.done:
            self.done = True
            if self.on_complete:
                self.on_complete()

    def draw(self):
        # clear to dark grey
        self.ctx.clear(0.1, 0.1, 0.1, 1.0)

        # draw outer bar
        bar_w, bar_h = self.w * 0.6, 30
        x0 = (self.w - bar_w) / 2
        y0 = (self.h - bar_h) / 2

        # border
        self.ui.draw_rect(x0 - 2, y0 - 2, bar_w + 4, bar_h + 4, (200,200,200))
        # fill
        if self.total:
            pct = self.loaded / self.total
        else:
            pct = 1.0
        self.ui.draw_rect(x0, y0, bar_w*pct, bar_h, (100,200,100))
