import pygame
from pygame.locals import DOUBLEBUF, OPENGL, QUIT, KEYUP, K_ESCAPE

from OpenGL.GL import *
from OpenGL.GL import shaders as gl_shaders  # wrapper

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
        self.resolution = 1920, 1080
        # self.resolution = 3840, 2160
        pygame.display.set_mode(self.resolution, DOUBLEBUF | OPENGL)

        #################################################
        # Create shaders and programs ( vertex + frag ) #
        #################################################

        # shaders compilation
        gl_shaders.compileShader(VERTEX_SHADER_IM, GL_VERTEX_SHADER)
        display_sh = gl_shaders.compileShader(FRAGMENT_SHADER_IM, GL_FRAGMENT_SHADER)
        a_sh = gl_shaders.compileShader(FRAGMENT_SHADER_A, GL_FRAGMENT_SHADER)
        b_sh = gl_shaders.compileShader(FRAGMENT_SHADER_B, GL_FRAGMENT_SHADER)

        # programs creation
        self.display_prog = gl_shaders.compileProgram(display_sh)
        self.a_prog = gl_shaders.compileProgram(a_sh)
        self.b_prog = gl_shaders.compileProgram(b_sh)

        # get and send uniforms
        glUseProgram(self.display_prog)
        glUniform2f(glGetUniformLocation(self.display_prog, 'iResolution'), *self.resolution)
        self.display_channel_a = glGetUniformLocation(self.display_prog, "iChannel0")
        self.display_channel_b = glGetUniformLocation(self.display_prog, "iChannel1")
        glUseProgram(self.a_prog)
        glUniform2f(glGetUniformLocation(self.a_prog, 'iResolution'), *self.resolution)
        self.a_prog_channel_a = glGetUniformLocation(self.a_prog, "kernelTexture")
        self.a_prog_channel_b = glGetUniformLocation(self.a_prog, "iChannel1")
        glUseProgram(self.b_prog)
        glUniform2f(glGetUniformLocation(self.b_prog, 'iResolution'), *self.resolution)
        self.uni_mouse = glGetUniformLocation(self.b_prog, 'iMouse')
        self.b_prog_channel_a = glGetUniformLocation(self.b_prog, "kernelTexture")
        self.b_prog_channel_b = glGetUniformLocation(self.b_prog, "iChannel1")

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
        glActiveTexture(GL_TEXTURE1)
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
        glActiveTexture(GL_TEXTURE2)
        glBindTexture(GL_TEXTURE_2D, self.texture_b)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RG32F, *self.resolution, 0, GL_RG, GL_BYTE, None)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

        self.b_fb = glGenFramebuffers(1)
        glBindFramebuffer(GL_FRAMEBUFFER, self.b_fb)
        glFramebufferTexture2D(GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT0, GL_TEXTURE_2D, self.texture_b, 0)

        self.clock = pygame.time.Clock()

    def mainloop(self):

        mouse_pos = pygame.mouse.get_pos()

        while 1:
            self.clock.tick(120)  # cap fps

            for event in pygame.event.get():
                if pygame.mouse.get_pressed()[0]:  # left mouse button pressed
                    mouse_pos = pygame.mouse.get_pos()
                if (event.type == QUIT) or (event.type == KEYUP and event.key == K_ESCAPE):
                    pygame.quit()
                    exitsystem()

            glBindFramebuffer(GL_FRAMEBUFFER, self.a_fb)
            glUseProgram(self.a_prog)
            glUniform1i(self.a_prog_channel_a, self.texture_a)
            glUniform1i(self.a_prog_channel_b, self.texture_b)
            glDrawArrays(GL_QUADS, 0, 4)

            glBindFramebuffer(GL_FRAMEBUFFER, self.b_fb)
            glUseProgram(self.b_prog)
            glUniform1i(self.b_prog_channel_a, self.texture_a)
            glUniform1i(self.b_prog_channel_b, self.texture_b)
            glUniform2f(self.uni_mouse, *mouse_pos)
            glDrawArrays(GL_QUADS, 0, 4)

            glBindFramebuffer(GL_FRAMEBUFFER, 0)
            glUseProgram(self.display_prog)
            glUniform1i(self.display_channel_a, self.texture_a)
            glUniform1i(self.display_channel_b, self.texture_b)
            glDrawArrays(GL_QUADS, 0, 4)

            pygame.display.set_caption(f"FPS: {self.clock.get_fps():.0f}")
            pygame.display.flip()  # Update the full display Surface to the screen


if __name__ == '__main__':
    ColorSound().mainloop()
