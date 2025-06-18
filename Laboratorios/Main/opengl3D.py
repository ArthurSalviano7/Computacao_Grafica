from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from pyopengltk import OpenGLFrame
import numpy as np
import tkinter as tk
import customtkinter as ctk

from Transformações import Rotacao
from Transformações import Translacao
from Transformações import Escala
from Transformações import Cisalhamento
from Transformações import Reflexao
from Transformações import ReflexaoQualquer

'''Desenho do galpão e câmera configurada para ver todas as faces ao mesmo tempo'''
class opengl3D(OpenGLFrame):
    def __init__(self, master=None, **kw):
        ''' Inicializa os vertices do cubo para evitar erros ao atualizar cena '''
        super().__init__(master, **kw)
        
        self.cube_vertices = self.criar_vertices_cubo(50) # Lista de pontos para armazenar os vértices do cubo
        self.rotation_angle_y = 0.0  # Variável para o ângulo de rotação Y (câmera)

    def initgl(self):
        """Inicializa o ambiente OpenGL"""
        glClearColor(0.7, 0.7, 0.7, 0.0)  # Cor de fundo do openGL
        glEnable(GL_DEPTH_TEST)  # Habilita teste de profundidade
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        self.vp_width = self.winfo_reqwidth()
        self.vp_height = self.winfo_reqheight()
        self.vp_Zaxis = 800 # Valor default para eixo Z
        print("width x height: ", self.vp_width, "x", self.vp_height)

        self.points = []  # Lista de pontos para armazenar o desenho
        self.redraw()
    
    # Define a janela em coordenadas do mundo de acordo com a entrada do usuário
    def definir_janela_mundo(self, new_vp_width, new_vp_height, new_vp_Zaxis):
        self.vp_width = new_vp_width
        self.vp_height = new_vp_height
        self.vp_Zaxis =  new_vp_Zaxis
        self.redraw()
        
    def draw_pixel(self, dc_x, dc_y, dc_z):
        glBegin(GL_POINTS)
        glColor3f(0, 0, 0)
        glVertex3f(dc_x, dc_y, dc_z) 
        glEnd()    

    def criar_cubo(self, size): #Funcão para criar cubo e atualizar cena
        self.cube_vertices = self.criar_vertices_cubo(size)
        self.redraw()
    
    def criar_vertices_cubo(self, size):
        print("Tamanho: ", size)
        return np.array([
            [0, 0, 0, 1], # Adicionado 1 para coordenadas homogêneas (w)
            [size, 0, 0, 1],
            [size, size, 0, 1],
            [0, size, 0, 1],
            [0, 0, size, 1],
            [size, 0, size, 1],
            [size, size, size, 1],
            [0, size, size, 1]
        ], dtype=float) # Garanta que os vértices são floats para multiplicação

    def redraw(self):
        self.draw_scene()

    def draw_scene(self):
        """
        Redesenha a cena OpenGL, configurando completamente o ambiente 
        de visualização para o 3D a CADA FRAME.
        """

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT) # Limpa os buffers
        # --- Configuração da PROJEÇÃO ---
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        
        # Definindo view port
        glOrtho(-self.vp_width/2, self.vp_width/2, -self.vp_height/2, self.vp_height/2, -self.vp_Zaxis/2, self.vp_Zaxis/2) 
        
        # --- Configuração da CÂMERA (MODELVIEW) ---
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity() # Resetar a matriz MODELVIEW para cada frame

        # Aplicar as rotações ISOMÉTRICAS FIXAS (se aplicável a este frame 3D)
        glRotatef(35.36, 1, 0, 0)
        glRotatef(45, 0, -1, 0) 

        # Aplicar a rotação dinâmica da CÂMERA (botão 30º)
        glRotatef(self.rotation_angle_y, 0, 1, 0) 
        
        print("Cubo: ", self.cube_vertices)
        # Desenhar os objetos da cena
        self.desenhar_eixos(self.vp_width, self.vp_height, self.vp_Zaxis)
        self.desenhar_cubo()

       
        
        # Força a troca de buffers e atualização na tela
        self.tkSwapBuffers() 


    def desenhar_eixos(self, sizeX, sizeY, sizeZ):
        """Desenha os eixos X, Y e Z"""
        glBegin(GL_LINES)
        glColor3f(1, 0, 0)  # Eixo X em vermelho
        glVertex3f(-sizeX, 0, 0)
        glVertex3f(sizeX, 0, 0)
        glColor3f(0, 1, 0)  # Eixo Y em verde
        glVertex3f(0, -sizeY, 0)
        glVertex3f(0, sizeY, 0)
        glColor3f(0, 0, 1)  # Eixo Z em azul
        glVertex3f(0, 0, -sizeZ)
        glVertex3f(0, 0, sizeZ)
        glEnd()

    def desenhar_cubo(self):
        """Desenha o cubo a partir das arestas definidas"""
        vertices = self.cube_vertices
        arestas = [
            (0, 1), (1, 2), (2, 3), (3, 0), 
            (4, 5), (5, 6), (6, 7), (7, 4), 
            (0, 4), (1, 5), (2, 6), (3, 7)
        ]

        glBegin(GL_LINES)
        glColor3f(0, 0, 0)
        for i, j in arestas:
            # Pega X, Y, Z de cada vértice, IGNORANDO a 4ª coordenada (w)
            v1_xyz = vertices[i][:3]
            v2_xyz = vertices[j][:3]
                
            glVertex3fv(v1_xyz) # Passa apenas o vetor (x,y,z) de 3 componentes
            glVertex3fv(v2_xyz)
        glEnd()
    

    def desenhar_cubo_DDA(self):
        vertices = self.cube_vertices
        arestas_indices = [
            (0, 1), (1, 2), (2, 3), (3, 0), # Face frontal
            (4, 5), (5, 6), (6, 7), (7, 4), # Face traseira
            (0, 4), (1, 5), (2, 6), (3, 7)  # Conectores
        ]

        # Use GL_POINTS para desenhar cada ponto gerado pelo DDA
        glBegin(GL_POINTS)
        glColor3f(0, 0, 0) # Cor preta para as arestas

        for i, j in arestas_indices:
            p1 = vertices[i]
            p2 = vertices[j]
            
            # Gerar pontos da linha usando DDA 3D
            line_points = self.DDA3D(p1, p2)
            
            # Desenhar cada ponto da linha
            for point in line_points:
                glVertex3f(point[0], point[1], point[2])
        glEnd()
    
    def DDA3D(self, p1, p2):
        x1, y1, z1 = p1
        x2, y2, z2 = p2

        dx = x2 - x1
        dy = y2 - y1
        dz = z2 - z1

        # Determine o maior deslocamento para o número de passos
        steps = max(abs(dx), abs(dy), abs(dz))

        if steps == 0:
            return [(x1, y1, z1)] # Retorna apenas o ponto se forem coincidentes

        x_increment = dx / steps
        y_increment = dy / steps
        z_increment = dz / steps

        points = []
        x, y, z = float(x1), float(y1), float(z1) # Usar floats para precisão incremental

        for _ in range(int(steps) + 1): # Inclui o ponto final
            points.append((round(x), round(y), round(z)))
            x += x_increment
            y += y_increment
            z += z_increment
            
        return points
    
    # Função para girar o cubo por um ângulo específico
    def rotate_by_angle(self, angle_increment):
        print("Botão acionado")
        self.rotation_angle_y += angle_increment # Adiciona o incremento ao ângulo
        self.rotation_angle_y %= 360.0 # Garante que o ângulo fique entre 0 e 360
        self.redraw() # Redesenha a cena com o novo ângulo

    # TRANSFORMAÇÕES NO CUBO:
    def escala(self, sx, sy, sz):
        #Passa os pontos do cubo desenhado para a função de escala que retorna os novos pontos do cubo
        self.cube_vertices = Escala.realizar_escala3D(self.cube_vertices, sx, sy, sz)

        #Remove o cubo anterior
        c = [] 
        #Desenha o novo cubo
        self.redraw()
    
    def translacao(self, tx, ty, tz):
        #Passa os pontos do cubo desenhado para a função de escala que retorna os novos pontos do cubo
        print("Antes: ", self.cube_vertices)
        self.cube_vertices = Translacao.realizar_translacao3D(self.cube_vertices, tx, ty, tz)
        print("Depois: ", self.cube_vertices)
        #Remove o cubo anterior
        self.points = [] 
        #Desenha o novo cubo
        self.redraw()
        

