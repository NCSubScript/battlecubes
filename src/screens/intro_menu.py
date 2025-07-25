import sys
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from .gl_renderer import GLRenderer

class IntroMenu:
    def __init__(self, screen,
                 bg_path="assets/images/menu_bg.png"):
        self.screen = screen
        self.w, self.h = screen.get_size()
        self.clock = pygame.time.Clock()
        self.renderer = GLRenderer()

        # 1) Load and build GL texture for background
        bg_surf = pygame.image.load(bg_path).convert()
        bg_surf = pygame.transform.smoothscale(bg_surf, (self.w, self.h))
        self.bg_tex = self._surface_to_texture(bg_surf)

        # 2) Menu text options → textures
        self.font = pygame.font.SysFont(None, 48)
        self.options = ["Start Game", "Options", "Quit"]
        self.selected = 0
        self.textures = []
        for opt in self.options:
            surf = self.font.render(opt, True, (255,255,255))
            tex = self._surface_to_texture(surf)
            self.textures.append((surf.get_width(), surf.get_height(), tex))

    def _surface_to_texture(self, surf):

        w, h = surf.get_size()
        data = pygame.image.tostring(surf, "RGBA", True)
        print(f"Uploading texture: {w}×{h}, data bytes: {len(data)}, expected: {w*h*4}")
        
        """
        Upload a Pygame surface to an OpenGL texture.
        Ensures the surface is 32-bit RGBA and sets unpack alignment.
        """
        # 1) Make sure we have an alpha channel
        surf = surf.convert_alpha()

        # 2) Flip & grab raw bytes in RGBA order
        data = pygame.image.tostring(surf, "RGBA", True)
        w, h = surf.get_size()

        # 3) Create & bind the GL texture
        tex = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, tex)

        # 4) Ensure rows are byte-aligned
        glPixelStorei(GL_UNPACK_ALIGNMENT, 1)

        # 5) Set our filters
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

        # 6) Upload!  Now width/height and format/type match our data exactly.
        glTexImage2D(
            GL_TEXTURE_2D, 0, GL_RGBA, w, h, 0,
            GL_RGBA, GL_UNSIGNED_BYTE, data
        )

        return tex

    def run(self):
        # Main loop
        while True:
            for ev in pygame.event.get():
                if ev.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif ev.type == KEYDOWN:
                    if ev.key == K_UP:
                        self.selected = (self.selected - 1) % len(self.options)
                    elif ev.key == K_DOWN:
                        self.selected = (self.selected + 1) % len(self.options)
                    elif ev.key == K_RETURN:
                        self._activate(self.options[self.selected])

            # 1) Clear color AND depth
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

            # 2) 3D Background Pass
            glEnable(GL_DEPTH_TEST)
            self.renderer.render()

            # 3) 2D Overlay Pass
            glDisable(GL_DEPTH_TEST)
            # — set up orthographic projection
            glMatrixMode(GL_PROJECTION)
            glPushMatrix()
            glLoadIdentity()
            gluOrtho2D(0, self.w, self.h, 0)

            glMatrixMode(GL_MODELVIEW)
            glPushMatrix()
            glLoadIdentity()

            glEnable(GL_TEXTURE_2D)

            #   a) Draw full-screen background quad
            glBindTexture(GL_TEXTURE_2D, self.bg_tex)
            glColor3f(1,1,1)
            glBegin(GL_QUADS)
            glTexCoord2f(0,1); glVertex2f(0,   0)
            glTexCoord2f(1,1); glVertex2f(self.w, 0)
            glTexCoord2f(1,0); glVertex2f(self.w, self.h)
            glTexCoord2f(0,0); glVertex2f(0,   self.h)
            glEnd()

            #   b) Draw menu items
            for i, (tw, th, tex) in enumerate(self.textures):
                x = (self.w - tw) // 2
                y = self.h//2 + i*60
                # highlight selected
                color = (1.0,1.0,0.0) if i == self.selected else (1.0,1.0,1.0)
                glColor3f(*color)
                glBindTexture(GL_TEXTURE_2D, tex)
                glBegin(GL_QUADS)
                glTexCoord2f(0,1); glVertex2f(x,    y)
                glTexCoord2f(1,1); glVertex2f(x+tw, y)
                glTexCoord2f(1,0); glVertex2f(x+tw, y+th)
                glTexCoord2f(0,0); glVertex2f(x,    y+th)
                glEnd()

            glDisable(GL_TEXTURE_2D)

            # restore matrices
            glPopMatrix()
            glMatrixMode(GL_PROJECTION)
            glPopMatrix()
            glMatrixMode(GL_MODELVIEW)

            pygame.display.flip()
            self.clock.tick(60)

    def _activate(self, choice):
        if choice == "Quit":
            pygame.quit()
            sys.exit()
        print("Activated:", choice)
