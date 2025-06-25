from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from pyopengltk import OpenGLFrame
import numpy as np
import tkinter as tk
import customtkinter as ctk
import math

class Reta_circ(OpenGLFrame):
    def initgl(self):
        """Inicializa o ambiente OpenGL"""
        glClearColor(0.7, 0.7, 0.7, 0.0)  # Cor de fundo do openGL
        self.vp_width = self.winfo_reqwidth()
        self.vp_height = self.winfo_reqheight()
        print("width x height: ", self.vp_width, "x", self.vp_height)
        
        self.pontos = []  # Lista de pontos para armazenar o desenho
        self.redraw() # Sempre atualizar cena para aplicar alterações
    
    def redraw(self):
        self.draw_scene()

    # Define a janela em coordenadas do mundo de acordo com a entrada do usuário
    def definir_janela_mundo(self, new_vp_width, new_vp_height):
        self.vp_width = new_vp_width
        self.vp_height = new_vp_height
        self.redraw()

    def draw_scene(self):
        """Redesenha a cena OpenGL para que os objetos etc. fiquem na tela"""
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()

        #Definindo view port
        gluOrtho2D(-self.vp_width/2, self.vp_width/2, -self.vp_height/2, self.vp_height/2)

         # --- Configuração da CÂMERA/MODELO para 2D ---
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity() # Resetar a matriz MODELVIEW para cada frame

        self.draw_axes(self.vp_width, self.vp_height) #Desenhar eixos X e Y

        # Desenha os pontos armazenados na listaAdd commentMore actions
        glBegin(GL_POINTS)
        glColor3f(1.0, 0, 0)
        for point in self.pontos:
            glVertex2f(point[0], point[1])
        glEnd()

        self.tkSwapBuffers() # Força a troca de buffers e atualização na tela

    def limpar(self):
        self.pontos.clear()
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

    def DDA(self, x1, y1, x2, y2):
        dx = x2 - x1 # Variação de x
        dy = y2 - y1 # Variação de y

        # Número de passos necessários para desenhar a reta
        length = max(abs(dx), abs(dy))
        
        # Caso dx = dy = 0, a reta é só um ponto
        if length == 0:
            return [(round(x1), round(y1))] 

        # Incrementos de x e y
        x_increment = dx / length
        y_increment = dy / length

        x, y = x1, y1
        self.pontos.append((round(x), round(y)))  # Adiciona o primeiro ponto

        # Loop de desenha a reta
        while round(x) != round(x2) or round(y) != round(y2):
            x += x_increment
            y += y_increment
            self.pontos.append((round(x), round(y)))
      
        self.redraw() # Sempre atualizar cena após alteração

        return ((x, y))   
    
    def pontoMedio(self, x1, y1, x2, y2):

        # Garante que a reta sempre vá da esquerda para a direita (em x)
        if x1 > x2:
            x1, y1, x2, y2 = x2, y2, x1, y1

        dx = x2 - x1  # Diferença em x
        dy = y2 - y1  # Diferença em y

        # Verifica se a reta é "íngreme" (|dy| > |dx|) e se for, inverte x e y para tratar como uma reta menos inclinada
        if abs(dy) > abs(dx):
            x1, y1, x2, y2 = y1, x1, y2, x2  # Troca coordenadas
            steep = True  # Marca que a reta foi invertida
        else:
            steep = False  # Não foi necessário inverter

        # Recalcula as diferenças após possível troca
        dx = abs(x2 - x1)
        dy = abs(y2 - y1)

        # Inicializa o parâmetro de decisão do algoritmo de ponto médio
        d = 2 * dy - dx
        incE = 2 * dy           # Incremento quando escolhe o pixel do Leste
        incNE = 2 * (dy - dx)   # Incremento quando escolhe o pixel do Nordeste

        x, y = x1, y1  # Começa a desenhar do ponto inicial

        # Determina se o y deve subir (+1) ou descer (-1) conforme direção da reta
        step_y = 1 if y2 > y1 else -1

        # Laço principal que percorre todos os pixels da reta
        for _ in range(dx + 1):
            # Adiciona o ponto à lista, invertendo se necessário
            self.pontos.append((y, x) if steep else (x, y))

            # Atualiza o valor de d e escolhe o próximo ponto
            if d <= 0:
                d += incE  # Move para o pixel do Leste
            else:
                d += incNE  # Move para o pixel do Nordeste
                y += step_y  # Altera o y conforme a direção da reta

            x += 1  # Sempre avança em x

        self.redraw() # Sempre atualizar cena após alteração

        return ((x, y))   

    def pontoCirculo(self, x, y):
        self.pontos.append((x, y))
        self.pontos.append((y, x))
        self.pontos.append((y, -x))
        self.pontos.append((x, -y))
        self.pontos.append((-x, -y))
        self.pontos.append((-y, -x))
        self.pontos.append((-y, x))
        self.pontos.append((-x, y))
    
    def circPontoMedio(self, raio):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT) # Quando desenhar novo círculo, limpa a tela antes
        points = []
        x = 0
        y = raio
        d = round(5/4 - raio)

        points.append((round(x), round(y)))
        self.pontoCirculo(round(x), round(y))
        
        while(y > x):
            if(d < 0):
                d += 2 * x + 3
            else:
                d += 2 * (x - y) + 5
                y -= 1
            x += 1
            points.append((round(x), round(y)))
            self.pontoCirculo(round(x), round(y))
        
        self.redraw()  # Desenha a cena com o novo círculo (atualização)
        
        return points
    
    def circEquacaoExplicita(self, raio):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT) # Quando desenhar novo círculo, limpa a tela antes

        '''
        Usa a equação do círculo y = sqrt(raio**2 - x**2)
        '''
        x = -raio
        while x <= raio:
            y = math.sqrt(raio**2 - x**2)
            self.pontoCirculo(int(x), int(y))
            x += 1 # Precisão do desenho
        
        self.redraw()  # Desenha a cena com o novo círculo

    def circTrigonometrico(self, raio):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT) # Quando desenhar novo círculo, limpa a tela antes

        num_pontos = 1000  # Número de pontos para desenhar o círculo
        for i in range(num_pontos):
            theta = 2.0 * math.pi * i / num_pontos
            x = raio * math.cos(theta)
            y = raio * math.sin(theta)
            self.pontos.append((round(x), round(y)))
        
        self.redraw() 

    def pontoElipse(self, x, y):
        self.pontos.append((x, y))
        self.pontos.append((-x, y))
        self.pontos.append((x, -y))
        self.pontos.append((-x, -y))

    '''Método para desenhar elipse pelo Algoritmo do Ponto-Medio para conversão matricial de elipses'''
    def elipsePontoMedio(self, a, b):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT) # Quando desenhar nova elipse, limpa a tela antes

        x = 0
        y = b
        d1 = b * b - a * a * b + a * a / 4.0

        self.pontoElipse(x, y)
        
        while((a * a * (y - 0.5)) > (b * b * (x + 1))):
            # Região 1
            if d1 < 0:
                d1 = d1 + b * b * (2 * x + 3)
                x += 1
            else:
                d1 = d1 + b * b * (2 * x + 3) + a * a * (-2 * y + 2)
                x += 1
                y -= 1
            
            self.pontoElipse(x, y)


        # Região 2
        d2 = b * b * (x + 0.5) * (x + 0.5) + a * a * (y - 1) * (y - 1) - a * a * b * b
        while y > 0:
            if d2 < 0:
                d2 = d2 + b * b * (2 * x + 2) + a * a * (-2 * y + 3)
                x += 1
                y -= 1
            else:
                d2 = d2 + a * a * (-2 * y + 3)
                y -= 1
            
            self.pontoElipse(x, y)
  
        self.redraw()  # Desenha a cena com a nova elipse

    def printPontos(self, points):
        for element in points:
            print(element)


