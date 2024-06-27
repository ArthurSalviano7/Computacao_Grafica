import math
import numpy as np
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

def reflect_point(point, m, b, w):
    
    denominador = math.sqrt(m * m + 1)
    senTheta = m / denominador
    cosTheta = 1 / denominador

    M_Translacao1 = np.array([[1, 0, 0],
                            [0, 1, b],
                            [0, 0, 1]])
    
    M_Rotacao1 = np.array([[cosTheta, -senTheta, 0],
                          [senTheta, cosTheta, 0],
                          [0, 0, 1]])
    
    M_ReflexaoX = np.array([[1, 0, 0],
                            [0, -1, 0],
                            [0, 0, 1]])
    
    M_Rotacao2 = np.array([[cosTheta, senTheta, 0],
                          [-senTheta, cosTheta, 0],
                          [0, 0, 1]])
    
    M_Translacao2 = np.array([[1, 0, 0],
                            [0, 1, -b],
                            [0, 0, 1]])
    
    matrizRefAny = np.dot(M_Translacao1, M_Rotacao1)
    matrizRefAny = np.dot(matrizRefAny, M_ReflexaoX)
    matrizRefAny = np.dot(matrizRefAny, M_Rotacao2)
    matrizRefAny = np.dot(matrizRefAny, M_Translacao2)

    # Convertendo o ponto para um vetor coluna
    point_vector = np.array([[point[0]], [point[1]], [w]])  # w = 1 para pontos

    # Aplicando a transformação de reflexão em uma reta qualquer multiplicando a matriz de reflexão pelo vetor do ponto
    reflect_point_vector = np.dot(matrizRefAny, point_vector)

    # Normalizando as coordenadas homogêneas resultantes
    reflect_point = (reflect_point_vector[0][0] / reflect_point_vector[2][0], 
                        reflect_point_vector[1][0] / reflect_point_vector[2][0])
    
    return reflect_point


def realizar_reflexao_qualquer(square_points_list, m, b):

    point1, point2, point3, point4 = square_points_list

    # Refletir os pontos
    point1 = reflect_point(point1, m, b, 1)
    point2 = reflect_point(point2, m, b, 1)
    point3 = reflect_point(point3, m, b, 1)
    point4 = reflect_point(point4, m, b, 1)

    # retornar os vertices do quadrado após a reflexão
    return [point1, point2, point3, point4]