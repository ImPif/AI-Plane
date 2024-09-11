import random
import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

verticies = (
    (.1, -.1, -.1),
    (.1, .1, -.1),
    (-.1, .1, -.1),
    (-.1, -.1, -.1),
    (.2, -.2, .2),
    (.2, .2, .2),
    (-.2, -.2, .2),
    (-.2, .2, .2)
    )

cube_v =[
    [.1, -.1, -.1],
    [.1, .1, -.1],
    [-.1, .1, -.1],
    [-.1, -.1, -.1],
    [.2, -.2, .2],
    [.2, .2, .2],
    [-.2, -.2, .2],
    [-.2, .2, .2]
]

edges = (
    (0,1),
    (0,3),
    (0,4),
    (2,1),
    (2,3),
    (2,7),
    (6,3),
    (6,4),
    (6,7),
    (5,1),
    (5,4),
    (5,7)
    )

t_vertice = (
    (-1, -1, -1),
    (1, 1, 1),
    (0, 0, 0),
    (-2, -2, -2),
    (2, 2, 2),
    (-1, -1, -1)

)

colors = (
    (1,0,0),
    (0,1,0),
    (0,0,1),
    (0,1,0),
    (1,1,1),
    (0,1,1),
    (1,0,0),
    (0,1,0),
    (0,0,1),
    (1,0,0),
    (1,1,1),
    (0,1,1),
    )

surfaces = (
    (0, 1, 2),
    (3, 4, 5)
)

surfaces = (
    (0,1,2,3),
    (3,2,7,6),
    (6,7,5,4),
    (4,5,1,0),
    (1,5,7,2),
    (4,0,3,6)
    )

def Cube():
    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(cube_v[vertex])
    glEnd()
    glBegin(GL_QUADS)
    for surface in surfaces:
        x = 0
        for vertex in surface:
            x += 1
            glColor3fv(colors[x])
            glVertex3fv(cube_v[vertex])
    glEnd()

def linething():
    glBegin(GL_LINES)
    glVertex3fv([1, -1, 1])
    glVertex3fv([-1, -1, -1])
    glEnd()

# def triangle():
#     glBegin(GL_TRIANGLES)
#     for vertex in t_vertice:
#         glVertex3fv(vertex)
#     glEnd()

#     glBegin(GL_TRIANGLES)
#     for surface in surfaces:
#         x = 0
#         for vertex in surface:
#             x += 1
#             glColor3fv(colors[x])
#             glVertex3fv(t_vertice[vertex])
#     glEnd()


def matrix_translation(x, y, z):
    for vertex in range(len(cube_v)):
        cube_v[vertex][0] += x
        cube_v[vertex][1] += y
        cube_v[vertex][2] += z


def matrix_rotation()


def main():
    pygame.init()
    display = (800,600)
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)

    gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)

    glTranslatef(0,0, -10)

    glRotatef(25, 2, 1, 0)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    glTranslatef(-0.5,0,0)
                if event.key == pygame.K_RIGHT:
                    glTranslatef(0.5,0,0)

                if event.key == pygame.K_LEFTBRACKET:
                    matrix_rotation()

                if event.key == pygame.K_RIGHTBRACKET:
                    matrix_rotation()

                if event.key == pygame.K_UP:
                    matrix_translation(0,1,0)
                if event.key == pygame.K_DOWN:
                    glTranslatef(0,-1,0)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:
                    glTranslatef(0,0,1.0)

                if event.button == 5:
                    glTranslatef(0,0,-1.0)

        #glRotatef(1, 3, 1, 1)
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        Cube()
        pygame.display.flip()
        pygame.time.wait(10)

main()        