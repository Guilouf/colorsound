"""
https://jameshfisher.com/2017/10/22/webgl-game-of-life/
"""

import pygame
from pygame.locals import DOUBLEBUF, OPENGL, QUIT, KEYUP, K_ESCAPE

from OpenGL.GL import *
from OpenGL.GL import shaders as gl_shaders # wrapper de plusieurs methodes

from sys import exit as exitsystem

import numpy as np


VERTEX_SHADER_IM = """
#version 330 core
layout(location = 0) in vec3 vPos;
void main()
{
    gl_Position = vec4(vPos, 1.0);
}
"""

with open('render.frag') as frag_im:
    FRAGMENT_SHADER_IM = frag_im.read()

with open('a.frag') as frag_a:
    FRAGMENT_SHADER_A = frag_a.read()

with open('b.frag') as frag_b:
    FRAGMENT_SHADER_B = frag_b.read()


class ColorSound:

    def __init__(self):
        pygame.init()
        self.resolution = 800, 600
        pygame.display.set_mode(self.resolution, DOUBLEBUF | OPENGL)

        ###################################################
        # Créations shaders et programs ( vertex + frag ) #
        ###################################################

        # compilation des shaders
        gl_shaders.compileShader(VERTEX_SHADER_IM, GL_VERTEX_SHADER)
        display_sh = gl_shaders.compileShader(FRAGMENT_SHADER_IM, GL_FRAGMENT_SHADER)
        a_sh = gl_shaders.compileShader(FRAGMENT_SHADER_A, GL_FRAGMENT_SHADER)
        b_sh = gl_shaders.compileShader(FRAGMENT_SHADER_B, GL_FRAGMENT_SHADER)

        # créations des programmes
        display_prog = gl_shaders.compileProgram(display_sh)
        a_prog = gl_shaders.compileProgram(a_sh)
        b_prog = gl_shaders.compileProgram(b_sh)

        # on envoit les uniforms
        glUseProgram(display_prog)
        glUniform2f(glGetUniformLocation(display_prog, 'iResolution'), *self.resolution)

        ##################
        # Vertex buffers #
        ##################

        self.vertex_buffer = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.vertex_buffer)
        vertices = np.array([-1.0, -1.0, 0.0,
                             1.0, -1.0, 0.0,
                             1.0, 1.0, 0.0,
                             -1.0, 1.0, 0.0], dtype='float32')  # 4 triangles, fullscreen
        glBufferData(GL_ARRAY_BUFFER, vertices, GL_STATIC_DRAW)

        glEnableVertexAttribArray(0)  # pointer
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, None)


if __name__ == '__main__':
    ColorSound()
