import numpy as np
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

def cis_point(point, a, b, w):

    matrizCis = np.array([[1, a, 0],
                          [b, 1, 0],
                          [0, 0, 1]])
    
    # Convertendo o ponto para um vetor coluna
    pixel_vetor = np.array([[point[0]], [point[1]], [w]])  # w = 1 para pontos

    # Aplicando a transformação de rotação multiplicando a matriz de cisalhamento pelo vetor do ponto
    vetor_pixel_cis = np.dot(matrizCis, pixel_vetor)

    # Normalizando as coordenadas homogêneas resultantes
    shear_point = (vetor_pixel_cis[0][0] / vetor_pixel_cis[2][0], 
                        vetor_pixel_cis[1][0] / vetor_pixel_cis[2][0])
    
    return shear_point


def realizar_cisalhamento(square_points_list, a, b):

    ponto1, ponto2, ponto3, ponto4 = square_points_list

    # Cisalhar os pontos
    ponto1 = cis_point(ponto1, a, b, 1)
    ponto2 = cis_point(ponto2, a, b, 1)
    ponto3 = cis_point(ponto3, a, b, 1)
    ponto4 = cis_point(ponto4, a, b, 1)

    # retornar os vertices do quadrado após o cisalhamento
    return [ponto1, ponto2, ponto3, ponto4]

def cis_point3D(point, a, b, cisType):

    matrizCis = []
    
    if cisType == "CisXY":
        matrizCis = np.array([[1, 0, a, 0],
                              [0, 1, b, 0],
                              [0, 0, 1, 0],
                              [0, 0, 0, 1]])
    elif cisType == "CisYZ":
        matrizCis = np.array([[1, 0, 0, 0],
                              [a, 1, 0, 0],
                              [b, 0, 1, 0],
                              [0, 0, 0, 1]])
    elif cisType == "CisXZ":
        matrizCis = np.array([[1, a, 0, 0],
                              [0, 1, 0, 0],
                              [0, b, 1, 0],
                              [0, 0, 0, 1]])
    
    # Convertendo o ponto para um vetor coluna
    point_vector = np.array([[point[0]], [point[1]], [point[2]], [point[3]]])

    # Aplicando a transformação de rotação multiplicando a matriz de cisalhamento pelo vetor do ponto
    vetor_point_cis = np.dot(matrizCis, point_vector)
    
    return [vetor_point_cis[0][0], vetor_point_cis[1][0], vetor_point_cis[2][0], vetor_point_cis[3][0]] 

def realizar_cisalhamento3D(cube_points_list, a, b, cisType):

    # Realiza a transformação um ponto por vez e retorna a lista de pontos transformada
    for i in range(len(cube_points_list)):
        cube_points_list[i] = cis_point3D(cube_points_list[i], a, b, cisType)

    return cube_points_list

def get_CisXY_Matrix3D(a, b):
    return np.array([[1, 0, a, 0],
                     [0, 1, b, 0],
                     [0, 0, 1, 0],
                     [0, 0, 0, 1]])

def get_CisYZ_Matrix3D(a, b):
    return np.array([[1, 0, 0, 0],
                     [a, 1, 0, 0],
                     [b, 0, 1, 0],
                     [0, 0, 0, 1]])

def get_CisXZ_Matrix3D(a, b):
    return np.array([[1, a, 0, 0],
                     [0, 1, 0, 0],
                     [0, b, 1, 0],
                     [0, 0, 0, 1]])

def get_Cis_Matrix2D(a, b):
    return np.array([[1, a, 0],
                     [b, 1, 0],
                     [0, 0, 1]])