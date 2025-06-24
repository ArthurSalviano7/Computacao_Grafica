import numpy as np
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

    
def rotate_point(point, ang, w):

    rad = np.radians(ang)

    matrizTheta = np.array([[np.cos(rad), - np.sin(rad), 0],
                            [np.sin(rad), np.cos(rad), 0],
                            [0, 0, 1]])
    
    # Convertendo o ponto para um vetor coluna
    point_vector = np.array([[point[0]], [point[1]], [w]])  # w = 1 para pontos

    # Aplicando a transformação de rotação multiplicando a matriz de translação pelo vetor do ponto
    rotated_point_vector = np.dot(matrizTheta, point_vector)

    # Normalizando as coordenadas homogêneas resultantes
    rotated_point = (rotated_point_vector[0][0] / rotated_point_vector[2][0], 
                        rotated_point_vector[1][0] / rotated_point_vector[2][0])
    
    return rotated_point


def realizar_rotacao(square_points_list, angle):

    point1, point2, point3, point4 = square_points_list

    # Rotacionar os pontos
    point1 = rotate_point(point1, angle, 1)
    point2 = rotate_point(point2, angle, 1)
    point3 = rotate_point(point3, angle, 1)
    point4 = rotate_point(point4, angle, 1)

    # retornar os vertices do quadrado após a rotação
    return [point1, point2, point3, point4]

def rotate_point3D(point, ang, rotate_type):

    rad = np.radians(ang)
    matrizTheta = []

    if rotate_type == "Rx":
            matrizTheta = np.array([[1, 0, 0, 0],
                                    [0, np.cos(rad), - np.sin(rad), 0],
                                    [0, np.sin(rad), np.cos(rad), 0],
                                    [0, 0, 0, 1]])
    elif rotate_type == "Ry":
            matrizTheta = np.array([[np.cos(rad), 0, np.sin(rad), 0],
                                    [0, 1, 0, 0],
                                    [- np.sin(rad), 0, np.cos(rad), 0],
                                    [0, 0, 0, 1]])
    elif rotate_type == "Rz":
            matrizTheta = np.array([[np.cos(rad), - np.sin(rad), 0, 0],
                                    [np.sin(rad), np.cos(rad), 0, 0],
                                    [0, 0, 1, 0],
                                    [0, 0, 0, 1]])
    
    # Convertendo o ponto para um vetor coluna
    point_vector = np.array([[point[0]], [point[1]], [point[2]], [point[3]]])  # point[3] = w = 1

    # Aplicando a transformação de rotação multiplicando a matriz de translação pelo vetor do ponto
    rotated_point_vector = np.dot(matrizTheta, point_vector)
    
    return [rotated_point_vector[0][0], rotated_point_vector[1][0], rotated_point_vector[2][0], rotated_point_vector[3][0]]

def realizar_rotacao3D(cube_points_list, angle, rotate_type):
    # Realiza a transformação um ponto por vez e retorna a lista de pontos transformada
    for i in range(len(cube_points_list)):
        cube_points_list[i] = rotate_point3D(cube_points_list[i], angle, rotate_type)

    return cube_points_list

def get_Rotate_Matrix2D(angle):
      rad = np.radians(angle)
      
      return np.array([[np.cos(rad), -np.sin(rad), 0,],
                        [np.sin(rad), np.cos(rad), 0],
                        [0,         0,          1]])

def get_RotateX_Matrix3D(angle):
      rad = np.radians(angle)
      
      return np.array([[1, 0, 0, 0],
                        [0, np.cos(rad), - np.sin(rad), 0],
                        [0, np.sin(rad), np.cos(rad), 0],
                        [0, 0, 0, 1]])

def get_RotateY_Matrix3D(angle):
      rad = np.radians(angle)
      
      return np.array([[np.cos(rad), 0, np.sin(rad), 0],
                        [0, 1, 0, 0],
                        [- np.sin(rad), 0, np.cos(rad), 0],
                        [0, 0, 0, 1]])

def get_RotateZ_Matrix3D(angle):
      rad = np.radians(angle)
      
      return np.array([[np.cos(rad), - np.sin(rad), 0, 0],
                        [np.sin(rad), np.cos(rad), 0, 0],
                        [0, 0, 1, 0],
                        [0, 0, 0, 1]])


