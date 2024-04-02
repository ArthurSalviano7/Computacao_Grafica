'''
    Classe que renderiza o OpenGl na tela
'''

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import numpy as np
from pyopengltk import OpenGLFrame

from Transformações import Escala



class AppOgl(OpenGLFrame):
    def initgl(self):
        """Inicializa o ambiente OpenGL"""
        glClearColor(0.7, 0.7, 0.7, 0.0) #Cor de fundo do openGL
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluOrtho2D(-self.winfo_reqwidth()/2, self.winfo_reqwidth()/2, -self.winfo_reqheight()/2, self.winfo_reqheight()/2)
        print("width x height: ", self.winfo_reqwidth(), "x", self.winfo_reqheight())
        self.points = []  # Lista de pontos para armazenar o desenho
        self.square_points_list = [] # Lista de pontos para armazenar os vértices do quadrado

    def redraw(self):
        self.draw_scene()

    def draw_scene(self):
        """Redesenha a cena OpenGL para que os objetos etc. fiquem na tela"""
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        self.draw_axes(self.winfo_reqwidth(), self.winfo_reqheight()) #Desenhar eixos X e Y

        # Desenha os pontos armazenados na lista
        glBegin(GL_POINTS)
        glColor3f(1.0, 0, 0)
        for point in self.points:
            glVertex2f(point[0], point[1])
        glEnd()

        self.update()

    def draw_axes(self, width, height): #Desenhar eixos X e Y 
        glBegin(GL_LINES)
        glColor3f(0.30, 0.30, 0.30)  # Cor para o eixo x
        glVertex3f(-width/2, 0.0, 0.0)
        glVertex3f(width/2, 0.0, 0.0)
        glColor3f(0.30, 0.30, 0.30)  # Cor para o eixo y
        glVertex3f(0.0, -height/2, 0.0)
        glVertex3f(0.0, height/2, 0.0)
        glEnd()

    def draw_pixel(self, dc_x, dc_y):
        glBegin(GL_POINTS)
        glColor3f(1.0, 1.0, 1.0)
        glVertex2f(dc_x, dc_y) 
        glEnd()

    def DDA(self, x0, y0, xEnd, yEnd):
        dx = xEnd - x0
        dy = yEnd - y0
        steps = max(abs(dx), abs(dy))
        xIncrement = dx / steps
        yIncrement = dy / steps
        x = x0
        y = y0
        self.draw_pixel(round(x), round(y))
        for k in range(int(steps)):
            x += xIncrement
            y += yIncrement
            self.points.append((round(x), round(y)))
            #self.draw_pixel(round(x), round(y))
    

    #Método para desenhar quadrado na origem
    def square_points(self, size):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT) # Quando desenhar novo quadrado, limpa a tela antes
        self.points = []
        self.square_points_list = []

        x = round(size)/2
        y = round(size)/2
        self.DDA(-x, y, x, y)
        self.DDA(x, y, x, -y)
        self.DDA(x, -y, -x, -y)
        self.DDA(-x, -y, -x, y)

        self.square_points_list = [(-x,y), (x,y), (x,-y), (-x,-y)]

        return (-x,y),(x,y),(x,-y),(-x,-y)
    
    #Método para desenhar quadrado após a transformação
    def draw_square(self, point1, point2, point3, point4):
        self.DDA(point1[0], point1[1], point2[0], point2[1])
        self.DDA(point2[0], point2[1], point3[0], point3[1])
        self.DDA(point3[0], point3[1], point4[0], point4[1])
        self.DDA(point4[0], point4[1], point1[0], point1[1])


    #Transformações no Quadrado
    def escala(self, scale_factor):
        #Passa os pontos do quadrado desenhado para a função de escala que retorna os novos pontos do quadrado
        self.square_points_list = Escala.realizar_escala(self.square_points_list, scale_factor)

        #Remove o quadrado anterior
        self.points = [] 

        #Desenha o novo quadrado
        self.draw_square(*self.square_points_list) #passa os parametros da função ao desempacotar a lista


        
        
        
    


