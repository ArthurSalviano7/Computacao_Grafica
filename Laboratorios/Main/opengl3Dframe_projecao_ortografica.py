from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from pyopengltk import OpenGLFrame
import numpy as np
import tkinter as tk

'''Desenho do galpão e câmera configurada para ver todas as faces ao mesmo tempo'''
class Galpao_projecao_ortografica(OpenGLFrame):
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
        self.rot_angle = 0  # Ângulo de rotação para mudar a visualização entre as faces

    def setup_view(self):
        """Configura a câmera para visualizar a cena em projeção paralela ortográfica"""
        glOrtho(-2, 2, -2, 2, -2, 2)  # Define a projeção ortográfica sem rotações adicionais
       
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
        glLoadIdentity()
        glRotatef(self.rot_angle, 0, 1, 0)  # Aplica a rotação em torno do eixo Y
        self.desenhar_casa()
        self.desenhar_eixos()
        self.update()

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
    
    def mudar_face(self):
        """Função para rotacionar o objeto e visualizar suas faces"""
        print(self.rot_angle)
        self.rot_angle += 90  # Rotaciona 90 graus em torno do eixo Y
        self.rot_angle %= 360  # Mantém o ângulo entre 0 e 360
        self.redraw()
        self.update()

    def mudar_camera(self):
        """Callback para mudar a câmera"""
        self.camera_angle += 10.0  # Aumenta o ângulo da câmera
        self.redraw()
        self.update()


def desenhar(tab5):
    frame_left = tk.Frame(tab5, width=200, height=600)
    frame_left.configure(background="#000C66")
    frame_left.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # Frame para o lado direito
    frame_right = tk.Frame(tab5, width=800, height=600)
    frame_right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=False)

    ogl_frame_paralela = Galpao_projecao_ortografica(frame_right, width=800, height=600)
    ogl_frame_paralela.pack(fill="both", expand=True)

    # Botão para Reflexão na Origem
    btn_faces = tk.Button(frame_left, text="Mudar Face", command=lambda: ogl_frame_paralela.mudar_face())
    btn_faces.pack(fill='x', expand=False, pady=10)

