import pygame as pg
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import numpy as np

def draw_pixel(dc_x, dc_y):
    glBegin(GL_POINTS)
    glColor3f(1.0, 1.0, 1.0)
    glVertex2f(dc_x, dc_y) 
    glEnd()

def DDA(x0, y0, xEnd, yEnd):
    dx = xEnd - x0
    dy = yEnd - y0
    steps = max(abs(dx), abs(dy))
    xIncrement = dx / steps
    yIncrement = dy / steps
    x = x0
    y = y0
    draw_pixel(round(x), round(y))
    for k in range(int(steps)):
        x += xIncrement
        y += yIncrement
        draw_pixel(round(x), round(y))
    

def square_points(size):
    x = round(size)/2
    y = round(size)/2
    DDA(-x, y, x, y)
    DDA(x, y, x, -y)
    DDA(x, -y, -x, -y)
    DDA(-x, -y, -x, y)

    return (-x,y),(x,y),(x,-y),(-x,-y)

def draw_square(point1,point2,point3,point4):
    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                running = False
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        DDA(point1[0], point1[1], point2[0], point2[1])
        DDA(point2[0], point2[1], point3[0], point3[1])
        DDA(point3[0], point3[1], point4[0], point4[1])
        DDA(point4[0], point4[1], point1[0], point1[1])
        pg.display.flip()


def translate_point(point, tx, ty, w):
    # Construção da matriz de transformação de translação
    translation_matrix = np.array([[1, 0, tx],
                                   [0, 1, ty],
                                   [0, 0, 1]])

    # Convertendo o ponto para um vetor coluna
    point_vector = np.array([[point[0]], [point[1]], [w]])  # w = 1 para pontos

    # Aplicando a transformação de translação multiplicando a matriz de translação pelo vetor do ponto
    translated_point_vector = np.dot(translation_matrix, point_vector)

    # Normalizando as coordenadas homogêneas resultantes
    translated_point = (translated_point_vector[0][0] / translated_point_vector[2][0], 
                        translated_point_vector[1][0] / translated_point_vector[2][0])
    
    return translated_point


def main():
    pg.init()
    info = pg.display.Info()
    height = info.current_h
    width = info.current_w 
    display = (width, height)
    screen = pg.display.set_mode(display, DOUBLEBUF | OPENGL)

    gluOrtho2D(-width/2, width/2, -height/2, height/2)
    
    size = int(input("Insira o tamanho do quadrado: "))
    
    point1, point2, point3, point4 = square_points(size)
    draw_square(point1, point2, point3, point4)

    tx = int(input("Transladar em x: "))
    ty = int(input("Transladar em y: "))

    # Transladar os pontos
    point1 = translate_point(point1, tx, ty,1)
    point2 = translate_point(point2, tx, ty,1)
    point3 = translate_point(point3, tx, ty,1)
    point4 = translate_point(point4, tx, ty,1)

    # Desenhar o quadrado após a translação
    draw_square(point1, point2, point3, point4)


if __name__ == "__main__":
    while(True):
        main()