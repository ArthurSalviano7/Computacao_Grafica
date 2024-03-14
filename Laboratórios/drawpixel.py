import pygame as pg
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

def wc_to_ndc(x, y, x_min, x_max, y_min, y_max):
    ndc_x = (x - x_min) / (x_max - x_min)
    ndc_y = (y - y_min) / (y_max - y_min)
    return ndc_x, ndc_y

def ndc_to_dc(ndc_x, ndc_y, ndh, ndv):  
    dc_x = round(ndc_x * (ndh - 1))
    dc_y = round(ndc_y * (ndv - 1))
    return dc_x, dc_y

def draw_pixel(dc_x, dc_y):
    glPointSize(2.0) #Alterar tamanho do Pixel
    glBegin(GL_POINTS)
    glColor3f(1.0, 1.0, 1.0)
    glVertex2f(dc_x, dc_y) 
    glEnd()

def main():
    pg.init()
    info = pg.display.Info()
    width = info.current_w - 100
    height = info.current_h - 100
    display = (width, height)
    screen = pg.display.set_mode(display, DOUBLEBUF | OPENGL)

    gluOrtho2D(-1, 1, -1, 1) 

    # WC coordenadas
    wc_x_min = 10.5
    wc_x_max = 20.3
    wc_y_min = 10.5
    wc_y_max = 20.3
    wc_x = 12.2
    wc_y = 12.2

    ndc_coordinates = wc_to_ndc(wc_x, wc_y, wc_x_min, wc_x_max, wc_y_min, wc_y_max)
    dc_coordinates = ndc_to_dc(ndc_coordinates[0], ndc_coordinates[1], info.current_w, info.current_h)

    print(f"Coordenadas WC: X = {wc_x}, Y = {wc_y}")
    print(f"Coordenadas NDC: X = {ndc_coordinates[0]}, Y = {ndc_coordinates[1]}")
    print(f"Coordenadas DC: X = {dc_coordinates[0]}, Y = {dc_coordinates[1]}")

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        draw_pixel(ndc_coordinates[0], ndc_coordinates[1])
        pg.display.flip()

if __name__ == "__main__":
    main()
