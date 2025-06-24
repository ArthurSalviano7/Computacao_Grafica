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
        self.width = width
        self.height = height
        self.points = []
        self.current_index = 0
        self.start_time = 0
        self.display_duration = 10  # Segundos
        self.is_running = False
        self.heartbeat_max = 100
        self.heartbeat_min = 30
    
    
    def initgl(self):
        
        glClearColor(0.0, 0.0, 0.0, 1.0)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluOrtho2D(0, self.width, 0, self.height)

    def create_points(self):
        self.points = []
        y_base = self.height // 2
        x = 0

        while x < self.width:
            if len(self.points) % 20 == 0:
                low = y_base - random.randint(self.heartbeat_min, self.heartbeat_max)
                high = y_base + random.randint(self.heartbeat_min, self.heartbeat_max)
                self.points.append((x, low))
                x += 10
                self.points.append((x, high))
            else:
                self.points.append((x, y_base))
            x += 10

        self.current_index = 0
        
    def draw_scene(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluOrtho2D(0, self.width, 0, self.height)

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        if self.is_running:
            glColor3f(0, 1, 0)
            glBegin(GL_LINE_STRIP)
            for i in range(self.current_index):
                x, y = self.points[i]
                glVertex2f(x, y)
            glEnd()

            self.current_index += 1
            if self.current_index >= len(self.points) or time.time() - self.start_time >= self.display_duration:
                self.is_running = False
                self.current_index = 0
                self.create_points()

        self.tkSwapBuffers()
        if self.is_running:
            self.after(33, self.redraw)

    def redraw(self):
        self.draw_scene()


    def start_simulation(self, duration=None):
        try:
            if duration is not None:
                self.display_duration = float(duration)
            else:
                self.display_duration = 10  # Valor padrão
        except ValueError:
            self.display_duration = 10

        self.create_points()
        self.start_time = time.time()
        self.is_running = True
        self.redraw()
        

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

    
    # Atualização da janela
    
    # Inserir tamanho da janela mundo
    entry_width = ctk.CTkEntry(frame_left, placeholder_text="Largura", width=50)
    entry_width.grid(row=0, column=0, pady=1, padx=1)

    entry_height = ctk.CTkEntry(frame_left, placeholder_text="Altura", width=50)
    entry_height.grid(row=0, column=1, pady=1, padx=1)

    # Botão para definir janela mundo
    btn_janela_mundo = tk.Button(frame_left, text="Def. Janela\nMundo", command=lambda: ogl_ecg.definir_janela_mundo(int(entry_width.get()), int(entry_height.get())))
    btn_janela_mundo.grid(row=0, column=2, pady=3, padx=2)

    # Caixa de entrada para o tempo da simulação
    entry_time = ctk.CTkEntry(frame_left, placeholder_text="Tempo simulação (s)", width=100)
    entry_time.grid(row=1, column=0, columnspan=2, padx=5, pady=5)

    # Botão para iniciar a simulação
    btn_start_ecg = tk.Button(frame_left, text="Iniciar ECG", command=lambda: ogl_ecg.start_simulation(entry_time.get()))
    btn_start_ecg.grid(row=1, column=2, pady=10)
