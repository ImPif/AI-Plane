from plane import *

def main():
    planes = [Plaine(cube_v, edges, surfaces, colors, np.array([1, 0, 0]), np.array([0,.2,0]), 0, 1, 0.02, 0.1, 10, 10)]
    
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
                    for plane in planes:
                        plane.movement(event)
            
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        for plane in planes:
            plane()
        pygame.display.flip()
        pygame.time.wait(10)

main()