from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from pyopengltk import OpenGLFrame
import numpy as np

class Cubo_ponto_de_fuga(OpenGLFrame):
    def initgl(self):
        """Inicializa o ambiente OpenGL"""
        glClearColor(0.7, 0.7, 0.7, 0.0)  # Cor de fundo do openGL
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45, self.winfo_reqwidth() / self.winfo_reqheight(), 1, 100.0)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glTranslatef(0.0, 0.0, -10.0)  # Move a câmera para trás para visualizar o cubo
        self.cube_vertices = self.criar_vertices_cubo()

    def criar_vertices_cubo(self):
        """Define os vértices do cubo"""
        return np.array([
            [-1, -1, -1],
            [1, -1, -1],
            [1, 1, -1],
            [-1, 1, -1],
            [-1, -1, 1],
            [1, -1, 1],
            [1, 1, 1],
            [-1, 1, 1]
        ])

    def redraw(self):
        self.draw_scene()

    def draw_scene(self):
        """Redesenha a cena OpenGL para que os objetos etc. fiquem na tela"""
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        self.desenhar_eixos()
        self.desenhar_cubo()
        self.update()

    def desenhar_eixos(self):
        """Desenha os eixos X, Y e Z"""
        eixo_tamanho = 50 # Modifica o tamanho dos eixos
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

    # Desenha o cubo a partir das arestas definidas
    def desenhar_cubo(self):
        vertices = self.cube_vertices
        arestas = [
            [vertices[0], vertices[1]],
            [vertices[1], vertices[2]],
            [vertices[2], vertices[3]],
            [vertices[3], vertices[0]],
            [vertices[4], vertices[5]],
            [vertices[5], vertices[6]],
            [vertices[6], vertices[7]],
            [vertices[7], vertices[4]],
            [vertices[0], vertices[4]],
            [vertices[1], vertices[5]],
            [vertices[2], vertices[6]],
            [vertices[3], vertices[7]]
        ]

        glBegin(GL_LINES)
        glColor3f(0, 0, 0)
        for aresta in arestas:
            for vertice in aresta:
                glVertex3fv(vertice)
        glEnd()

    def perspectiva(self, fov, aspect, near, far):
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(fov, aspect, near, far)
        glMatrixMode(GL_MODELVIEW)

def desenhar(tab2):
    ogl_frame = Cubo_ponto_de_fuga(tab2, width=800, height=600)
    ogl_frame.pack(fill="both", expand=True)