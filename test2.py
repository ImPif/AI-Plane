import random
import numpy as np
import pygame
from pygame.locals import *
import math

from OpenGL.GL import *
from OpenGL.GLU import *

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










def Cube(cubeArray):
    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(cubeArray[vertex])
    glEnd()
    glBegin(GL_QUADS)
    for surface in surfaces:
        x = 0
        for vertex in surface:
            x += 1
            glColor3fv(colors[x])
            glVertex3fv(cubeArray[vertex])
    glEnd()

def transformation_matrix_roll(matrix, theta):

    rotate_matrix = np.array([
        [math.cos(theta),        math.sin(theta), 0],
        [(-1) * math.sin(theta), math.cos(theta), 0],
        [0,                      0,               1]
        ])

    for vector in range(len(matrix)):
        matrix[vector] = np.dot(rotate_matrix, matrix[vector])

    return matrix

def transformation_matrix_pitch(matrix, theta):
    
    rotate_matrix = np.array([
        [1,               0,                      0],
        [0, math.cos(theta), (-1) * math.sin(theta)],
        [0, math.sin(theta),        math.cos(theta)]
        ])

    for vector in range(len(matrix)):
        matrix[vector] = np.dot(rotate_matrix, matrix[vector])

    return matrix


def main():
    array3d = np.array([
    [.1, -.1, -.1],
    [.1, .1, -.1],
    [-.1, .1, -.1],
    [-.1, -.1, -.1],
    [.2, -.2, .2],
    [.2, .2, .2],
    [-.2, -.2, .2],
    [-.2, .2, .2]
    ])

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

                #roll left and right
                if event.key == pygame.K_KP4:
                    array3d = transformation_matrix_roll(array3d, 5)
                if event.key == pygame.K_KP6:
                    array3d = transformation_matrix_roll(array3d, -5)

                #pitch up and down
                if event.key == pygame.K_PAGEUP:
                    array3d = transformation_matrix_pitch(array3d, 1)
                if event.key == pygame.K_PAGEDOWN:
                    array3d = transformation_matrix_pitch(array3d, -1)

                #forward and backwards
                if event.key == pygame.K_KP8:
                    x = 5
                if event.key == pygame.K_KP2:
                    x = 5

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:
                    glTranslatef(0,0,1.0)

                if event.button == 5:
                    glTranslatef(0,0,-1.0)

        #glRotatef(1, 3, 1, 1)
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        Cube(array3d)
        pygame.display.flip()
        pygame.time.wait(10)

main()        