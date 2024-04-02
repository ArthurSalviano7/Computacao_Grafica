import pygame as pg
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

def draw_pixel(dc_x, dc_y):
    glBegin(GL_POINTS)
    glColor3f(1.0, 0.0, 0.0)
    glVertex2f(dc_x, dc_y) 
    glEnd()

def DDA(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1

    length = max(abs(dx), abs(dy))

    if length != 0:
        x_increment = dx / length
        y_increment = dy / length
    else:
        x_increment = 0
        y_increment = 0

    x = x1
    y = y1

    points = []
    points.append((round(x), round(y)))

    draw_pixel(round(x), round(y))

    while(x < x2):
        x += x_increment
        y += y_increment
        points.append((round(x), round(y)))
        draw_pixel(round(x), round(y))
    
    return points

def printPontos(points):
    for element in points:
        print(element)

    
pg.init()
info = pg.display.Info()
height = info.current_h
width = info.current_w 
display = (width, height)
screen = pg.display.set_mode(display, DOUBLEBUF | OPENGL)

def main():

    gluOrtho2D(-width/2, width/2, -height/2, height/2)

    x1, y1 = -100, -200
    x2, y2 = 200, 350

    print("Pontos da reta:")

    printPontos(DDA(x1, y1, x2, y2))

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        DDA(x1, y1, x2, y2)
        pg.display.flip()

if __name__ == "__main__":
    main()
