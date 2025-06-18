'''
    Classe que renderiza o OpenGl na tela
'''

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from pyopengltk import OpenGLFrame
import tkinter as tk
import customtkinter as ctk

from Transformações import Rotacao
from Transformações import Translacao
from Transformações import Escala
from Transformações import Cisalhamento
from Transformações import Reflexao
from Transformações import ReflexaoQualquer

class AppOgl(OpenGLFrame):
    def __init__(self, master=None, **kw):
        super().__init__(master, **kw)
        self.points = []  # Lista de pontos para armazenar o desenho (para DDA)
        self.square_points_list = [] # Lista de vértices do quadrado atual
       
    def initgl(self):
        """Inicializa o ambiente OpenGL com configurações genéricas."""
        glClearColor(0.7, 0.7, 0.7, 0.0) # Cor de fundo do OpenGL
        self.vp_width = self.winfo_reqwidth()
        self.vp_height = self.winfo_reqheight()
        print("width x height: ", self.vp_width, "x", self.vp_height)
        self.redraw()
    
    # Define a janela em coordenadas do mundo de acordo com a entrada do usuário
    def definir_janela_mundo(self, new_vp_width, new_vp_height):
        self.vp_width = new_vp_width
        self.vp_height = new_vp_height
        self.redraw()

    def redraw(self):
        self.draw_scene()

    def draw_scene(self):
        """Redesenha a cena OpenGL, configurando a projeção e modelo-visão a cada frame."""
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT) # Limpa os buffers
        # --- Configuração da PROJEÇÃO para 2D ---
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
    
        # Definindo view port
        # Mapeia o centro da janela para (0,0) com eixos indo de -largura/2 a +largura/2
        gluOrtho2D(-self.vp_width/2, self.vp_width/2, -self.vp_height/2, self.vp_height/2)

        # --- Configuração da CÂMERA/MODELO para 2D ---
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity() # Resetar a matriz MODELVIEW para cada frame

        # Desenha os eixos X e Y
        self.draw_axes(self.vp_width, self.vp_height) 

        # Desenha os pontos armazenados na lista (do DDA)
        glBegin(GL_POINTS)
        glColor3f(1.0, 0, 0)
        for point in self.points:
            glVertex2f(point[0], point[1])
        
        for point in self.square_points_list:
            glVertex2f(point[0], point[1])
        glEnd()

        # Força a troca de buffers e atualização na tela
        self.tkSwapBuffers() 


    def limpar(self):
        self.points.clear()
        self.square_points_list.clear() # Limpa os pontos do quadrado
        self.redraw()

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
        #self.draw_pixel(round(x), round(y))
        for k in range(int(steps)):
            x += xIncrement
            y += yIncrement
            self.points.append((x, y))
            #self.draw_pixel(round(x), round(y))
        
        
    

    #Método para desenhar quadrado na origem, usa o método DDA
    def square_points(self, size):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT) # Quando desenhar novo quadrado, limpa a tela antes
        self.points = []
        self.square_points_list = []

        x = round(size)/2
        y = round(size)/2
        self.DDA(0, 0, size, 0)
        self.DDA(size, 0, size, size)
        self.DDA(size, size, 0, size)
        self.DDA(0, size, 0, 0)

        #Lista para armazenar os vértices do quadrado
        self.square_points_list = [(0, 0), (0, size), (size, size), (size, 0)]

        self.redraw()

        return (0, 0), (0, size), (size, size), (size, 0)
    
    #Método para desenhar quadrado após a transformação
    def draw_square(self, point1, point2, point3, point4):
        self.DDA(point1[0], point1[1], point2[0], point2[1])
        self.DDA(point2[0], point2[1], point3[0], point3[1])
        self.DDA(point3[0], point3[1], point4[0], point4[1])
        self.DDA(point4[0], point4[1], point1[0], point1[1])

        self.redraw()



    #Transformações no Quadrado
    def escala(self, sx, sy):
        #Passa os pontos do quadrado desenhado para a função de escala que retorna os novos pontos do quadrado
        self.square_points_list = Escala.realizar_escala(self.square_points_list, sx, sy)

        #Remove o quadrado anterior
        self.points = [] 

        #Desenha o novo quadrado
        self.draw_square(*self.square_points_list) #passa os parametros da função ao desempacotar a lista (p1, p2, etc.)

    def translacao(self, tx, ty):
        
        self.square_points_list = Translacao.realizar_translacao(self.square_points_list, tx, ty)

        #Remove o quadrado anterior
        self.points = []

        #Desenha o novo quadrado transladado
        self.draw_square(*self.square_points_list)
    
    def rotacao(self, angle):
        
        self.square_points_list = Rotacao.realizar_rotacao(self.square_points_list, angle)

        #Remove o quadrado anterior
        self.points = []

        #Desenha o novo quadrado rotacionado
        self.draw_square(*self.square_points_list)
    
    def cisalhamento(self, a, b):

        self.square_points_list = Cisalhamento.realizar_cisalhamento(self.square_points_list, a, b)

        #Remove o quadrado anterior
        self.points = []

        #Desenha o novo quadrado rotacionado
        self.draw_square(*self.square_points_list)
    
    def reflexaoX(self):

        self.square_points_list = Reflexao.realizar_reflexaoX(self.square_points_list)

        #Remove o quadrado anterior
        self.points = []

        #Desenha o novo quadrado rotacionado
        self.draw_square(*self.square_points_list)
    
    def reflexaoY(self):

        self.square_points_list = Reflexao.realizar_reflexaoY(self.square_points_list)

        #Remove o quadrado anterior
        self.points = []

        #Desenha o novo quadrado rotacionado
        self.draw_square(*self.square_points_list)

    def reflexaoOrigem(self):

        self.square_points_list = Reflexao.realizar_reflexaoOrigem(self.square_points_list)

        #Remove o quadrado anterior
        self.points = []

        #Desenha o novo quadrado rotacionado
        self.draw_square(*self.square_points_list)

    def reflexao45(self):

        self.square_points_list = Reflexao.realizar_reflexao45(self.square_points_list)

        #Remove o quadrado anterior
        self.points = []

        #Desenha o novo quadrado rotacionado
        self.draw_square(*self.square_points_list)
    
    def reflexaoQualquer(self, m, b):

        self.square_points_list = ReflexaoQualquer.realizar_reflexao_qualquer(self.square_points_list, m, b)

        #Remove o quadrado anterior
        self.points = []

        #Desenha o novo quadrado rotacionado
        self.draw_square(*self.square_points_list)

