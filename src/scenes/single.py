import math
import numpy as np
import pygame
import moderngl

from mesh_utils import build_unit_cube
from typing import Tuple

def perspective(fovy: float, aspect: float, near: float, far: float) -> np.ndarray:
    """Create a perspective projection matrix."""
    f = 1.0 / math.tan(fovy / 2.0)
    proj = np.zeros((4,4), dtype='f4')
    proj[0,0] = f / aspect
    proj[1,1] = f
    proj[2,2] = (far + near) / (near - far)
    proj[2,3] = (2 * far * near) / (near - far)
    proj[3,2] = -1.0
    return proj

def look_at(eye: np.ndarray, target: np.ndarray, up: np.ndarray) -> np.ndarray:
    """Build a look‐at view matrix."""
    f = target - eye
    f /= np.linalg.norm(f)
    s = np.cross(f, up)
    s /= np.linalg.norm(s)
    u = np.cross(s, f)
    m = np.eye(4, dtype='f4')
    m[0,0:3] = s
    m[1,0:3] = u
    m[2,0:3] = -f
    m[0,3]   = -s.dot(eye)
    m[1,3]   = -u.dot(eye)
    m[2,3]   =  f.dot(eye)
    return m

class SinglePlayerScene:
    def __init__(
        self,
        ctx: moderngl.Context,
        screen_size: Tuple[int, int],
        resource_mgr=None,
    ):
        self.ctx       = ctx
        self.width, self.height = screen_size

        # build cube shader
        vert = '''
        #version 330
        in vec3 in_pos;
        in vec3 in_normal;
        uniform mat4 m_model, m_view, m_proj;
        out vec3 v_normal;
        void main() {
            v_normal = mat3(m_model) * in_normal;
            gl_Position = m_proj * m_view * m_model * vec4(in_pos, 1.0);
        }
        '''
        frag = '''
        #version 330
        in vec3 v_normal;
        uniform vec3 face_colors[6];
        out vec4 f_color;
        void main() {
            vec3 n = normalize(v_normal);
            int idx;
            if (abs(n.x) > abs(n.y) && abs(n.x) > abs(n.z)) {
                idx = (n.x > 0.0) ? 0 : 1;
            } else if (abs(n.y) > abs(n.x) && abs(n.y) > abs(n.z)) {
                idx = (n.y > 0.0) ? 2 : 3;
            } else {
                idx = (n.z > 0.0) ? 4 : 5;
            }
            f_color = vec4(face_colors[idx], 1.0);
        }
        '''
        self.prog = ctx.program(vertex_shader=vert, fragment_shader=frag)

        # default cube‐face colors: [+X,−X, +Y,−Y, +Z,−Z]
        default = [
            (1.0, 0.0, 0.0),
            (1.0, 0.5, 0.0),
            (1.0, 1.0, 1.0),
            (1.0, 1.0, 0.0),
            (0.0, 0.0, 1.0),
            (0.0, 1.0, 0.0),
        ]

        # default is already a list of 6 (r,g,b) tuples
        colors = tuple(default)  
        # assign the array‐of‐vec3 directly
        self.prog['face_colors'].value = colors

        # build unit‐cube VAO
        self.vao, self.vcount = build_unit_cube(ctx, self.prog)

        # camera
        aspect = self.width / self.height
        self.proj = perspective(math.radians(60.0), aspect, 0.1, 100.0)
        eye    = np.array([4.0, 4.0, 4.0], dtype='f4')
        target = np.array([0.0, 0.0, 0.0], dtype='f4')
        up     = np.array([0.0, 1.0, 0.0], dtype='f4')
        self.view = look_at(eye, target, up)

        # interaction state
        self.rot_x = 0.0
        self.rot_y = 0.0
        self.dragging   = False
        self.last_mouse = (0, 0)

    def update(self, events):
        for e in events:
            if e.type == pygame.MOUSEBUTTONDOWN:
                if e.button == 1:  # left
                    self.dragging   = True
                    self.last_mouse = e.pos
                elif e.button == 3:  # right
                    print("→ Face‐turn click at", e.pos)
                    # TODO: ray‐picking & rotate a layer

            elif e.type == pygame.MOUSEBUTTONUP and e.button == 1:
                self.dragging = False

            elif e.type == pygame.MOUSEMOTION and self.dragging:
                mx, my = e.pos
                lx, ly = self.last_mouse
                dx = mx - lx
                dy = my - ly
                self.rot_x += dy * 0.005
                self.rot_y += dx * 0.005
                self.last_mouse = (mx, my)

    def draw(self):
        # 1) Ensure viewport is correct
        self.ctx.viewport = (0, 0, self.width, self.height)
        self.ctx.clear(0.1, 0.1, 0.1, 1.0, depth=1.0)
        self.ctx.enable(moderngl.DEPTH_TEST)
        self.ctx.disable(moderngl.CULL_FACE)
        self.ctx.polygon_mode = moderngl.LINES

        # 3) Turn on depth‐test, but disable culling so we can't hide the cube by winding
        self.ctx.enable(moderngl.DEPTH_TEST)
        self.ctx.disable(moderngl.CULL_FACE)

        # Debug log
        # (watch your console to confirm draw() actually ran)
        print("SinglePlayerScene.draw()")

        # 4) Build your orbiting model matrix (same as before)
        cx = math.cos(self.rot_x); sx = math.sin(self.rot_x)
        cy = math.cos(self.rot_y); sy = math.sin(self.rot_y)

        rx = np.array([
            [1,  0,   0, 0],
            [0, cx, -sx, 0],
            [0, sx,  cx, 0],
            [0,  0,   0, 1],
        ], dtype='f4')

        ry = np.array([
            [ cy, 0, sy, 0],
            [  0, 1,  0, 0],
            [-sy, 0, cy, 0],
            [  0, 0,  0, 1],
        ], dtype='f4')

        orbit = ry @ rx

        # 5) Upload view/proj once
        self.prog['m_view'].write(self.view.tobytes())
        self.prog['m_proj'].write(self.proj.tobytes())
        self.prog['m_model'].write(orbit.tobytes())

        # 6) Draw *one* cube at the origin
        model = orbit  # no translation
        # self.prog['m_model'].write(model.tobytes())
        self.vao.render(moderngl.TRIANGLES)

        # 7) (Don’t disable DEPTH_TEST here while debugging)
        # self.ctx.disable(moderngl.DEPTH_TEST)
