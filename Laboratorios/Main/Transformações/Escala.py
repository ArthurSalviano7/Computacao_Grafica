from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import numpy as np

def ponto_escala(ponto, sx, sy, w):
    # Criação da matriz de identidade de escala 2D
    matriz_escalonamento = np.array([[sx, 0, 0],
                             [0, sy, 0],
                             [0, 0, 1]])

    # Convertendo o ponto para um vetor coluna
    pixel_vetor = np.array([[ponto[0]], [ponto[1]],[w]])

    # Aplicando a transformação de escala multiplicando a matriz de escala pelo vetor do ponto
    pixel_vetor_esc = np.dot(matriz_escalonamento, pixel_vetor)
    
    return (pixel_vetor_esc[0][0], pixel_vetor_esc[1][0])

def realizar_escala(square_points_list, sx, sy):
    
    ponto1, ponto2, ponto3, ponto4 = square_points_list

    ponto1 = ponto_escala(ponto1, sx, sy, 1)
    ponto2 = ponto_escala(ponto2, sx, sy, 1)
    ponto3 = ponto_escala(ponto3, sx, sy, 1)
    ponto4 = ponto_escala(ponto4, sx, sy, 1)

    return [ponto1, ponto2, ponto3, ponto4]


