# src/screens/gl_renderer.py

from OpenGL.GL import *
import math

class GLRenderer:
    def __init__(self):
        self.angle = 0.0

    def render(self):
        # Slowly increment rotation
        self.angle = (self.angle + 0.5) % 360

        # Reset ModelView, position camera
        glLoadIdentity()
        glTranslatef(0.0, 0.0, -5.0)
        glRotatef(self.angle, 1.0, 1.0, 0.0)

        # Draw colored cube
        glBegin(GL_QUADS)
        # Front face (red)
        glColor3f(1, 0, 0)
        glVertex3f(-1, -1,  1)
        glVertex3f( 1, -1,  1)
        glVertex3f( 1,  1,  1)
        glVertex3f(-1,  1,  1)
        # Back face (green)
        glColor3f(0, 1, 0)
        glVertex3f(-1, -1, -1)
        glVertex3f(-1,  1, -1)
        glVertex3f( 1,  1, -1)
        glVertex3f( 1, -1, -1)
        # Left face (blue)
        glColor3f(0, 0, 1)
        glVertex3f(-1, -1, -1)
        glVertex3f(-1, -1,  1)
        glVertex3f(-1,  1,  1)
        glVertex3f(-1,  1, -1)
        # Right face (yellow)
        glColor3f(1, 1, 0)
        glVertex3f(1, -1, -1)
        glVertex3f(1,  1, -1)
        glVertex3f(1,  1,  1)
        glVertex3f(1, -1,  1)
        # Top face (cyan)
        glColor3f(0, 1, 1)
        glVertex3f(-1, 1, -1)
        glVertex3f(-1, 1,  1)
        glVertex3f( 1, 1,  1)
        glVertex3f( 1, 1, -1)
        # Bottom face (magenta)
        glColor3f(1, 0, 1)
        glVertex3f(-1, -1, -1)
        glVertex3f( 1, -1, -1)
        glVertex3f( 1, -1,  1)
        glVertex3f(-1, -1,  1)
        glEnd()
