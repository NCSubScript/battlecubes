import sys
import pygame
import moderngl

from resource_manager import ResourceManager
from scenes.splash_screen import SplashScreen
from scenes.loading_screen import LoadingScreen
from scenes.intro_menu    import IntroMenu
from scenes.single        import SinglePlayerScene  # ← new

# resolution
SCREEN_WIDTH  = 1024
SCREEN_HEIGHT = 768

pygame.init()
#
# 1) Request core-profile GL 3.3 + a 24-bit depth buffer *before* you open the window
pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MAJOR_VERSION, 3)
pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MINOR_VERSION, 3)
pygame.display.gl_set_attribute(
    pygame.GL_CONTEXT_PROFILE_MASK,
    pygame.GL_CONTEXT_PROFILE_CORE
)
pygame.display.gl_set_attribute(pygame.GL_DEPTH_SIZE, 24)

screen = pygame.display.set_mode(
    (SCREEN_WIDTH, SCREEN_HEIGHT),
    pygame.OPENGL | pygame.DOUBLEBUF
)

ctx   = moderngl.create_context()
rm    = ResourceManager(ctx)
clock = pygame.time.Clock()

loading_screen: LoadingScreen

def start_intro_menu():
    global current_scene
    current_scene = IntroMenu(
        ctx          = ctx,
        resource_mgr = rm,
        background_key= "menu_bg",
        font_key     = ("font_bold", 24),
        menu_items   = ["Single Player", "Multiplayer", "Learn", "Options", "Exit"],
        callbacks    = [on_single, on_multi, on_learn, on_options, on_exit],
        render_3d    = render_placeholder_3d
    )

def start_loading():
    global current_scene, loading_screen
    manifest = [
        ("image", "menu_bg",   "assets/images/menu_bg.png"),
        ("font",  "font_thin", "assets/fonts/Kubus-Thin.ttf", 24),
        ("font",  "font_bold", "assets/fonts/Kubus-Bold.ttf", 24),
    ]
    loading_screen = LoadingScreen(
        ctx            = ctx,
        screen_size    = (SCREEN_WIDTH, SCREEN_HEIGHT),
        resource_mgr   = rm,
        asset_manifest = manifest,
        on_complete    = start_intro_menu
    )
    current_scene = loading_screen

def on_single():
    print("→ Single Player")
    # swap to SinglePlayerScene
    global current_scene
    current_scene = SinglePlayerScene(
        ctx          = ctx,
        screen_size  = (SCREEN_WIDTH, SCREEN_HEIGHT),
        resource_mgr = rm,
    )

def on_multi():
    print("→ Multiplayer")
    # …

def on_learn():
    print("→ Learn")
    # …

def on_options():
    print("→ Options")
    # …

def on_exit():
    pygame.quit()
    sys.exit()

# Placeholder 3D render callback
def render_placeholder_3d(ctx):
    pass

# start at splash screen
current_scene = SplashScreen(
    ctx          = ctx,
    screen_size  = (SCREEN_WIDTH, SCREEN_HEIGHT),
    logo_paths   = [
        "assets/images/logo1.png",
        "assets/images/logo2.png"
    ],
    display_time = 2.0,
    fade_time    = 1.0,
    on_complete  = start_loading
)

running = True
while running:
    events = pygame.event.get()
    for e in events:
        if e.type == pygame.QUIT:
            running = False

    current_scene.update(events)
    current_scene.draw()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
