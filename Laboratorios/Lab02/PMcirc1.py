import pygame as pg
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

def draw_pixel(dc_x, dc_y):
    glBegin(GL_POINTS)
    glColor3f(0.0, 1.0, 0.0)
    glVertex2f(dc_x, dc_y) 
    glEnd()

def pontoCirculo(x, y):
    draw_pixel(x, y)
    draw_pixel(y, x)
    draw_pixel(y, -x)
    draw_pixel(x, -y)
    draw_pixel(-x, -y)
    draw_pixel(-y, -x)
    draw_pixel(-y, x)
    draw_pixel(-x, y)

def circPontoMedio(raio):
    points = []
    x = 0
    y = raio
    d = round(5/4 - raio)

    points.append((round(x), round(y)))
    pontoCirculo(round(x), round(y))
    
    while(y > x):
        if(d < 0):
            d += 2 * x + 3
        else:
            d += 2 * (x - y) + 5
            y -= 1
        x += 1
        points.append((round(x), round(y)))
        pontoCirculo(round(x), round(y))
    
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

    raio = 50
    
    print("Raio: " + str(raio))
    print("Pontos 1º octante: ")
    print(printPontos(circPontoMedio(raio)))

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        circPontoMedio(raio)
        pg.display.flip()

if __name__ == "__main__":
    main()