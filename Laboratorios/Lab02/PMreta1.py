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

def pontoMedio(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1

    points = []

    d = 2 * dy - dx
    incE = 2 * dy
    incNE = 2 * (dy - dx)

    x = x1
    y = y1

    points.append((round(x), round(y)))
    draw_pixel(round(x), round(y))

    while(x < x2):
        if (d <= 0):
            d += incE
            x += 1
        else:
            d += incNE
            x += 1
            y += 1
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

    x1, y1 = 150, 100
    x2, y2 = 300, 200

    print("Pontos da reta")
    printPontos(pontoMedio(x1, y1, x2, y2))

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        pontoMedio(x1, y1, x2, y2)
        pg.display.flip()

if __name__ == "__main__":
    main()