# src/resource_manager.py

import os
import logging

import pygame
import moderngl

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class ResourceManager:
    """
    Central asset loader/cacher for:
      - pygame.Surface images
      - pygame.mixer.Sound effects/music
      - pygame.font.Font
      - moderngl.Texture
      - moderngl.Program (shaders)
    """

    def __init__(self, mgl_ctx: moderngl.Context):
        self.ctx = mgl_ctx

        self._images   = {}  # path -> pygame.Surface
        self._sounds   = {}  # path -> pygame.mixer.Sound
        self._fonts    = {}  # (path,size) -> pygame.font.Font
        self._textures = {}  # path -> moderngl.Texture
        self._shaders  = {}  # name -> moderngl.Program

    #── Images ----------------------------------------------------------------

    def load_image(self, key: str, path: str = "") -> pygame.Surface:
        """Load and cache a pygame.Surface with alpha."""
        if key in self._images:
            return self._images[key]

        if not os.path.exists(path):
            logger.error(f"Image not found: {path}")
            raise FileNotFoundError(path)

        surf = pygame.image.load(path).convert_alpha()
        self._images[key] = surf
        logger.info(f"Loaded image: {path}")
        return surf

    def get_image(self, key: str) -> pygame.Surface:
        return self._images[key]

    #── Sounds ----------------------------------------------------------------

    def load_sound(self, key: str, path: str) -> pygame.mixer.Sound:
        """Load and cache a Sound."""
        if key in self._sounds:
            return self._sounds[path]

        if not os.path.exists(path):
            logger.error(f"Sound not found: {path}")
            raise FileNotFoundError(path)

        snd = pygame.mixer.Sound(path)
        self._sounds[str] = snd
        logger.info(f"Loaded sound: {path}")
        return snd

    def get_sound(self, path: str) -> pygame.mixer.Sound:
        return self.load_sound(path)

    #── Fonts -----------------------------------------------------------------

    def load_font(self, key: str, path: str, size: int) -> pygame.font.Font:
        """Load and cache a Font by (path, size)."""
        key = (key, size)
        if key in self._fonts:
            return self._fonts[key]

        if not os.path.exists(path):
            logger.error(f"Font not found: {path}")
            raise FileNotFoundError(path)

        font = pygame.font.Font(path, size)
        self._fonts[key] = font
        logger.info(f"Loaded font: {path}@{size}")
        return font

    def get_font(self, key) -> pygame.font.Font:
        return self._fonts[key]

    def get_font(self, key, size) -> pygame.font.Font:
        return self._fonts[(key, size)]
    
    
    #── GPU Textures ----------------------------------------------------------

    def load_texture(self, key, path: str = "", build_mipmaps: bool = True) -> moderngl.Texture:
        """
        Load a pygame.Surface, upload to GPU as RGBA texture,
        generate mipmaps if requested.
        """
        if key in self._textures:
            return self._textures[key]

        surf = self.load_image(key)  # ensures PNG→Surface
        w, h = surf.get_size()
        data = pygame.image.tostring(surf, 'RGBA', False)

        tex = self.ctx.texture((w, h), 4, data)
        if build_mipmaps:
            tex.build_mipmaps()
        self._textures[key] = tex

        logger.info(f"Created GPU texture: {path} ({w}×{h})")
        return tex

    def get_texture(self, key: str) -> moderngl.Texture:
        return self.load_texture(key)

    #── Shaders / Programs ---------------------------------------------------

    def load_shader(
        self,
        name: str,
        vert_path: str,
        frag_path: str,
        geom_path: str = None
    ) -> moderngl.Program:
        """
        Compile and cache a shader program by name.
        vert_path, frag_path, optional geom_path are file paths.
        """
        if name in self._shaders:
            return self._shaders[name]

        def _read_file(p):
            if not os.path.exists(p):
                logger.error(f"Shader file not found: {p}")
                raise FileNotFoundError(p)
            with open(p, 'r') as f:
                return f.read()

        vert_src = _read_file(vert_path)
        frag_src = _read_file(frag_path)
        kwargs   = dict(vertex_shader=vert_src, fragment_shader=frag_src)

        if geom_path:
            geom_src = _read_file(geom_path)
            kwargs['geometry_shader'] = geom_src

        prog = self.ctx.program(**kwargs)
        self._shaders[name] = prog
        logger.info(f"Compiled shader program: {name}")
        return prog

    def get_shader(self, name: str) -> moderngl.Program:
        return self._shaders[name]

    #── Cleanup ---------------------------------------------------------------

    def clear(self):
        """Unload all cached assets."""
        self._images.clear()
        self._sounds.clear()
        self._fonts.clear()
        self._textures.clear()
        self._shaders.clear()
        logger.info("ResourceManager caches cleared.")
