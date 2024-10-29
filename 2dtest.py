import random
import numpy as np
import pygame
from pygame.locals import *
import math

from OpenGL.GL import *
from OpenGL.GLU import *

# Define the edges, vertices, and colors as before
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

cube_v = [
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

# Rotation and transformation functions as before
def transform(matrix, roll, amount, x, y, type):
    match type:
        case 0:
            return_matrix = transformation_matrix_translationx(matrix, -x)
            return_matrix = transformation_matrix_translationy(return_matrix, -y)
            return_matrix = transformation_matrix_roll(return_matrix, roll)
            return_matrix = transformation_matrix_translationx(return_matrix, x)
            return_matrix = transformation_matrix_translationy(return_matrix, y)
            return return_matrix
        case 1:
            return_matrix = transformation_matrix_translationx(matrix, amount)
            return return_matrix
        case 2:
            return_matrix = transformation_matrix_translationy(matrix, amount)
            return return_matrix

def transformation_matrix_translationx(matrix, amount):
    for vertex in range(len(matrix)):
        matrix[vertex][1] += amount
    return matrix

def transformation_matrix_translationy(matrix, amount):
    for vertex in range(len(matrix)):
        matrix[vertex][0] += amount
    return matrix

def transformation_matrix_roll(matrix, theta):
    rotate_matrix = np.array([
        [math.cos(theta), math.sin(theta), 0],
        [(-1) * math.sin(theta), math.cos(theta), 0],
        [0, 0, 1]
    ])
    for vector in range(len(matrix)):
        matrix[vector] = np.dot(rotate_matrix, matrix[vector])
    return matrix

# Rotate the direction vector using roll (theta)
def rotate_direction_vector(vector, theta):
    rotate_matrix = np.array([
        [math.cos(theta), -math.sin(theta), 0],
        [math.sin(theta), math.cos(theta), 0],
        [0, 0, 1]
    ])
    return np.dot(rotate_matrix, vector)

# Move the matrix along the direction vector with adjustable thrust
def translate_along_direction(matrix, direction_vector, thrust):
    for vertex in matrix:
        vertex[0] += direction_vector[0] * thrust
        vertex[1] += direction_vector[1] * thrust
    return matrix

def main():
    array3d = np.array(cube_v)
    direction_vector = np.array([1, 0, 0])  # Initial direction
    thrust = 0.0  # Initial thrust (speed)
    max_thrust = 1.0  # Maximum thrust limit

    pygame.init()
    pygame.key.set_repeat(100)
    display = (1500, 800)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
    glTranslatef(0, 0, -10)
    glRotatef(25, 2, 1, 0)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    direction_vector = rotate_direction_vector(direction_vector, 0.2)
                if event.key == pygame.K_RIGHT:
                    direction_vector = rotate_direction_vector(direction_vector, -0.2)
                if event.key == pygame.K_UP:
                    thrust = min(thrust + 0.01, max_thrust)  # Increase thrust
                if event.key == pygame.K_DOWN:
                    thrust = max(thrust - 0.01, 0)  # Decrease thrust

        # Apply the movement with the current thrust level
        array3d = translate_along_direction(array3d, direction_vector, thrust)

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        Cube(array3d)
        pygame.display.flip()
        pygame.time.wait(10)

main()
