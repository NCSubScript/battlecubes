# scenes/splash_screen.py

import pygame
import moderngl
import time
from typing import List, Optional, Callable
from gl_ui import GLUI

class SplashScreen:
    """
    ModernGL-powered splash screen.
    Loads each logo as a texture (correctly oriented),
    then fades them in/out in sequence, full-screen centered.
    """

    def __init__(
        self,
        ctx: moderngl.Context,
        screen_size: tuple,
        logo_paths: List[str],
        display_time: float = 2.0,
        fade_time: float = 1.0,
        on_complete: Optional[Callable] = None,
    ):
        self.ctx         = ctx
        self.ui          = GLUI(ctx)
        self.screen_w, self.screen_h = screen_size
        self.on_complete = on_complete

        # timings in milliseconds
        self.display_ms = int(display_time * 1000)
        self.fade_ms    = int(fade_time   * 1000)
        self.cycle_ms   = self.display_ms + 2 * self.fade_ms

        # load logos into ModernGL textures
        self.textures: List[moderngl.Texture] = []
        for path in logo_paths:
            surf = pygame.image.load(path).convert_alpha()
            # flip_y=True so OpenGL sees it right-side-up
            raw  = pygame.image.tostring(surf, 'RGBA', True)
            tex  = ctx.texture(surf.get_size(), 4, raw)
            tex.build_mipmaps()
            self.textures.append(tex)

        if not self.textures:
            raise RuntimeError("No splash logos found")

        # center rectangle is full-screen
        self.x, self.y = 0, 0
        self.w, self.h = self.screen_w, self.screen_h

        # start timer
        self.start = pygame.time.get_ticks()
        self.done  = False

    def update(self, events):
        """
        Call every frame with the Pygame event list.
        Skips ahead on any key or mouse press.
        """
        if self.done:
            return

        now     = pygame.time.get_ticks()
        elapsed = now - self.start

        # skip on input
        for e in events:
            if e.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
                self.done = True
                if self.on_complete:
                    self.on_complete()
                return

        # finish after all logos played
        total_duration = len(self.textures) * self.cycle_ms
        if elapsed >= total_duration:
            self.done = True
            if self.on_complete:
                self.on_complete()

    def draw(self):
        """
        Render the current logo with fade-in/out.
        """
        if self.done:
            return

        # clear & enable blending for fades
        self.ctx.clear(0.0, 0.0, 0.0, 1.0)
        self.ctx.enable(moderngl.BLEND)
        self.ctx.blend_func = (
            moderngl.SRC_ALPHA,
            moderngl.ONE_MINUS_SRC_ALPHA,
        )

        # compute which logo and its alpha
        elapsed = pygame.time.get_ticks() - self.start
        idx     = min(elapsed // self.cycle_ms, len(self.textures) - 1)
        in_cycle= elapsed - idx * self.cycle_ms

        if in_cycle < self.fade_ms:
            alpha = in_cycle / self.fade_ms
        elif in_cycle < self.fade_ms + self.display_ms:
            alpha = 1.0
        else:
            alpha = (self.cycle_ms - in_cycle) / self.fade_ms

        # draw it full-screen
        tex = self.textures[idx]
        self.ui.draw_texture(
            texture=tex,
            x=self.x, y=self.y,
            w=self.w, h=self.h,
            alpha=alpha,
        )
