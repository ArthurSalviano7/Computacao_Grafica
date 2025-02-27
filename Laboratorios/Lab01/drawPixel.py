import pygame as pg
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

pg.init()
info = pg.display.Info()

# Definindo altura e largura da janela
height = info.current_h - 100
width = info.current_w - 100
display = (width, height)
screen = pg.display.set_mode(display, DOUBLEBUF | OPENGL)

#text_font = pg.font.SysFont("Arial")

def wc_to_ndc(x, y, x_min, x_max, y_min, y_max):
    ndc_x = (x - x_min) / (x_max - x_min)
    ndc_y = (y - y_min) / (y_max - y_min)
    return ndc_x, ndc_y

def ndc_to_dc(ndc_x, ndc_y, ndh, ndv):  
    dc_x = round(ndc_x * (ndh - 1))
    dc_y = round(ndc_y * (ndv - 1))
    return dc_x, dc_y

def draw_pixel(dc_x, dc_y):
    glPointSize(5) # Aumenta tamanho do pixel
    glBegin(GL_POINTS)
    glColor3f(1.0, 0.0, 0.0)
    glVertex2f(dc_x, dc_y) 
    glEnd()

def main():    
    ndh = info.current_w # Largura do dispositivo
    ndv = info.current_h # Altura do dispositivo
    

    # WC coordenadas
    wc_x_min = 10.5
    wc_x_max = 100.3
    wc_y_min = 15.2
    wc_y_max = 100.4
    wc_x = 20.3
    wc_y = 50.2
    
    # Configurar a matriz de projeção
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0, width, 0, height)  # Mapeia coordenadas ao tamanho da janela
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    ndc_coordinates = wc_to_ndc(wc_x, wc_y, wc_x_min, wc_x_max, wc_y_min, wc_y_max)
    dc_coordinates = ndc_to_dc(ndc_coordinates[0], ndc_coordinates[1], ndh, ndv)

    print(f"Resolução do Dispositivo: {info.current_w} x {info.current_h}")
    print(f"Coordenadas WC: X = {wc_x}, Y = {wc_y}")
    print(f"Coordenadas NDC: X = {ndc_coordinates[0]}, Y = {ndc_coordinates[1]}")
    print(f"Coordenadas DC: X = {dc_coordinates[0]}, Y = {dc_coordinates[1]}")

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        draw_pixel(dc_coordinates[0], dc_coordinates[1])
        pg.display.flip()

if __name__ == "__main__":
    main()
