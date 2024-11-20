import numpy as np
import pygame
from pygame.locals import *
import math
from OpenGL.GL import *
from OpenGL.GLU import *
class Plaine:

    def __init__(self, plane_array, plane_edges, surfaces, colors, direction_vector, lift_vector, thrust, max_thrust, velocity, max_velocity, starting_x=0, starting_y=0):
        self.edges = plane_edges
        self.surfaces = surfaces
        self.colors = colors
        self.direction_vector = direction_vector
        self.lift_vector = lift_vector
        self.thrust = thrust
        self.max_thrust = max_thrust
        self.velocity = velocity
        self.max_velocity = max_velocity
        self.array3d = self.plane_initializer(starting_x, starting_y, plane_array)

    def __str__(self):
        return np.array2string(self.array3d)

    #Initialize position of plane
    def plane_initializer(self, x, y, array3d):
        array3d = np.array(array3d)        
        array3d += np.array([x, y, 0])
        return array3d
    
    #Call function to render plane array
    def __call__(self):
        self.translate_along_direction()
        self.translate_lift()
        self.translate_gravity()
        self.change_velocity()
        self.cube(self.array3d)
        self.bound()

    #makes sure plane is within visible bounds
    def bound(self):
        if self.array3d[0,0] > 62:
            for vertex in self.array3d:
                vertex[0] = vertex[0] - 124
        elif self.array3d[0,0] < -62:
            for vertex in self.array3d:
                vertex[0] = vertex[0] + 124
        if self.array3d[0,1] > 33:
            for vertex in self.array3d:
                vertex[1] = vertex[1] - 66
        elif self.array3d[0,1] < -33:
            for vertex in self.array3d:
                vertex[1] = vertex[1] + 66

    #renders plane array
    def cube(self, array):
        glBegin(GL_LINES)
        for edge in self.edges:
            for vertex in edge:
                glVertex3fv(array[vertex])
        glEnd()
        glBegin(GL_QUADS)
        for surface in self.surfaces:
            x = 0
            for vertex in surface:
                x += 1
                glColor3fv(self.colors[x])
                glVertex3fv(array[vertex])
        glEnd()
    
    #rotate direction vector which determines the direction the plane moves
    def rotate_direction_vector(self, theta):
        rotate_matrix = np.array([
        [math.cos(theta), -math.sin(theta), 0],
        [math.sin(theta), math.cos(theta), 0],
        [0, 0, 1]
        ])
        self.direction_vector = np.dot(rotate_matrix, self.direction_vector)
        self.lift_vector = np.dot(rotate_matrix, self.lift_vector)

    #translates in the direction of the direction vector
    def translate_along_direction(self):
        for vertex in self.array3d:
            vertex[0] += self.direction_vector[0] * self.velocity
            vertex[1] += self.direction_vector[1] * self.velocity
    
    #translate along the lift vector
    def translate_lift(self):
        for vertex in self.array3d:
            vertex[0] += self.lift_vector[0] * (self.velocity * 0.5)
            vertex[1] += self.lift_vector[1] * (self.velocity * 0.5)

    #translate straight down(gravity)
    def translate_gravity(self):
        for vertex in self.array3d:
            vertex[1] -= 0.01
    
    #increases or decrease velocity based off of thrust
    def change_velocity(self):
        if (self.velocity < self.max_velocity and self.velocity < (self.thrust * 0.1)):
            self.velocity += 0.001
        elif (self.velocity > self.max_velocity):
            self.velocity -= 0.001
        if self.velocity > (self.thrust * 0.1):
            self.velocity -= 0.0001

    #takes movement input and changes thrust, lift, and rotation accordingly
    def movement(self, event):
        if event.key == pygame.K_LEFT:
            self.rotate_direction_vector(0.2)
        elif event.key == pygame.K_RIGHT:
            self.rotate_direction_vector(-0.2)
        elif event.key == pygame.K_UP:
            self.thrust = min(self.thrust + 0.1, self.max_thrust)
            self.lift_vector = self.lift_vector + np.array([0, 0.01, 0])
            # print("Thrust: ", self.thrust, "\nVelocity: ", self.velocity)
        elif event.key == pygame.K_DOWN:
            self.thrust = max(self.thrust - 0.1, 0)
            self.lift_vector = self.lift_vector - np.array([0, 0.01, 0])
            # print("Thrust: ", self.thrust, "\nVelocity: ", self.velocity)





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
