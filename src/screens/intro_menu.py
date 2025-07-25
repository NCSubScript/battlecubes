# intro_menu.py

import sys
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from .gl_renderer import GLRenderer

def _next_power_of_two(x):
    return 1 << (x - 1).bit_length()

class IntroMenu:
    def __init__(self, screen, bg_path="assets/images/menu_bg.png"):
        self.screen = screen
        self.w, self.h = screen.get_size()
        self.clock = pygame.time.Clock()
        self.renderer = GLRenderer()

        # Enable alpha‐blending for text
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        # 1) Background texture
        bg_surf = pygame.image.load(bg_path).convert_alpha()
        bg_surf = pygame.transform.smoothscale(bg_surf, (self.w, self.h))
        self.bg_tex, self.bg_u, self.bg_v = self._surface_to_texture(bg_surf)

        # 2) Menu‐item textures
        self.font = pygame.font.SysFont(None, 48)
        self.options = ["Start Game", "Options", "Quit"]
        self.selected = 0
        self.textures = []  # (width, height, tex_id, u, v)
        for label in self.options:
            surf = self.font.render(label, True, (255, 255, 255)).convert_alpha()
            tex, u, v = self._surface_to_texture(surf)
            self.textures.append((surf.get_width(), surf.get_height(), tex, u, v))

    def _surface_to_texture(self, surf):
        surf = surf.convert_alpha()
        orig_w, orig_h = surf.get_size()

        # always pad to POT
        pot_w = 1 << (orig_w - 1).bit_length()
        pot_h = 1 << (orig_h - 1).bit_length()
        if pot_w != orig_w or pot_h != orig_h:
            padded = pygame.Surface((pot_w, pot_h), SRCALPHA, 32).convert_alpha()
            padded.blit(surf, (0, 0))
            surf = padded

        w, h = surf.get_size()
        data = pygame.image.tostring(surf, "RGBA", True)

        # Print diagnostics
        max_tex = glGetIntegerv(GL_MAX_TEXTURE_SIZE)
        print(f"[UPLOAD] orig={orig_w}×{orig_h}, pot={pot_w}×{pot_h}, "
            f"upload={w}×{h}, data_bytes={len(data)}, max_tex={max_tex}")

        # Setup
        tex = glGenTextures(1)
        if isinstance(tex, (tuple, list)):
            tex = tex[0]
        glBindTexture(GL_TEXTURE_2D, tex)

        # Reset unpack state
        glPixelStorei(GL_UNPACK_ALIGNMENT,    1)
        glPixelStorei(GL_UNPACK_ROW_LENGTH,   0)
        glPixelStorei(GL_UNPACK_SKIP_PIXELS,  0)
        glPixelStorei(GL_UNPACK_SKIP_ROWS,    0)

        # Error check before
        err0 = glGetError()
        print(f"[BEFORE] glGetError() = 0x{err0:03X}")

        # The upload call
        glTexImage2D(
            GL_TEXTURE_2D, 0, GL_RGBA, w, h, 0,
            GL_RGBA, GL_UNSIGNED_BYTE, data
        )

        # Error check after
        err1 = glGetError()
        print(f"[AFTER ] glGetError() = 0x{err1:03X}")

        # Set parameters (won’t affect upload)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S,     GL_CLAMP)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T,     GL_CLAMP)

        # UV scales
        u = orig_w / float(pot_w)
        v = orig_h / float(pot_h)
        return tex, u, v

    def run(self):
        while True:
            for ev in pygame.event.get():
                if ev.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if ev.type == KEYDOWN:
                    if ev.key == K_UP:
                        self.selected = (self.selected - 1) % len(self.options)
                    elif ev.key == K_DOWN:
                        self.selected = (self.selected + 1) % len(self.options)
                    elif ev.key == K_RETURN:
                        self._activate(self.options[self.selected])

            # 1) Clear
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

            # 2) 3D background pass
            glEnable(GL_DEPTH_TEST)
            self.renderer.render()

            # 3) 2D overlay
            glDisable(GL_DEPTH_TEST)
            glDepthMask(GL_FALSE)

            glMatrixMode(GL_PROJECTION)
            glPushMatrix()
            glLoadIdentity()
            gluOrtho2D(0, self.w, self.h, 0)

            glMatrixMode(GL_MODELVIEW)
            glPushMatrix()
            glLoadIdentity()

            glEnable(GL_TEXTURE_2D)
            glColor4f(1, 1, 1, 1)

            # a) Draw fullscreen background
            glBindTexture(GL_TEXTURE_2D, self.bg_tex)
            glBegin(GL_QUADS)
            glTexCoord2f(0,       self.bg_v); glVertex2f(0,       0)
            glTexCoord2f(self.bg_u, self.bg_v); glVertex2f(self.w,   0)
            glTexCoord2f(self.bg_u, 0       ); glVertex2f(self.w, self.h)
            glTexCoord2f(0,       0       ); glVertex2f(0,       self.h)
            glEnd()

            # b) Draw each menu item
            for i, (tw, th, tex, u, v) in enumerate(self.textures):
                x = (self.w - tw) // 2
                y = self.h // 2 + i * 60

                # highlight selected
                if i == self.selected:
                    glColor4f(1, 1, 0, 1)
                else:
                    glColor4f(1, 1, 1, 1)

                glBindTexture(GL_TEXTURE_2D, tex)
                glBegin(GL_QUADS)
                glTexCoord2f(0, v);    glVertex2f(x,    y)
                glTexCoord2f(u, v);    glVertex2f(x+tw, y)
                glTexCoord2f(u, 0);    glVertex2f(x+tw, y+th)
                glTexCoord2f(0, 0);    glVertex2f(x,    y+th)
                glEnd()

            glDisable(GL_TEXTURE_2D)

            # restore state
            glPopMatrix()
            glMatrixMode(GL_PROJECTION)
            glPopMatrix()
            glMatrixMode(GL_MODELVIEW)
            glDepthMask(GL_TRUE)

            pygame.display.flip()
            self.clock.tick(60)

    def _activate(self, choice):
        if choice == "Quit":
            pygame.quit()
            sys.exit()
        print("Activated:", choice)
