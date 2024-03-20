import pygame as pg
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import retaPM

def draw_axes(width, height): #Desenhar eixos X e Y (Verificar gluOrtho2D)
    glBegin(GL_LINES)
    glColor3f(0.30, 0.30, 0.30)  # Cor para o eixo x
    glVertex3f(-width/2, 0.0, 0.0)
    glVertex3f(width/2, 0.0, 0.0)
    glColor3f(0.30, 0.30, 0.30)  # Cor para o eixo y
    glVertex3f(0.0, -height/2, 0.0)
    glVertex3f(0.0, height/2, 0.0)
    glEnd()

def wc_to_ndc(x, y, x_min, x_max, y_min, y_max):
    ndc_x = (x - x_min) / (x_max - x_min)
    ndc_y = (y - y_min) / (y_max - y_min)
    return ndc_x, ndc_y

def ndc_to_dc(ndc_x, ndc_y, ndh, ndv):  
    dc_x = round(ndc_x * (ndh - 1))
    dc_y = round(ndc_y * (ndv - 1))
    return dc_x, dc_y

def draw_pixel(x, y):
    glPointSize(1.0) #Alterar tamanho do Pixel
    glBegin(GL_POINTS)
    glColor3f(1.0, 1.0, 1.0)
    glVertex2f(x, y) 
    glEnd()

def printPontos(points):
    for element in points:
        print(element)

def main():
    pg.init()
    info = pg.display.Info()
    width = info.current_w
    height = info.current_h
    display = (width, height)
    screen = pg.display.set_mode(display, DOUBLEBUF | OPENGL)

    gluOrtho2D(-width/2, width/2, -height/2, height/2) 

    x1, y1 = 20 , 10
    x2, y2 = 150, 90

    print("Pontos da reta:")
    printPontos(retaPM.desenhar_reta_pm(x1, y1, x2, y2))


    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        draw_axes(width, height)
        #draw_pixel(ndc_coordinates[0], ndc_coordinates[1])
        retaPM.desenhar_reta_pm(x1, y1, x2, y2)
        pg.display.flip()

if __name__ == "__main__":
    main()