def desenhar(tab1):
     # Frame para o lado esquerdo
    frame_left = tk.Frame(tab1, width=150, height=600)
    frame_left.configure(background="#000C66")
    frame_left.pack(side=tk.LEFT, fill=tk.BOTH, expand=False)

    # Frame intermediário1
    frame_mid1 = tk.Frame(tab1, width=75, height=600)
    frame_mid1.configure(background="#000C66")
    frame_mid1.pack(side=tk.LEFT, fill=tk.BOTH, expand=False)

    # Frame intermediário2
    frame_mid2 = tk.Frame(tab1, width=75, height=600)
    frame_mid2.configure(background="#000C66")
    frame_mid2.pack(side=tk.RIGHT, fill=tk.BOTH, expand=False)

    # Frame para o lado direito
    frame_right = tk.Frame(tab1, width=700, height=600)
    frame_right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
    
    # Adicionar o frame OpenGL ao lado direito
    ogl_frame = AppOgl(frame_right, width=700, height=600)
    ogl_frame.pack(fill=tk.BOTH, expand=True)  # Definindo expand=False para manter o tamanho fixo
    #ogl_frame.animate = 1 # Função para atualizar o frame 

    # Inserir tamanho da janela mundo
    entry_width = ctk.CTkEntry(frame_left, placeholder_text="Largura", width=50)
    entry_width.pack()

    entry_height = ctk.CTkEntry(frame_left, placeholder_text="Altura", width=50)
    entry_height.pack()

    # Botão para definir janela mundo
    btn_janela_mundo = tk.Button(frame_left, text="Def. Janela\nMundo", command=lambda: ogl_frame.definir_janela_mundo(int(entry_width.get()), int(entry_height.get())))
    btn_janela_mundo.pack()

    # Botão para desenhar um quadrado, chama a função desejada ao apertar botão(command=funcao_executada)
    btn_desenhar_quadrado = tk.Button(frame_left, text="Desenhar\nQuadrado", command=lambda: ogl_frame.square_points(int(entry_tamanho.get())))
    btn_desenhar_quadrado.pack()

    # Caixa de entrada para o tamanho do quadrado
    entry_tamanho = ctk.CTkEntry(frame_left, placeholder_text="size", height=10, width=40)
    entry_tamanho.pack(pady=0)

    # Botão para Escala
    btn_scale = tk.Button(frame_left, text="Aplicar\nEscala", command=lambda: ogl_frame.escala(float(entry_sx.get()), float(entry_sy.get()))) #Converter para int sempre que chamar a função
    btn_scale.pack()

    # Caixa de entrada para Fator de escala Sx
    entry_sx = ctk.CTkEntry(frame_left, placeholder_text="sx", height=10, width=40)
    entry_sx.pack(pady=0)

    # Caixa de entrada para Fator de escala Sy
    entry_sy = ctk.CTkEntry(frame_left, placeholder_text="sy", height=10, width=40)
    entry_sy.pack(pady=0)

    # Botão para Translação
    btn_translate = tk.Button(frame_left, text="Aplicar\nTranslação", command=lambda: ogl_frame.translacao(int(entry_tx.get()), int(entry_ty.get())))
    btn_translate.pack()

    # Caixa de entrada para Translação Tx
    entry_tx = ctk.CTkEntry(frame_left, placeholder_text="Tx", height=10, width=40)
    entry_tx.pack(pady=0)

    # Caixa de entrada para Translação Ty
    entry_ty = ctk.CTkEntry(frame_left, placeholder_text="Ty", height=10, width=40)
    entry_ty.pack(pady=0)

    # Botão para Rotação
    btn_translate = tk.Button(frame_left, text="Aplicar\nRotação", command=lambda: ogl_frame.rotacao(int(entry_rot.get())))
    btn_translate.pack()

    # Caixa de entrada para ângulo de Rotação
    entry_rot = ctk.CTkEntry(frame_left, placeholder_text="ang", height=10, width=40)
    entry_rot.pack(pady=0)

    # Botão para Cisalhamento
    btn_translate = tk.Button(frame_left, text="Aplicar\nCisalhamento", command=lambda: ogl_frame.cisalhamento(int(entry_a.get()), int(entry_b.get())))
    btn_translate.pack()

    # Caixa de entrada para Fator A de cisalhamento
    entry_a = ctk.CTkEntry(frame_left, placeholder_text="a", height=10, width=40)
    entry_a.pack(pady=0)

    # Caixa de entrada para Fator B de cisalhamento
    entry_b = ctk.CTkEntry(frame_left, placeholder_text="b", height=10, width=40)
    entry_b.pack(pady=0)

    # Botão para Reflexão em X
    btn_translate = tk.Button(frame_mid1, text="Ref X", command=lambda: ogl_frame.reflexaoX())
    btn_translate.pack()

    # Botão para Reflexão em Y
    btn_translate = tk.Button(frame_mid1, text="Ref Y", command=lambda: ogl_frame.reflexaoY())
    btn_translate.pack()

    # Botão para Reflexão na Origem
    btn_translate = tk.Button(frame_mid1, text="Ref Origem", command=lambda: ogl_frame.reflexaoOrigem())
    btn_translate.pack()

    # Botão para Reflexão na Reta de 45 graus
    btn_translate = tk.Button(frame_mid1, text="Ref Reta 45", command=lambda: ogl_frame.reflexao45())
    btn_translate.pack()

    # Botão para Reflexão Qualquer
    btn_translate = tk.Button(frame_left, text="Aplicar\nReflexao\nQualquer", command=lambda: ogl_frame.reflexaoQualquer(float(entry_m.get()), float(entry_b_reta.get())))
    btn_translate.pack()

    # Caixa de entrada para M da Reta da Reflexão Qualquer
    entry_m = ctk.CTkEntry(frame_left, placeholder_text="m", height=10, width=40)
    entry_m.pack(pady=0)

    # Caixa de entrada para B da Reta da Reflexão Qualquer
    entry_b_reta = ctk.CTkEntry(frame_left, placeholder_text="b", height=10, width=40)
    entry_b_reta.pack(pady=0)

    # Botão para Limpar objetos desenhados
    btn_desenhar_circulo = tk.Button(frame_left, text="Limpar", command=lambda: ogl_frame.limpar())
    btn_desenhar_circulo.pack(pady=20)