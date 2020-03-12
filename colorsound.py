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
        self.display_prog = gl_shaders.compileProgram(display_sh)
        self.a_prog = gl_shaders.compileProgram(a_sh)
        self.b_prog = gl_shaders.compileProgram(b_sh)

        # on envoit les uniforms
        glUseProgram(self.display_prog)
        glUniform2f(glGetUniformLocation(self.display_prog, 'iResolution'), *self.resolution)
        glUseProgram(self.a_prog)
        glUniform2f(glGetUniformLocation(self.a_prog, 'iResolution'), *self.resolution)
        glUseProgram(self.b_prog)
        glUniform2f(glGetUniformLocation(self.b_prog, 'iResolution'), *self.resolution)
        self.uni_mouse = glGetUniformLocation(self.b_prog, 'iMouse')

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

        ################
        # Framebuffers #
        ################

        self.texture_a = glGenTextures(1)
        glActiveTexture(GL_TEXTURE0 + 1)
        glBindTexture(GL_TEXTURE_2D, self.texture_a)
        # with GL_RGBA16F, light artifacts
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA32F, *self.resolution, 0, GL_RGBA, GL_BYTE, None)
        # important: store negative values
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)  # nearest ?
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

        self.a_fb = glGenFramebuffers(1)
        glBindFramebuffer(GL_FRAMEBUFFER, self.a_fb)
        glFramebufferTexture2D(GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT0, GL_TEXTURE_2D, self.texture_a, 0)

        self.texture_b = glGenTextures(1)
        glActiveTexture(GL_TEXTURE0 + 2)  # num texture
        glBindTexture(GL_TEXTURE_2D, self.texture_b)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA32F, *self.resolution, 0, GL_RGBA, GL_BYTE, None)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)  # nearest ?
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

        self.b_fb = glGenFramebuffers(1)
        glBindFramebuffer(GL_FRAMEBUFFER, self.b_fb)
        glFramebufferTexture2D(GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT0, GL_TEXTURE_2D, self.texture_b, 0)

        self.clock = pygame.time.Clock()

    def mainloop(self):
        while 1:
            self.clock.tick(60)  # cap fps

            for event in pygame.event.get():
                if (event.type == QUIT) or (event.type == KEYUP and event.key == K_ESCAPE):
                    pygame.quit()
                    exitsystem()

            channel_a = glGetUniformLocation(self.a_prog, "iChannel0")
            channel_b = glGetUniformLocation(self.a_prog, "iChannel1")

            glActiveTexture(GL_TEXTURE0 + 1)
            glBindFramebuffer(GL_FRAMEBUFFER, self.a_fb)
            glUseProgram(self.a_prog)
            glUniform1i(channel_a, self.texture_a)
            glUniform1i(channel_b, self.texture_b)
            glDrawArrays(GL_QUADS, 0, 4)

            channel_a = glGetUniformLocation(self.b_prog, "iChannel0")
            channel_b = glGetUniformLocation(self.b_prog, "iChannel1")

            glActiveTexture(GL_TEXTURE0 + 2)
            glBindFramebuffer(GL_FRAMEBUFFER, self.b_fb)
            glUseProgram(self.b_prog)
            glUniform1i(channel_a, self.texture_a)
            glUniform1i(channel_b, self.texture_b)
            glUniform2f(self.uni_mouse, *pygame.mouse.get_pos())
            glDrawArrays(GL_QUADS, 0, 4)

            channel_a = glGetUniformLocation(self.display_prog, "iChannel0")
            channel_b = glGetUniformLocation(self.display_prog, "iChannel1")

            glActiveTexture(GL_TEXTURE0)
            glBindFramebuffer(GL_FRAMEBUFFER, 0)
            glUseProgram(self.display_prog)
            glUniform1i(channel_a, self.texture_a)
            glUniform1i(channel_b, self.texture_b)
            glDrawArrays(GL_QUADS, 0, 4)

            pygame.display.flip()  # Update the full display Surface to the screen


if __name__ == '__main__':
    ColorSound().mainloop()
