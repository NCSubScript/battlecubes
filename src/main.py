import sys
import argparse
import pygame
from pygame.locals import *
from OpenGL.GL import *

from OpenGL import GL
from OpenGL.GL import glGetString, GL_EXTENSIONS, glGetIntegerv, GL_MAJOR_VERSION, GL_MINOR_VERSION
from OpenGL.GL import GL_CLAMP, GL_CLAMP_TO_EDGE

from screens.splash_screen   import SplashScreen
from screens.loading_screen  import LoadingScreen
from screens.intro_menu       import IntroMenu

def parse_args():
    parser = argparse.ArgumentParser(description="BattleCubes Launcher")
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Skip splash screens and loading delays"
    )
    return parser.parse_args()

def test_formats():
    print("\n--- TEXTURE UPLOAD MATRIX ---")
    px = bytes([
        255,   0,   0, 255,   # red
          0, 255,   0, 255,   # green
          0,   0, 255, 255,   # blue
        255, 255,   0, 255    # yellow
    ])
    combos = [
        ("RGBA8 ← RGBA", GL_RGBA8, GL_RGBA),
        ("RGBA8 ← BGRA", GL_RGBA8, GL_BGRA),
        ("RGBA  ← RGBA", GL_RGBA,  GL_RGBA),
        ("RGBA  ← BGRA", GL_RGBA,  GL_BGRA),
    ]

    for name, internal, fmt in combos:
        tex = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, tex)
        glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
        glTexImage2D(GL_TEXTURE_2D, 0, internal, 2, 2, 0, fmt, GL_UNSIGNED_BYTE, px)
        err = glGetError()
        print(f"{name:15s} → err = 0x{err:03X}")
        glDeleteTextures([tex])
    print("------------------------------\n")

def has_npot_support():
    # 1) Grab the extensions list
    exts = glGetString(GL_EXTENSIONS).decode().split()
    if "GL_ARB_texture_non_power_of_two" in exts:
        return True

    # 2) Fallback: parse the version string
    version_str = glGetString(GL_VERSION).decode()  # e.g. "2.1.0 …"
    major, minor = map(int, version_str.split()[0].split('.')[:2])
    return (major > 2) or (major == 2 and minor >= 0)

def main():
    args = parse_args()
    debug = args.debug

    pygame.init()
    pygame.font.init()

    pygame.display.set_caption("BattleCubes")

    
    # Ask for 24 bits of depth precision
    pygame.display.gl_set_attribute(pygame.GL_DEPTH_SIZE, 32)

    # Create an OpenGL-enabled, double-buffered window
    screen = pygame.display.set_mode((800, 600), OPENGL | DOUBLEBUF)
    exts = glGetString(GL_EXTENSIONS).decode().split()
    wrap_mode = GL_CLAMP_TO_EDGE if "GL_ARB_texture_non_power_of_two" in exts else GL_CLAMP

    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, wrap_mode)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, wrap_mode)

    test_formats()
    max_tex = glGetIntegerv(GL_MAX_TEXTURE_SIZE)
    print("GL_MAX_TEXTURE_SIZE =", max_tex)


    has_npot_support()

    # Turn on depth testing (optional but typical)
    glEnable(GL_DEPTH_TEST)

    # 1. Splash — skip if debug
    splash = SplashScreen(
        screen,
        image_paths=[
            "assets/images/logo1.png",
            "assets/images/logo2.png",
        ],
        fade_duration=1000,
        display_duration=5000,
        debug=debug
    )
    splash.run()

    # 2. Loading — pass debug to skip delays
    loader = LoadingScreen(screen, debug=debug)
    loader.run()

    # 3. Intro Menu
    menu = IntroMenu(screen)
    menu.run()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()