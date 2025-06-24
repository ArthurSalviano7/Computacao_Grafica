import numpy as np
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

def refX_point(point, w):

    matrizRef = np.array([[1, 0, 0],
                          [0, -1, 0],
                          [0, 0, 1]])
    
    # Convertendo o ponto para um vetor coluna
    point_vector = np.array([[point[0]], [point[1]], [w]])  # w = 1 para pontos

    # Aplicando a transformação de reflexão em X multiplicando a matriz de reflexão pelo vetor do ponto
    reflection_point_vector = np.dot(matrizRef, point_vector)
    
    return [reflection_point_vector[0][0], reflection_point_vector[1][0]] 

def refY_point(point, w):

    matrizRef = np.array([[-1, 0, 0],
                          [0, 1, 0],
                          [0, 0, 1]])

    # Convertendo o ponto para um vetor coluna
    point_vector = np.array([[point[0]], [point[1]], [w]])  # w = 1 para pontos

    # Aplicando a transformação de reflexão em Y multiplicando a matriz de reflexão pelo vetor do ponto
    reflection_point_vector = np.dot(matrizRef, point_vector)
    
    return [reflection_point_vector[0][0], reflection_point_vector[1][0]] 

def refOrigin_point(point, w):

    matrizRef = np.array([[-1, 0, 0],
                          [0, -1, 0],
                          [0, 0, 1]])
    
    # Convertendo o ponto para um vetor coluna
    point_vector = np.array([[point[0]], [point[1]], [w]])  # w = 1 para pontos

    # Aplicando a transformação de reflexão na origem multiplicando a matriz de reflexão pelo vetor do ponto
    reflection_point_vector = np.dot(matrizRef, point_vector)
    
    return [reflection_point_vector[0][0], reflection_point_vector[1][0]] 

def ref45_point(point, w):

    matrizRef = np.array([[0, 1, 0],
                          [1, 0, 0],
                          [0, 0, 1]])
    
    # Convertendo o ponto para um vetor coluna
    point_vector = np.array([[point[0]], [point[1]], [w]])  # w = 1 para pontos

    # Aplicando a transformação de reflexão pela reta de 45 graus multiplicando a matriz de reflexão pelo vetor do ponto
    reflection_point_vector = np.dot(matrizRef, point_vector)

    return [reflection_point_vector[0][0], reflection_point_vector[1][0]] 

def realizar_reflexaoX(square_points_list):

    point1, point2, point3, point4 = square_points_list

    # Refletir os pontos
    point1 = refX_point(point1, 1)
    point2 = refX_point(point2, 1)
    point3 = refX_point(point3, 1)
    point4 = refX_point(point4, 1)

    # retornar os vertices do quadrado após a reflexão
    return [point1, point2, point3, point4]

def realizar_reflexaoY(square_points_list):

    point1, point2, point3, point4 = square_points_list

    # Refletir os pontos
    point1 = refY_point(point1, 1)
    point2 = refY_point(point2, 1)
    point3 = refY_point(point3, 1)
    point4 = refY_point(point4, 1)

    # retornar os vertices do quadrado após a reflexão
    return [point1, point2, point3, point4]

def realizar_reflexaoOrigem(square_points_list):

    point1, point2, point3, point4 = square_points_list

    # Refletir os pontos
    point1 = refOrigin_point(point1, 1)
    point2 = refOrigin_point(point2, 1)
    point3 = refOrigin_point(point3, 1)
    point4 = refOrigin_point(point4, 1)

    # retornar os vertices do quadrado após a reflexão
    return [point1, point2, point3, point4]

def realizar_reflexao45(square_points_list):

    point1, point2, point3, point4 = square_points_list

    # Refletir os pontos
    point1 = ref45_point(point1, 1)
    point2 = ref45_point(point2, 1)
    point3 = ref45_point(point3, 1)
    point4 = ref45_point(point4, 1)

    # retornar os vertices do quadrado após a reflexão
    return [point1, point2, point3, point4]

# --- REFLEXÃO 3D ---
def ref_point(point, refType):
    '''Reflexão no plano XY'''
    matrizRef = []
    
    if refType == "RefXY":
        matrizRef = np.array([[1, 0, 0, 0],
                              [0, 1, 0, 0],
                              [0, 0, -1, 0],
                              [0, 0, 0, 1]])
    elif refType == "RefYZ":
        matrizRef = np.array([[-1, 0, 0, 0],
                              [0, 1, 0, 0],
                              [0, 0, 1, 0],
                              [0, 0, 0, 1]])
    elif refType == "RefXZ":
        matrizRef = np.array([[1, 0, 0, 0],
                              [0, -1, 0, 0],
                              [0, 0, 1, 0],
                              [0, 0, 0, 1]])
    elif refType == "RefOrig":
        matrizRef = np.array([[-1, 0, 0, 0],
                              [0, -1, 0, 0],
                              [0, 0, -1, 0],
                              [0, 0, 0, 1]])
    
    
    # Convertendo o ponto para um vetor coluna
    point_vector = np.array([[point[0]], [point[1]], [point[2]], [point[3]]])

    # Aplicando a transformação de reflexão em X multiplicando a matriz de reflexão pelo vetor do ponto
    reflection_point_vector = np.dot(matrizRef, point_vector)
    
    return [reflection_point_vector[0][0], reflection_point_vector[1][0], reflection_point_vector[2][0], reflection_point_vector[3][0]] 

def realizar_reflexao3D(cube_points_list, ref_type):
    # Colocar todas as reflexoes em um só
    # Realiza a transformação um ponto por vez e retorna a lista de pontos transformada
    for i in range(len(cube_points_list)):
        cube_points_list[i] = ref_point(cube_points_list[i], ref_type)

    return cube_points_list

def get_RefXY_Matrix3D():      
      return np.array([[1, 0, 0, 0],
                       [0, 1, 0, 0],
                       [0, 0, -1, 0],
                       [0, 0, 0, 1]])

def get_RefYZ_Matrix3D():      
      return np.array([[-1, 0, 0, 0],
                       [0, 1, 0, 0],
                       [0, 0, 1, 0],
                       [0, 0, 0, 1]])

def get_RefXZ_Matrix3D():      
      return np.array([[1, 0, 0, 0],
                       [0, -1, 0, 0],
                       [0, 0, 1, 0],
                       [0, 0, 0, 1]])

def get_RefOrig_Matrix3D():      
      return np.array([[-1, 0, 0, 0],
                       [0, -1, 0, 0],
                       [0, 0, -1, 0],
                       [0, 0, 0, 1]])

def get_RefX_Matrix2D():
    return np.array([[1, 0, 0],
                     [0, -1, 0],
                     [0,  0, 1]])

def get_RefY_Matrix2D():
    return np.array([[-1,  0, 0],
                     [0, 1, 0],
                     [0,  0, 1]])

def get_RefOrig_Matrix2D():
    return np.array([[-1, 0, 0],
                     [0, -1, 0],
                     [0,  0, 1]])

def get_Ref45_Matrix2D():
    return np.array([[0, 1, 0],
                     [1, 0, 0],
                     [0, 0, 1]])