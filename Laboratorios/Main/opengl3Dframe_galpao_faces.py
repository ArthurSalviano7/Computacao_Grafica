from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from pyopengltk import OpenGLFrame
import numpy as np

'''Desenho do galpão e câmera configurada para ver todas as faces ao mesmo tempo'''
class Galpao_projecao_multiplas_faces(OpenGLFrame):
    def initgl(self):
        """Inicializa o ambiente OpenGL"""
        glClearColor(0.7, 0.7, 0.7, 0.0)  # Cor de fundo do openGL
        glEnable(GL_DEPTH_TEST)  # Habilita teste de profundidade
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        self.setup_view()
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        self.cube_vertices = self.criar_vertices_casa()

    def setup_view(self):
        """Configura a câmera para visualizar a cena em projeção paralela ortográfica"""
        glOrtho(-2, 2, -2, 2, -2, 2)  # Define a projeção ortográfica sem rotações adicionais
        glRotatef(30, 1, 0, 0)  # Rotaciona a visualização para melhor visualização das faces
        glRotatef(45, 0, -1, 0)  # Rotaciona a visualização para melhor visualização das faces
    
    def criar_vertices_casa(self):
        """Define os vértices do galpão a ser desenhado"""
        return np.array([
            [0, 0, 0],
            [1, 0, 0],
            [1, 1, 0],
            [0.5, 1.5, 0],
            [0, 1, 0],
            [0, 0, 1],
            [1, 0, 1],
            [1, 1, 1],
            [0.5, 1.5, 1],
            [0, 1, 1]
        ])

    def redraw(self):
        self.draw_scene()

    def draw_scene(self):
        """Redesenha a cena OpenGL para que os objetos etc. fiquem na tela"""
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        self.desenhar_casa()
        self.desenhar_eixos()
        self.update()

    def desenhar_eixos(self):
        """Desenha os eixos X, Y e Z"""
        eixo_tamanho = 50  # Modifica o tamanho dos eixos
        glBegin(GL_LINES)
        glColor3f(1, 0, 0)  # Eixo X em vermelho
        glVertex3f(-eixo_tamanho, 0, 0)
        glVertex3f(eixo_tamanho, 0, 0)
        glColor3f(0, 1, 0)  # Eixo Y em verde
        glVertex3f(0, -eixo_tamanho, 0)
        glVertex3f(0, eixo_tamanho, 0)
        glColor3f(0, 0, 1)  # Eixo Z em azul
        glVertex3f(0, 0, -eixo_tamanho)
        glVertex3f(0, 0, eixo_tamanho)
        glEnd()

    def desenhar_casa(self):
        """Desenha a casa a partir das arestas definidas"""
        vertices = self.cube_vertices
        arestas = [
            #Face 0 (left):
            [vertices[0], vertices[5]],
            [vertices[5], vertices[9]],
            [vertices[9], vertices[4]],
            [vertices[4], vertices[0]],
            #Face 1 (roof left):
            [vertices[3], vertices[4]],
            [vertices[4], vertices[9]],
            [vertices[9], vertices[8]],
            [vertices[8], vertices[3]],
            #Face 2 (roof right):
            [vertices[2], vertices[3]],
            [vertices[3], vertices[8]],
            [vertices[8], vertices[7]],
            [vertices[7], vertices[2]],
            #Face 6 (back):
            [vertices[0], vertices[4]],
            [vertices[4], vertices[3]],
            [vertices[3], vertices[2]],
            [vertices[2], vertices[1]],
            [vertices[1], vertices[0]],
            #Face 3 (right):
            [vertices[1], vertices[2]],
            [vertices[2], vertices[7]],
            [vertices[7], vertices[6]],
            [vertices[6], vertices[1]],
            #Face 4 (bottom):
            [vertices[0], vertices[1]],
            [vertices[1], vertices[6]],
            [vertices[6], vertices[5]],
            [vertices[5], vertices[0]],
            #Face 5 (front):
            [vertices[5], vertices[6]],
            [vertices[6], vertices[7]],
            [vertices[7], vertices[8]],
            [vertices[8], vertices[9]],
            [vertices[9], vertices[5]]
        ]

        glBegin(GL_LINES)
        glColor3f(0, 0, 0)
        for aresta in arestas:
            for vertice in aresta:
                glVertex3fv(vertice)
        glEnd()

def desenhar(tab4):
    ogl_frame = Galpao_projecao_multiplas_faces(tab4, width=800, height=600)
    ogl_frame.pack(fill="both", expand=True)

