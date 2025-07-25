# main.py

import pygame
import moderngl
from resource_manager import ResourceManager
from scenes.splash_screen import SplashScreen
from scenes.loading_screen import LoadingScreen
from scenes.intro_menu   import IntroMenu


# your screen setup
SCREEN_WIDTH  = 1024
SCREEN_HEIGHT = 768

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.OPENGL | pygame.DOUBLEBUF)
clock  = pygame.time.Clock()

# initialize your ResourceManager (e.g. wraps ModernGL context, file I/O, etc.)
mgl_ctx = moderngl.create_context()
rm = ResourceManager(mgl_ctx)

# We'll keep the loading_screen instance around so we can
# pull assets out of rm when it's done.
loading_screen: LoadingScreen

def start_intro_menu():
    global current_scene, rm

    # grab loaded assets from ResourceManager
    bg     = rm.get_image("menu_bg")
    font_t = rm.get_font("font_thin", 24)
    font_b = rm.get_font("font_bold", 24)
    # any other calls: rm.get_sound("…")

    current_scene = IntroMenu(
        screen     = screen,
        background = bg,
        font_thin  = font_t,
        font_bold  = font_b,
        # pass along other rm.get_* assets as needed
    )

def start_loading():
    global current_scene, loading_screen, rm

    # define what to load (kind, key, path[, size])
    manifest = [
        ("image", "menu_bg",   "assets/images/menu_bg.png"),
        ("font",  "font_thin", "assets/fonts/Kubus-Thin.ttf", 24),
        ("font",  "font_bold", "assets/fonts/Kubus-Bold.ttf", 24),
        #("sound", "music",     "assets/sounds/music.ogg"),
        # add more ("image"|"sound"|"font", key, path[, size]) entries here
    ]

    loading_screen = LoadingScreen(
        screen       = screen,
        resource_mgr = rm,
        asset_manifest = manifest,
        on_complete  = start_intro_menu
    )
    current_scene = loading_screen

# start with logo splash (no ResourceManager)
current_scene = SplashScreen(
    screen      = screen,
    logo_paths  = [
        "assets/images/logo1.png",
        "assets/images/logo2.png",
    ],
    display_time = 2.0,
    fade_time    = 1.0,
    on_complete  = start_loading
)

# main loop
running = True
while running:
    events = pygame.event.get()
    for ev in events:
        if ev.type == pygame.QUIT:
            running = False

    current_scene.update(events)
    current_scene.draw()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