def desenhar(tab6):
    frame_left = tk.Frame(tab6, width=200, height=600)
    frame_left.configure(background="#000C66")
    frame_left.pack(side=tk.LEFT, fill=tk.BOTH, expand=False)

    # Frame para o lado direito
    frame_right = tk.Frame(tab6, width=800, height=600)
    frame_right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    ogl_frame_reta_circ = Reta_circ(frame_right, width=800, height=600)
    ogl_frame_reta_circ.pack(fill="both", expand=True)
    
    # Atualização da janela
    #ogl_frame_reta_circ.animate = 1

    # Inserir tamanho da janela mundo
    entry_width = ctk.CTkEntry(frame_left, placeholder_text="Largura", width=50)
    entry_width.grid(row=0, column=0, pady=1, padx=1)

    entry_height = ctk.CTkEntry(frame_left, placeholder_text="Altura", width=50)
    entry_height.grid(row=0, column=1, pady=1, padx=1)

    # Botão para definir janela mundo
    btn_janela_mundo = tk.Button(frame_left, text="Def. Janela\nMundo", command=lambda: ogl_frame_reta_circ.definir_janela_mundo(int(entry_width.get()), int(entry_height.get())))
    btn_janela_mundo.grid(row=0, column=2, pady=3, padx=2)

    # Caixa de entrada para Raio do circulo
    entry_raio = ctk.CTkEntry(frame_left, placeholder_text="raio", width=50)
    entry_raio.grid(row=1, column=0, pady=5, padx=5)

    # Botão para desenhar um circulo pelo método do ponto médio
    btn_desenhar_circulo = tk.Button(frame_left, text="Circulo\n P.M.", command=lambda: ogl_frame_reta_circ.circPontoMedio(int(entry_raio.get())))
    btn_desenhar_circulo.grid(row=2, column=0)

    # Botão para desenhar um circulo pelo método da equação explícita
    btn_desenhar_circulo = tk.Button(frame_left, text="Circulo eq.\nexplicita", command=lambda: ogl_frame_reta_circ.circEquacaoExplicita(int(entry_raio.get())))
    btn_desenhar_circulo.grid(row=2, column=1, padx=2)

    # Botão para desenhar um circulo pelo método Trigonométric
    btn_desenhar_circulo = tk.Button(frame_left, text="Circulo\nTrigonométrica", command=lambda: ogl_frame_reta_circ.circTrigonometrico(int(entry_raio.get())))
    btn_desenhar_circulo.grid(row=2, column=2)

    # Caixas de entrada para pontos da reta
    entry_x1 = ctk.CTkEntry(frame_left, placeholder_text="x1", width=50)
    entry_x1.grid(row=3, column=0, pady=10, padx=5)

    entry_y1 = ctk.CTkEntry(frame_left, placeholder_text="y1", width=50)
    entry_y1.grid(row=3, column=1, pady=10, padx=5)

    entry_x2 = ctk.CTkEntry(frame_left, placeholder_text="x2", width=50)
    entry_x2.grid(row=4, column=0, padx=5)

    entry_y2 = ctk.CTkEntry(frame_left, placeholder_text="y2", width=50)
    entry_y2.grid(row=4, column=1, padx=5)

    # Botão para desenhar reta (DDA)
    btn_desenhar_reta_dda = tk.Button(frame_left, text="Desenhar reta(DDA)", command=lambda: ogl_frame_reta_circ.DDA(int(entry_x1.get()), int(entry_y1.get()), int(entry_x2.get()), int(entry_y2.get())))
    btn_desenhar_reta_dda.grid(row=4, column=2)
    
    # Botão para desenhar a reta (ponto médio)
    btn_desenhar_reta_pm = tk.Button(frame_left, text="Desenhar reta(P.M)", command=lambda: ogl_frame_reta_circ.pontoMedio(int(entry_x1.get()), int(entry_y1.get()), int(entry_x2.get()), int(entry_y2.get())))
    btn_desenhar_reta_pm.grid(row=5, column=2)

    # Entradas Elipse:
    entry_a = ctk.CTkEntry(frame_left, placeholder_text="a", width=50)
    entry_a.grid(row=6, column=0, padx=5, pady=20)

    entry_b = ctk.CTkEntry(frame_left, placeholder_text="b", width=50)
    entry_b.grid(row=6, column=1, padx=5, pady=20)

    # Botão para desenhar Elipse ponto médio
    btn_desenhar_elipse = tk.Button(frame_left, text="Elipse P.M.", command=lambda: ogl_frame_reta_circ.elipsePontoMedio(int(entry_a.get()), int(entry_b.get())))
    btn_desenhar_elipse.grid(row=6, column=2)

    # Botão para Limpar objetos desenhados
    btn_desenhar_circulo = tk.Button(frame_left, text="Limpar", command=lambda: ogl_frame_reta_circ.limpar())
    btn_desenhar_circulo.grid(row=9, column=1, pady=20)

     # Botão para Limpar objetos desenhados
    btn_desenhar_circulo = tk.Button(frame_left, text="Atualizar tela", command=lambda: ogl_frame_reta_circ.redraw())
    btn_desenhar_circulo.grid(row=9, column=0, pady=20)

