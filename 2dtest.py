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
def translate_along_direction(matrix, direction_vector, velocity):
    for vertex in matrix:
        vertex[0] += direction_vector[0] * velocity
        vertex[1] += direction_vector[1] * velocity
    return matrix

def translate_lift(matrix, lift_vector, velocity):
    for vertex in matrix:
        vertex[0] += lift_vector[0] * (velocity * 0.5)
        vertex[1] += lift_vector[1] * (velocity * 0.5)
    return matrix

def translate_gravity(matrix):
    for vertex in matrix:
        vertex[1] -= 0.01
    return matrix

def change_velocity(max_velocity, thrust, velocity):
    if (velocity < max_velocity):
        velocity += 0.001
        return velocity
    elif (velocity > max_velocity):
        velocity -= 0.001
        return velocity
    return velocity


def main():
    array3d = np.array(cube_v)
    direction_vector = np.array([1, 0, 0])  # Initial direction
    lift_vector = np.array([0,.2,0]) # Initial lift direction
    thrust = 0.0  # Initial thrust (speed)
    max_thrust = 1  # Maximum thrust limit
    velocity = 0.02
    max_velocity = 0.1

    pygame.init()
    pygame.key.set_repeat(100)
    display = (1500, 800)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    gluPerspective(45, (display[0] / display[1]), 0.1, 150.0)
    glTranslatef(0, 0, -80)
    #glRotatef(25, 2, 1, 0)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    direction_vector = rotate_direction_vector(direction_vector, 0.2)
                    lift_vector = rotate_direction_vector(lift_vector, 0.2)
                    print("Left key counter-clockwise")
                    print("Direction Vector: ", direction_vector)
                    print("Lift vector: ", lift_vector, "\n")
                if event.key == pygame.K_RIGHT:
                    direction_vector = rotate_direction_vector(direction_vector, -0.2)
                    lift_vector = rotate_direction_vector(lift_vector, -0.2)
                    print("Right key clockwise")
                    print("Direction Vector: ", direction_vector)
                    print("Lift vector: ", lift_vector, "\n")
                if event.key == pygame.K_UP:
                    thrust = min(thrust + 0.1, max_thrust)  # Increase thrust
                    lift_vector = lift_vector + np.array([0, 0.01, 0])
                    print("Velocity: " , velocity, "\nThrust: ", thrust)
                if event.key == pygame.K_DOWN:
                    thrust = max(thrust - 0.1, 0)  # Decrease thrust
                    lift_vector = lift_vector - np.array([0, 0.01, 0])
                    print("Velocity: " , velocity, "\nThrust: ", thrust)


        # Apply the movement with the current thrust level
        array3d = translate_along_direction(array3d, direction_vector, velocity)
        array3d = translate_lift(array3d, lift_vector, thrust)
        array3d = translate_gravity(array3d)
        velocity = change_velocity(max_velocity, thrust, velocity)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        Cube(array3d)
        pygame.display.flip()
        pygame.time.wait(10)

main()
