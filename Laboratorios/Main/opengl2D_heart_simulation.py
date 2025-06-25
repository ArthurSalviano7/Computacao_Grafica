from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from pyopengltk import OpenGLFrame
import numpy as np
import tkinter as tk
import customtkinter as ctk
import math
import random
import time


class HeartSimulation(OpenGLFrame):
    def __init__(self, master=None, width=800, height=500, **kwargs):
        super().__init__(master, width=width, height=height, **kwargs)
        
        # Define as dimensões da janela de visualização
        self.width = width
        self.height = height

        # Lista que armazenará os pontos do traçado do ECG
        self.points = []

        # Índice do ponto atual a ser desenhado
        self.current_index = 0

        # Tempo em que a simulação começou
        self.start_time = 0

        # Duração total da simulação (em segundos)
        self.display_duration = 10

        # Flag que indica se a simulação está em execução
        self.is_running = False

        # Variação máxima e mínima para o "batimento"
        self.heartbeat_max = 100
        self.heartbeat_min = 30
    
    
    def initgl(self):
        
        # Define a cor do fundo como preto
        glClearColor(0.0, 0.0, 0.0, 1.0)
        
        # Define que o modo de matriz atual é o de projeção (visualização)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        
        # Projeção ortográfica 2D com base nas dimensões da janela
        gluOrtho2D(0, self.width, 0, self.height)

    def create_points(self):
        self.points = []
        y_base = self.height // 2 # Linha base de repouso onde a linha fica quando não há picos de batimento
        x = 0 # Onde a linha começa a ser desenhada

        # Gera os pontos até atingir a largura da tela
        while x < self.width:
            if len(self.points) % 20 == 0:
                # A cada 20 pontos simula um batimento cardíaco com pico e vale
                low = y_base - random.randint(self.heartbeat_min, self.heartbeat_max) # Cria um vale com valores aleatótios dentro do intervalo definido
                high = y_base + random.randint(self.heartbeat_min, self.heartbeat_max) # Cria um pico com valores aleatótios dentro do intervalo definido
                
                # Adiciona dois pontos, um de vale e um de pico 10 unidades à dureita no eixo x
                self.points.append((x, low))
                x += 10
                self.points.append((x, high))
            else:
                # Caso contrário, desenha ponto na linha base (sem batimento)
                    self.points.append((x, y_base))
            x += 10  # Avança no eixo X

        self.current_index = 0  # Reinicia o índice

        
    def draw_scene(self):
        # Limpa os buffers de cor e profundidade
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Define projeção ortográfica novamente
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluOrtho2D(0, self.width, 0, self.height)

        # Reinicia a matriz de modelo (posição da câmera virtual)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        # Se a simulação estiver em execução, desenha a linha
        if self.is_running:
            glColor3f(0, 1, 0)

            glBegin(GL_LINE_STRIP)
            for i in range(self.current_index):
                x, y = self.points[i]
                glVertex2f(x, y)  # Adiciona vértice
            glEnd()

             # Avança para o próximo ponto
            self.current_index += 1

        # Se chegou no fim da largura da tela, reinicia o traçado
        if self.current_index >= len(self.points):
            self.current_index = 0
            self.create_points()  # Gera nova linha a partir de x = 0

        # Verifica se o tempo acabou
        if time.time() - self.start_time >= self.display_duration:
            self.is_running = False

        self.tkSwapBuffers()

        if self.is_running:
            self.after(33, self.redraw) # ~ 30 FPS


    def redraw(self):
        self.draw_scene() # Redesenha a cena


    def start_simulation(self, duration=None):
        try:
            if duration is not None:
                self.display_duration = float(duration)
            else:
                self.display_duration = 10  # Valor padrão
        except ValueError:
            self.display_duration = 10 # Fallback se valor inválido

        self.create_points()  # Gera os dados do ECG
        self.start_time = time.time()  # Marca o tempo inicial
        self.is_running = True  # Liga a simulação
        self.redraw()  # Começa o desenho

        

def desenhar(tab5):
    frame_left = tk.Frame(tab5, width=300, height=600)
    frame_left.configure(background="#000C66")
    frame_left.pack(side=tk.LEFT, fill=tk.BOTH, expand=False)
    frame_left.pack_propagate(False)

    # Frame para o lado direito
    frame_right = tk.Frame(tab5, width=800, height=600)
    frame_right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    ogl_ecg = HeartSimulation(frame_right, width=800, height=600)
    ogl_ecg.pack(fill="both", expand=True)

    # Caixa de entrada para o tempo da simulação
    entry_time = ctk.CTkEntry(frame_left, placeholder_text="Tempo simulação (s)", width=100)
    entry_time.grid(row=1, column=0, columnspan=2, padx=5, pady=5)

    # Botão para iniciar a simulação
    btn_start_ecg = tk.Button(frame_left, text="Iniciar ECG", command=lambda: ogl_ecg.start_simulation(entry_time.get()))
    btn_start_ecg.grid(row=1, column=2, pady=10)