def desenhar(tab4):
    # Frame esquerdo (Interface do usuário)
    frame_left = tk.Frame(tab4, width=200, height=600)
    frame_left.configure(background="#000C66")
    frame_left.pack(side=tk.LEFT, fill=tk.BOTH, expand=False)

    # Frame para o lado direito (openGL)
    frame_right = tk.Frame(tab4, width=800, height=600)
    frame_right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    ogl_frame = opengl3D(frame_right, width=800, height=600)
    ogl_frame.pack(fill="both", expand=True)

    # --- Criação da interface ---
    # Inserir tamanho da janela mundo
    entry_vp_X = ctk.CTkEntry(frame_left, placeholder_text="X", width=50)
    entry_vp_X.grid(row=0, column=0, pady=1, padx=1)

    entry_vp_Y = ctk.CTkEntry(frame_left, placeholder_text="Y", width=50)
    entry_vp_Y.grid(row=0, column=1, pady=1, padx=1)

    entry_vp_Z = ctk.CTkEntry(frame_left, placeholder_text="Z", width=50)
    entry_vp_Z.grid(row=0, column=2, pady=1, padx=1)

    # Botão para definir janela mundo
    btn_janela_mundo = tk.Button(frame_left, text="Def. Janela\nMundo", command=lambda: ogl_frame.definir_janela_mundo(int(entry_vp_X.get()), int(entry_vp_Y.get()), int(entry_vp_Z.get())))
    btn_janela_mundo.grid(row=0, column=3, pady=3, padx=2)

    # Caixa de entrada para tamanho do cubo
    entry_cube = ctk.CTkEntry(frame_left, placeholder_text="size", width=50)
    entry_cube.grid(row=1, column=0, pady=5, padx=5)
     # Botão para desenhar cubo
    btn_draw_cube = tk.Button(frame_left, text="Desenhar", command=lambda: ogl_frame.criar_cubo(int(entry_cube.get())))
    btn_draw_cube.grid(row=1, column=2, pady=3, padx=2)

    # Cria o botão "Girar 30°"
    btn_rotate_30 = tk.Button(frame_left, text="Girar 30°", command=lambda: ogl_frame.rotate_by_angle(30))
    btn_rotate_30.grid(row=8, column=0, pady=3, padx=2) # Posiciona o botão
    #ogl_frame.after(100, lambda: ogl_frame.escala(sx, sy, sz))
    #ogl_frame.after(100, lambda: ogl_frame.translacao(100, 100, 100))

