from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import numpy as np

class Translacao:
    @staticmethod
    def get_translation_matrix3D(tx, ty, tz):
        # Matriz de translação 4x4 em coordenadas homogêneas
        matrix = np.array([
            [1, 0, 0, tx],
            [0, 1, 0, ty],
            [0, 0, 1, tz],
            [0, 0, 0, 1]
        ], dtype=float)
        return matrix

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


def realizar_translacao(square_points_list, tx, ty):
        
    point1, point2, point3, point4 = square_points_list

    # Transladar os pontos
    point1 = translate_point(point1, tx, ty, 1)
    point2 = translate_point(point2, tx, ty, 1)
    point3 = translate_point(point3, tx, ty, 1)
    point4 = translate_point(point4, tx, ty, 1)

    # retornar os vertices do quadrado após a translação
    return [point1, point2, point3, point4]

def translate_point3D(point, tx, ty, tz):
    # Construção da matriz de transformação de translação
    translation_matrix = np.array([[1, 0, 0, tx],
                                   [0, 1, 0, ty],
                                   [0, 0, 1, tz],
                                   [0, 0, 0, 1]])

    # Convertendo o ponto para um vetor coluna
    point_vector = np.array([[point[0]], [point[1]], [point[2]], [point[3]]])  # point[3] = 1 = W

    # Aplicando a transformação de translação multiplicando a matriz de translação pelo vetor do ponto
    translated_point_vector = np.dot(translation_matrix, point_vector)
    
    return (translated_point_vector[0][0], translated_point_vector[1][0], translated_point_vector[2][0], translated_point_vector[3][0]) 


def realizar_translacao3D(cube_points_list, tx, ty, tz):
    # Realiza a transformação um ponto por vez e retorna a lista de pontos transformada
    for i in range(len(cube_points_list)):
        cube_points_list[i] = translate_point3D(cube_points_list[i], tx, ty, tz)

    return cube_points_list

def get_translate_Matrix3D(tx, ty, tz):
    return np.array([[1, 0, 0, tx],
                     [0, 1, 0, ty],
                     [0, 0, 1, tz],
                     [0, 0, 0, 1]])

def get_translate_Matrix2D(tx, ty):
    return np.array([[1, 0, tx],
                     [0, 1, ty],
                     [0, 0, 1]])

