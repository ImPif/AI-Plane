import numpy as np
import pygame
from pygame.locals import *
import math
from OpenGL.GL import *
from OpenGL.GLU import *
class Plaine:

    def __init__(self, plane_array, plane_edges, surfaces, colors, direction_vector, lift_vector, thrust, max_thrust, velocity, max_velocity):
        self.array3d = np.array(plane_array)
        self.edges = plane_edges
        self.surfaces = surfaces
        self.colors = colors
        self.direction_vector = direction_vector
        self.lift_vector = lift_vector
        self.thrust = thrust
        self.max_thrust = max_thrust
        self.velocity = velocity
        self.max_velocity = max_velocity
    
    #Call function to render plane array
    def __call__(self):
        self.cube(self.array3d)

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
    
    def rotate_direction_vector(self, theta):
        rotate_matrix = np.array([
        [math.cos(theta), -math.sin(theta), 0],
        [math.sin(theta), math.cos(theta), 0],
        [0, 0, 1]
        ])
        self.direction_vector = np.dot(rotate_matrix, self.direction_vector)

    def translate_along_direction(self):
        for vertex in self.array3d:
            vertex[0] += self.direction_vector[0] * self.velocity
            vertex[1] += self.direction_vector[1] * self.velocity
    
    def translate_lift(self):
        for vertex in self.array3d:
            vertex[0] += self.lift_vector[0] * (self.velocity * 0.5)
            vertex[1] += self.lift_vector[1] * (self.velocity * 0.5)

    def translate_gravity(self):
        for vertex in self.array3d:
            vertex[1] -= 0.01
    
    def change_velocity(self):
        if (self.velocity < self.max_velocity):
            self.velocity += 0.001
            return self.velocity
        elif (self.velocity > self.max_velocity):
            self.velocity -= 0.001
            return self.velocity
        return self.velocity

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













def main():
    plane = Plaine(cube_v, edges, surfaces, colors, np.array([1, 0, 0]), np.array([0,.2,0]), 0, 1, 0.02, 0.1)

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
            
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        plane()
        pygame.display.flip()
        pygame.time.wait(10)

main()