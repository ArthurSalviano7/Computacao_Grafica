import pygame as pg
import numpy as np
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

def draw_pixel(dc_x, dc_y, Red, Green, Blue):
    glBegin(GL_POINTS)
    glColor3f(Red, Green, Blue)
    glVertex2f(dc_x, dc_y) 
    glEnd()

def DDA(x0, y0, xEnd, yEnd, Red, Green, Blue):
    dx = xEnd - x0
    dy = yEnd - y0
    steps = max(abs(dx), abs(dy))
    xIncrement = dx / steps
    yIncrement = dy / steps
    x = x0
    y = y0
    draw_pixel(round(x), round(y), Red, Green, Blue)
    for k in range(int(steps)):
        x += xIncrement
        y += yIncrement
        draw_pixel(round(x), round(y), Red, Green, Blue)
    
def reflexao_em_x(matriz1):

    matrizRef = np.array([[1, 0, 0],
                          [0, -1, 0],
                          [0, 0, 1]])

    matriz2 = np.dot(matrizRef, matriz1)
    return matriz2

def reflexao_em_y(matriz1):

    matrizRef = np.array([[-1, 0, 0],
                          [0, 1, 0],
                          [0, 0, 1]])

    matriz2 = np.dot(matrizRef, matriz1)
    return matriz2

def reflexao_origem(matriz1):

    matrizRef = np.array([[-1, 0, 0],
                          [0, -1, 0],
                          [0, 0, 1]])

    matriz2 = np.dot(matrizRef, matriz1)
    return matriz2

def reflexao_em_reta(matriz1):

    matrizRef = np.array([[0, 1, 0],
                          [1, 0, 0],
                          [0, 0, 1]])

    matriz2 = np.dot(matrizRef, matriz1)
    return matriz2

    #obs.: figura fica no mesmo lugar porque é um quadrado

pg.init()
info = pg.display.Info()
height = info.current_h - 100
width = info.current_w - 100
display = (width, height)
screen = pg.display.set_mode(display, DOUBLEBUF | OPENGL)
pg.display.set_caption("Reflexão")

def main():

    gluOrtho2D(-width/2, width/2, -height/2, height/2)

    matriz1 = np.array([[0, 50, 50, 0], 
                        [0, 0, 50, 50],
                        [1, 1, 1, 1]])

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        DDA(matriz1[0, 0], matriz1[1, 0], matriz1[0, 1], matriz1[1, 1], 1, 0, 0)
        DDA(matriz1[0, 1], matriz1[1, 1], matriz1[0, 2], matriz1[1, 2], 1, 0, 0)
        DDA(matriz1[0, 2], matriz1[1, 2], matriz1[0, 3], matriz1[1, 3], 1, 0, 0)
        DDA(matriz1[0, 3], matriz1[1, 3], matriz1[0, 0], matriz1[1, 0], 1, 0, 0)

        matriz2 = np.array(reflexao_em_x(matriz1))

        DDA(matriz2[0, 0], matriz2[1, 0], matriz2[0, 1], matriz2[1, 1], 0, 1, 0)
        DDA(matriz2[0, 1], matriz2[1, 1], matriz2[0, 2], matriz2[1, 2], 0, 1, 0)
        DDA(matriz2[0, 2], matriz2[1, 2], matriz2[0, 3], matriz2[1, 3], 0, 1, 0)
        DDA(matriz2[0, 3], matriz2[1, 3], matriz2[0, 0], matriz2[1, 0], 0, 1, 0)

        pg.display.flip()

if __name__ == "__main__":
    main()