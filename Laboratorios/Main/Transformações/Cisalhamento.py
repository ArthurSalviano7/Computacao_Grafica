import numpy as np
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

def ponto_cis(pixel, a, b, w):

    matrizCis = np.array([[1, a, 0],
                          [b, 1, 0],
                          [0, 0, 1]])
    
    # Convertendo o ponto para um vetor coluna
    pixel_vetor = np.array([[pixel[0]], [pixel[1]], [w]])  # w = 1 para pontos

    # Aplicando a transformação de rotação multiplicando a matriz de cisalhamento pelo vetor do ponto
    vetor_pixel_cis = np.dot(matrizCis, pixel_vetor)

    # Normalizando as coordenadas homogêneas resultantes
    shear_point = (vetor_pixel_cis[0][0] / vetor_pixel_cis[2][0], 
                        vetor_pixel_cis[1][0] / vetor_pixel_cis[2][0])
    
    return shear_point


def realizar_cisalhamento(square_points_list, a, b):

    ponto1, ponto2, ponto3, ponto4 = square_points_list

    # Cisalhar os pontos
    ponto1 = ponto_cis(ponto1, a, b, 1)
    ponto2 = ponto_cis(ponto2, a, b, 1)
    ponto3 = ponto_cis(ponto3, a, b, 1)
    ponto4 = ponto_cis(ponto4, a, b, 1)

    # retornar os vertices do quadrado após o cisalhamento
    return [ponto1, ponto2, ponto3, ponto4]