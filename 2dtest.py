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

#rotates either pitch or roll so that the transformation applies properly
#roll == 0, pitch == 1
def transform(matrix,  roll, amount, x, y, type):
    match type:
        case 0:
            return_matrix = transformation_matrix_translationx(matrix, -x)
            return_matrix = transformation_matrix_translationy(return_matrix, -y)
            return_matrix = transformation_matrix_roll(return_matrix, roll)
            return_matrix = transformation_matrix_translationx(return_matrix, x)
            return_matrix = transformation_matrix_translationy(return_matrix, y)
            return return_matrix
        case 1:
            return_matrix = transformation_matrix_translationx(matrix,amount)
            return return_matrix
        case 2:
            return_matrix = transformation_matrix_translationy(matrix, amount)
            return return_matrix
#transformation to move laterally

def transformation_matrix_translationx(matrix, amount):

    for vertex in range(len(matrix)):
        matrix[vertex][1] += amount
    return matrix

def transformation_matrix_translationy(matrix, amount):

    for vertex in range(len(matrix)):
        matrix[vertex][0] += amount
    return matrix
        


#transformation to rotate for roll
def transformation_matrix_roll(matrix, theta):

    rotate_matrix = np.array([
        [math.cos(theta),        math.sin(theta), 0],
        [(-1) * math.sin(theta), math.cos(theta), 0],
        [0,                      0,               1]
        ])

    for vector in range(len(matrix)):
        matrix[vector] = np.dot(rotate_matrix, matrix[vector])

    return matrix

#to do
#add linear transformation to this one
#       it needs to go in the direction
#       the plane is facing rather than
#       parrallel with x y z



# Initialize a direction vector for the plane
direction_vector = np.array([1, 0, 0])  # Points along the x-axis

# Rotate the direction vector using roll (theta)
def rotate_direction_vector(vector, theta):
    rotate_matrix = np.array([
        [math.cos(theta), -math.sin(theta), 0],
        [math.sin(theta), math.cos(theta), 0],
        [0, 0, 1]
    ])
    return np.dot(rotate_matrix, vector)

# Move the matrix along the direction vector
def translate_along_direction(matrix, direction_vector, amount):
    for vertex in matrix:
        vertex[0] += direction_vector[0] * amount
        vertex[1] += direction_vector[1] * amount
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
    ])# Your original vertices
    default_array = np.array([
    [.1, -.1, -.1],
    [.1, .1, -.1],
    [-.1, .1, -.1],
    [-.1, -.1, -.1],
    [.2, -.2, .2],
    [.2, .2, .2],
    [-.2, -.2, .2],
    [-.2, .2, .2]
    ])

    direction_vector = np.array([1, 0, 0])  # Initial direction
    pitch = 0
    lateral = 0
    horizontal = 0

    pygame.init()
    pygame.key.set_repeat(100)
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
                if event.key == pygame.K_KP8:
                    pitch += 0.03
                    direction_vector = rotate_direction_vector(direction_vector, 0.1)
                if event.key == pygame.K_KP2:
                    pitch -= 0.03
                    direction_vector = rotate_direction_vector(direction_vector, -0.1)

                if event.key == pygame.K_UP:
                    array3d = translate_along_direction(array3d, direction_vector, 0.1)
                if event.key == pygame.K_DOWN:
                    array3d = translate_along_direction(array3d, direction_vector, -0.1)

        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        Cube(array3d)
        pygame.display.flip()
        pygame.time.wait(1)

main()        