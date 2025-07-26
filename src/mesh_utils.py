# mesh_utils.py

import numpy as np

def build_unit_cube(ctx, program):
    """
    Build a 1×1×1 cube (centered at origin) with per‐vertex normals.
    Returns:
      vao         – a moderngl.VertexArray bound to ctx.programs['basic3d']
      vertex_count– number of vertices (36)
    """
    # 6 faces × 2 triangles × 3 verts = 36 verts
    # Each vert: position (x,y,z) + normal (nx,ny,nz)
    vertices = np.array([
        # back face (−Z)
         0.5, -0.5, -0.5,   0.0,  0.0, -1.0,
        -0.5, -0.5, -0.5,   0.0,  0.0, -1.0,
        -0.5,  0.5, -0.5,   0.0,  0.0, -1.0,
         0.5, -0.5, -0.5,   0.0,  0.0, -1.0,
        -0.5,  0.5, -0.5,   0.0,  0.0, -1.0,
         0.5,  0.5, -0.5,   0.0,  0.0, -1.0,

        # front face (+Z)
        -0.5, -0.5,  0.5,   0.0,  0.0,  1.0,
         0.5, -0.5,  0.5,   0.0,  0.0,  1.0,
         0.5,  0.5,  0.5,   0.0,  0.0,  1.0,
        -0.5, -0.5,  0.5,   0.0,  0.0,  1.0,
         0.5,  0.5,  0.5,   0.0,  0.0,  1.0,
        -0.5,  0.5,  0.5,   0.0,  0.0,  1.0,

        # left face (−X)
        -0.5, -0.5, -0.5,  -1.0,  0.0,  0.0,
        -0.5, -0.5,  0.5,  -1.0,  0.0,  0.0,
        -0.5,  0.5,  0.5,  -1.0,  0.0,  0.0,
        -0.5, -0.5, -0.5,  -1.0,  0.0,  0.0,
        -0.5,  0.5,  0.5,  -1.0,  0.0,  0.0,
        -0.5,  0.5, -0.5,  -1.0,  0.0,  0.0,

        # right face (+X)
         0.5, -0.5,  0.5,   1.0,  0.0,  0.0,
         0.5, -0.5, -0.5,   1.0,  0.0,  0.0,
         0.5,  0.5, -0.5,   1.0,  0.0,  0.0,
         0.5, -0.5,  0.5,   1.0,  0.0,  0.0,
         0.5,  0.5, -0.5,   1.0,  0.0,  0.0,
         0.5,  0.5,  0.5,   1.0,  0.0,  0.0,

        # bottom face (−Y)
        -0.5, -0.5, -0.5,   0.0, -1.0,  0.0,
         0.5, -0.5, -0.5,   0.0, -1.0,  0.0,
         0.5, -0.5,  0.5,   0.0, -1.0,  0.0,
        -0.5, -0.5, -0.5,   0.0, -1.0,  0.0,
         0.5, -0.5,  0.5,   0.0, -1.0,  0.0,
        -0.5, -0.5,  0.5,   0.0, -1.0,  0.0,

        # top face (+Y)
        -0.5,  0.5,  0.5,   0.0,  1.0,  0.0,
         0.5,  0.5,  0.5,   0.0,  1.0,  0.0,
         0.5,  0.5, -0.5,   0.0,  1.0,  0.0,
        -0.5,  0.5,  0.5,   0.0,  1.0,  0.0,
         0.5,  0.5, -0.5,   0.0,  1.0,  0.0,
        -0.5,  0.5, -0.5,   0.0,  1.0,  0.0,
    ], dtype='f4')

    # upload to GPU
    vbo = ctx.buffer(vertices.tobytes())

    # bind to your basic3d program (must be loaded into ctx.programs)
    vao = ctx.vertex_array(program, [
        (vbo, '3f 3f', 'in_pos', 'in_normal'),
    ])

    return vao, vertices.shape[0] // 6
