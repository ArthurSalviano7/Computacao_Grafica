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

    # Simetria dos pontos nos 8 oitantes
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
        # Limpa os buffers de cor e profundidade para preparar o novo desenho
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    
        points = []  # Lista que armazenará os pontos calculados do círculo

        # Inicializa as coordenadas do primeiro ponto no eixo Y
        x = 0
        y = raio

        # Define o valor inicial da decisão, com base na equação do ponto médio
        # A fórmula é d = 1 - raio, mas o arredondamento com 5/4 melhora a precisão para inteiros
        d = round(5/4 - raio)

        # Adiciona o primeiro ponto e seus simétricos (usando simetria octal)
        points.append((round(x), round(y)))
        self.pontoCirculo(round(x), round(y))  # Desenha os 8 pontos simétricos a partir desse

        # Enquanto y > x (só desenha 1/8 do círculo, os outros 7/8 são por simetria)
        while y > x:
            if d < 0:
                # Próximo ponto está dentro do círculo, então só incrementa x
                d += 2 * x + 3
            else:
                # Próximo ponto está fora ou na borda, decrementa y e incrementa x
                d += 2 * (x - y) + 5
                y -= 1
            x += 1

            # Armazena e desenha o novo ponto calculado com simetria
            points.append((round(x), round(y)))
            self.pontoCirculo(round(x), round(y))

        # Atualiza a cena para mostrar o círculo completo
        self.redraw()

        return points  # Retorna os pontos usados no desenho

    
    def circEquacaoExplicita(self, raio):
        # Limpa a tela antes de desenhar o novo círculo
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        '''
        A equação do círculo centrado na origem é: x² + y² = r²
        Despejando y: y = sqrt(r² - x²)
        Este algoritmo percorre valores de x de -raio até +raio
        e calcula o valor correspondente de y para desenhar os pontos do arco superior do círculo.
        '''
        x = -raio  # Começa no extremo esquerdo do círculo

        while x <= raio:
            # Calcula o y correspondente usando a equação do círculo
            y = math.sqrt(raio**2 - x**2)

            # Desenha o ponto (x, y) e seus simétricos (via método pontoCirculo)
            self.pontoCirculo(int(x), int(y))

            # Avança no eixo x. Como estamos trabalhando com inteiros,
            # a precisão depende de quão pequenos são os passos (1, 0.5, etc.)
            x += 1

        # Atualiza a cena para exibir o círculo completo
        self.redraw()


    def circTrigonometrico(self, raio, h=0, k=0, passo=0.01):
        # Passo 1: Inicializa a tela e os parâmetros
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        theta = 0.0  # Início do ângulo
        self.pontos.clear()  # Limpa lista anterior, se houver

        # Passo 2: Testa se já percorreu toda a circunferência
        while theta < 2 * math.pi:
            # Passo 3: Calcula coordenadas x e y
            x = round(raio * math.cos(theta))
            y = round(raio * math.sin(theta))

            # Passo 4: Adiciona os 8 pontos simétricos ao redor do centro (h, k)
            self.pontos.append((h + x, k + y))
            self.pontos.append((h + y, k + x))
            self.pontos.append((h - y, k + x))
            self.pontos.append((h - x, k + y))
            self.pontos.append((h - x, k - y))
            self.pontos.append((h - y, k - x))
            self.pontos.append((h + y, k - x))
            self.pontos.append((h + x, k - y))

            # Passo 5: Incrementa o ângulo
            theta += passo

        # Passo 6: Atualiza a tela
        self.redraw()


    def pontoElipse(self, x, y):
        self.pontos.append((x, y))
        self.pontos.append((-x, y))
        self.pontos.append((x, -y))
        self.pontos.append((-x, -y))

    '''Método para desenhar elipse pelo Algoritmo do Ponto-Medio para conversão matricial de elipses'''
    def elipsePontoMedio(self, a, b):
        # Limpa a tela antes de desenhar a nova elipse
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Começa do ponto mais alto da elipse (x = 0, y = b)
        x = 0
        y = b

        # Calcula o valor inicial da decisão para a Região 1
        d1 = b * b - a * a * b + a * a / 4.0

        # Desenha o ponto inicial e seus simétricos (provavelmente com simetria quádrupla)
        self.pontoElipse(x, y)

        # Região 1: enquanto a inclinação da tangente é < -1 (ou seja, dy/dx > 1)
        # Isso acontece quando (a²)(y - 0.5) > (b²)(x + 1)
        while((a * a * (y - 0.5)) > (b * b * (x + 1))):
            if d1 < 0:
                # Ponto dentro da elipse — só avança no eixo x
                d1 = d1 + b * b * (2 * x + 3)
                x += 1
            else:
                # Ponto fora da elipse — avança em x e recua em y
                d1 = d1 + b * b * (2 * x + 3) + a * a * (-2 * y + 2)
                x += 1
                y -= 1
        
            self.pontoElipse(x, y)

        # Região 2: a inclinação da tangente é >= -1 (ou seja, dy/dx <= 1)
        # Calcula valor inicial da decisão para Região 2
        d2 = b * b * (x + 0.5)**2 + a * a * (y - 1)**2 - a * a * b * b

        while y > 0:
            if d2 < 0:
                # Ponto dentro — avança x e reduz y
                d2 = d2 + b * b * (2 * x + 2) + a * a * (-2 * y + 3)
                x += 1
                y -= 1
            else:
                # Ponto fora — reduz apenas y
                d2 = d2 + a * a * (-2 * y + 3)
                y -= 1
        
            self.pontoElipse(x, y)

        # Atualiza a cena com a elipse desenhada
        self.redraw()

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

