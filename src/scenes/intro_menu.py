import pygame
import moderngl
from typing import List, Callable, Optional
from gl_ui import GLUI

class IntroMenu:
    def __init__(
        self,
        ctx: moderngl.Context,
        resource_mgr,
        background_key: str,
        font_key: tuple,         # (font_path, size)
        menu_items: List[str],
        callbacks: List[Callable],
        render_3d: Optional[Callable] = None,
    ):
        self.ctx       = ctx
        self.ui        = GLUI(ctx)
        self.rm        = resource_mgr
        self.render_3d = render_3d
        self.items     = menu_items
        self.callbacks = callbacks
        self.selected  = 0

        # viewport size
        _, _, self.screen_w, self.screen_h = ctx.viewport

        # load background texture (flip_y=True to get right-side-up)
        bg_surf = self.rm.get_image(background_key)
        raw     = pygame.image.tostring(bg_surf, 'RGBA', True)
        self.bg_tex = ctx.texture(bg_surf.get_size(), 4, raw)
        self.bg_tex.build_mipmaps()

        # load font
        font_path, font_size = font_key
        pg_font = self.rm.get_font(font_path, font_size)

        # measure total text height
        PADDING = 20
        sizes = [pg_font.render(label, True, (255,255,255)).get_size() for label in self.items]
        total_h = sum(h for _, h in sizes) + (len(sizes)-1) * PADDING
        start_y = (self.screen_h - total_h) // 2

        # build text textures + positions
        self.textures  = []
        self.positions = []
        y = start_y
        for (w_px, h_px), label in zip(sizes, self.items):
            surf = pg_font.render(label, True, (255,255,255))
            raw  = pygame.image.tostring(surf, 'RGBA', True)
            tex  = ctx.texture((w_px, h_px), 4, raw)
            tex.build_mipmaps()
            self.textures.append(tex)

            x = (self.screen_w - w_px) // 2
            self.positions.append((x, y, w_px, h_px))
            y += h_px + PADDING

    def update(self, events: List[pygame.event.EventType]):
        for evt in events:
            if evt.type == pygame.KEYDOWN:
                if evt.key in (pygame.K_UP, pygame.K_w):
                    self.selected = (self.selected - 1) % len(self.items)
                elif evt.key in (pygame.K_DOWN, pygame.K_s):
                    self.selected = (self.selected + 1) % len(self.items)
                elif evt.key in (pygame.K_RETURN, pygame.K_SPACE):
                    self.callbacks[self.selected]()

    def draw(self):
        # clear + enable blending
        self.ctx.clear(0.0, 0.0, 0.0, 1.0)
        self.ctx.enable(moderngl.BLEND)
        self.ctx.blend_func = (moderngl.SRC_ALPHA, moderngl.ONE_MINUS_SRC_ALPHA)

        # fullscreen background
        self.ui.draw_texture(
            self.bg_tex,
            0, 0,
            self.screen_w, self.screen_h,
            1.0
        )

        # optional 3D content
        if self.render_3d:
            self.render_3d(self.ctx)

        # draw menu items
        for idx, (tex, (x, y, w, h)) in enumerate(zip(self.textures, self.positions)):
            # text backer
            self.ui.draw_rect(x - 10, y - 5, w + 20, h + 10, (50, 50, 50, 180))

            # selected outline
            if idx == self.selected:
                self.ui.draw_rect(x - 10, y - 5, w + 20, h + 10, (30, 144, 255, 200))

            # text
            self.ui.draw_texture(tex, x, y, w, h, 1.0)
