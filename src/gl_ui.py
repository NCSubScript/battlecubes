import numpy as np
import moderngl

class GLUI:
    def __init__(self, ctx: moderngl.Context):
        self.ctx = ctx

        # Build a full‐screen quad (NDC coords: x,y pairs)
        quad = np.array([
            -1.0, -1.0,
             1.0, -1.0,
            -1.0,  1.0,
             1.0,  1.0,
        ], dtype='f4').tobytes()
        self.vbo = ctx.buffer(quad)

        # Color shader (rectangles)
        vert_col = '''
        #version 330
        in vec2 in_pos;
        void main() { gl_Position = vec4(in_pos, 0.0, 1.0); }
        '''
        frag_col = '''
        #version 330
        uniform vec3  u_color;
        uniform float u_alpha;
        out vec4 f_color;
        void main() { f_color = vec4(u_color, u_alpha); }
        '''
        self.col_prog = ctx.program(vertex_shader=vert_col, fragment_shader=frag_col)
        self.col_prog['u_color'].value = (1.0, 1.0, 1.0)
        self.col_prog['u_alpha'].value = 1.0
        self.col_vao = ctx.simple_vertex_array(self.col_prog, self.vbo, 'in_pos')

        # Texture shader (images, logos, text)
        vert_tex = vert_col  # same vertex shader
        frag_tex = '''
        #version 330
        uniform sampler2D u_texture;
        uniform vec4     u_rect;   // x, y, width, height in pixels
        uniform float    u_alpha;
        out vec4 f_color;
        void main() {
            // map window‐coords → [0,1]
            vec2 uv = (gl_FragCoord.xy - u_rect.xy) / u_rect.zw;
            f_color = texture(u_texture, uv) * u_alpha;
        }
        '''
        self.tex_prog = ctx.program(vertex_shader=vert_tex, fragment_shader=frag_tex)
        self.tex_prog['u_texture'].value = 0
        self.tex_prog['u_alpha'].value   = 1.0
        self.tex_prog['u_rect'].value    = (0.0, 0.0, 1.0, 1.0)
        self.tex_vao = ctx.simple_vertex_array(self.tex_prog, self.vbo, 'in_pos')

    def draw_rect(self, x, y, w, h, color):
        """
        Draw a solid (optionally semitransparent) rectangle.
        color can be (r,g,b) or (r,g,b,a) 0–255.
        """
        if len(color) == 3:
            r, g, b = color; a = 255
        else:
            r, g, b, a = color
        r, g, b = r/255.0, g/255.0, b/255.0
        a       = a/255.0

        # scissor to the pixel rect
        bx = int(x)
        by = int(self.ctx.viewport[3] - (y + h))
        self.ctx.scissor = (bx, by, int(w), int(h))

        # set uniforms & draw
        self.col_prog['u_color'].value = (r, g, b)
        self.col_prog['u_alpha'].value = a
        self.col_vao.render(mode=moderngl.TRIANGLE_STRIP)

        self.ctx.scissor = None

    def draw_texture(self, texture, x, y, w, h, alpha=1.0):
        """
        Draw a textured sprite or logo in pixel rect with opacity alpha.
        """
        bx = int(x)
        by = int(self.ctx.viewport[3] - (y + h))
        self.ctx.scissor = (bx, by, int(w), int(h))

        # set uniforms & draw
        self.tex_prog['u_rect'].value  = (bx, by, w, h)
        self.tex_prog['u_alpha'].value = alpha
        texture.use(location=0)
        self.tex_vao.render(mode=moderngl.TRIANGLE_STRIP)

        self.ctx.scissor = None
