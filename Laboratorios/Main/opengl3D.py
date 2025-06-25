from turtle import color
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from pyopengltk import OpenGLFrame
import numpy as np
import tkinter as tk
import customtkinter as ctk

from Transformações import MatrizComposta
from Transformações import Rotacao
from Transformações import Translacao
from Transformações import Escala
from Transformações import Cisalhamento
from Transformações import Reflexao
from Transformações import ReflexaoQualquer
from Recorte import Cohen_sutherland

'''Desenho do galpão e câmera configurada para ver todas as faces ao mesmo tempo'''
class opengl3D(OpenGLFrame):
    def __init__(self, master=None, message_text_widget=None, **kw):
        ''' Inicializa os vertices do cubo para evitar erros ao atualizar cena '''
        
        self.message_text_widget = message_text_widget # Salva a referência ao widget
        super().__init__(master, **kw)

        self.last_proj_matrix = np.identity(4) # Inicialize matrizes do openGL
        self.last_modelview_matrix = np.identity(4)

        self.cube_vertices = self.criar_vertices_cubo(50) # Lista de pontos para armazenar os vértices do cubo
        self.rotation_angle_y = 0.0  # Variável para o ângulo de rotação Y (câmera)
        self.compose_transformations = tk.BooleanVar(value=False)
        self.compose_list = [] # Lista que armazena as tranformações a serem aplicadas
        
        # Teste para log de mensagem
        if self.message_text_widget:
            self._log_message("Sistema de visualização 3D iniciado.")

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

        # Salvar as matrizes iniciais
        self.last_proj_matrix = glGetDoublev(GL_PROJECTION_MATRIX)
        self.last_modelview_matrix = glGetDoublev(GL_MODELVIEW_MATRIX)

        self.points = []  # Lista de pontos para armazenar o desenho
        self.redraw()
    
    def _log_message(self, message):
        """Método auxiliar para enviar mensagens para o terminal da GUI."""
        if self.message_text_widget: # Verifica se o widget foi passado
            self.message_text_widget.config(state="normal") # Habilita para escrita
            self.message_text_widget.insert(tk.END, message + "\n") # Adiciona a mensagem no final
            self.message_text_widget.see(tk.END) # Rola para o final para mostrar a nova mensagem
            self.message_text_widget.config(state="disabled") # Desabilita novamente
        else:
            print(message) # Fallback para console se o widget não foi configurado

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

    def criar_cubo(self, size, tx=0, ty=0, tz=0): #Funcão para criar cubo e atualizar cena
        self.cube_vertices = self.criar_vertices_cubo(size, tx, ty, tz)
        self.redraw()
    
    def criar_vertices_cubo(self, size, tx=0, ty=0, tz=0): # Desloca para fora da origem de acordo com tx, ty, tz
        print("Tamanho: ", size)
        return np.array([
            #[ x,       y,         z,       , 1]
            [0 + tx   , 0 + ty   , 0 + tz   , 1], # Adicionado 1 para coordenadas homogêneas (w)
            [size + tx, 0 + ty   , 0 + tz   , 1],
            [size + tx, size + ty, 0 + tz   , 1],
            [0 + tx   , size + ty, 0 + tz   , 1],
            [0 + tx   , 0 + ty   , size + tz, 1],
            [size + tx, 0 + ty   , size + tz, 1],
            [size + tx, size + ty, size + tz, 1],
            [0 + tx   , size + ty, size + tz, 1]
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

        # Aplicar as rotações ISOMÉTRICAS FIXAS
        glRotatef(35.36, 1, 0, 0)
        glRotatef(45, 0, -1, 0) 

        # Aplicar a rotação dinâmica da CÂMERA (botão 30º)
        glRotatef(self.rotation_angle_y, 0, 1, 0) 
        
        print("Cubo: ", self.cube_vertices)
        print("Lista: ", self.compose_list)
        # Desenhar os objetos da cena
        self.desenhar_eixos(self.vp_width, self.vp_height, self.vp_Zaxis)
        #self.desenhar_cubo()
        self.desenhar_cubo_DDA()
        
        # Força a troca de buffers e atualização na tela
        self.tkSwapBuffers()

    def reset_camera(self):
        self.rotation_angle_y = 0
        self.redraw()

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

    def desenhar_cubo_DDA(self):
        vertices = self.cube_vertices
        arestas_indices = [
            (0, 1), (1, 2), (2, 3), (3, 0), # Face frontal
            (4, 5), (5, 6), (6, 7), (7, 4), # Face traseira
            (0, 4), (1, 5), (2, 6), (3, 7)  # Conectores
        ]

        # Usa GL_POINTS para desenhar cada ponto gerado pelo DDA
        glBegin(GL_POINTS)
        glColor3f(0, 0, 0) # Cor preta para as arestas

        for i, j in arestas_indices:
            p1 = vertices[i][:3]
            p2 = vertices[j][:3]
            
            # Gerar pontos da linha usando DDA 3D
            line_points = self.DDA3D(p1, p2)
            
            # Desenhar cada ponto da linha
            for point in line_points:
                glVertex3f(point[0], point[1], point[2]) # Desenha pixel x, y, z
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
    
    # Função para girar a câmera por um ângulo específico
    def rotate_by_angle(self, angle_increment):
        self.rotation_angle_y += angle_increment # Adiciona o incremento ao ângulo
        self.rotation_angle_y %= 360.0 # Garante que o ângulo fique entre 0 e 360
        self.redraw() # Redesenha a cena com o novo ângulo

    # Função para verificar se está fora da origem:
    def verificar_se_fora_da_orig(self):
        tx, ty, tz = 0, 0, 0
        x = self.cube_vertices[0, 0]
        y = self.cube_vertices[0, 1]
        z = self.cube_vertices[0, 2]

        if x > 0: # ponto X fora da origem
            tx = -x 
        elif x < 0: # ponto X fora da origem (lado negativo)
            tx = -x # Sempre o negativo do valor atual para ir para 0
                             # Se x é -50, tx = -(-50) = 50
        
        if y > 0: # ponto Y fora da origem
            ty = -y
        elif y < 0: # ponto Y fora da origem (lado negativo)
            ty = -y
        
        if z > 0: # ponto Z fora da origem
            tz = -z
        elif z < 0: # ponto Z fora da origem (lado negativo)
            tz = -z
        
        return tx, ty, tz

    # TRANSFORMAÇÕES NO CUBO:
    def escala(self, sx, sy, sz):
        if self.compose_transformations.get(): # Adiciona escala a lista para montar matriz M composta
            self.compose_list.append(["Escala", sx, sy, sz])
            self._log_message(f"'Escala (Sx={sx}, Sy={sy}, Sz={sz})' adicionada.")
        else:
            tx, ty, tz = self.verificar_se_fora_da_orig() 

            if tx or ty or tz:
                self._log_message(f"\nCubo fora da origem:")
                self._log_message(f"1. Transladar para origem (Tx={tx}, Ty={ty}, Tz={tz})")
                self.cube_vertices = Translacao.realizar_translacao3D(self.cube_vertices, tx, ty, tz)
            
            self._log_message(f"2. Aplicar Escala (Sx={sx}, Sy={sy}, Sz={sz})")
            self.cube_vertices = Escala.realizar_escala3D(self.cube_vertices, sx, sy, sz) # Passa os pontos do cubo desenhado para a função de escala que retorna os novos pontos do cubo

            if tx or ty or tz:
                self._log_message(f"3. Transladar de volta (Tx={-tx}, Ty={-ty}, Tz={-tz})")
                self.cube_vertices = Translacao.realizar_translacao3D(self.cube_vertices, -tx, -ty, -tz)
        
        #Desenha o novo cubo
        self.redraw()
    
    def translacao(self, tx, ty, tz):
        if self.compose_transformations.get(): # Adiciona translacao na lista para montar matriz M composta
            self.compose_list.append(["Translacao", tx, ty, tz])
            self._log_message(f"Translação (Tx={tx}, Ty={ty}, Tz={tz}) adicionada.")
        else:
            # Passa os pontos do cubo desenhado para a função de translação que retorna os novos pontos do cubo
            self.cube_vertices = Translacao.realizar_translacao3D(self.cube_vertices, tx, ty, tz)
        
        #Desenha o novo cubo
        self.redraw()
    
    def rotacao(self, angle, rotate_type):
        if self.compose_transformations.get(): # Adiciona translacao na lista para montar matriz M composta
            self.compose_list.append([rotate_type, angle])
            self._log_message(f"'Rotação {rotate_type} ({angle}°)' adicionada.")
        else:
            tx, ty, tz = self.verificar_se_fora_da_orig() 

            if tx or ty or tz:
                self._log_message(f"\nCubo fora da origem:")
                self._log_message(f"1. Transladar para origem (Tx={tx}, Ty={ty}, Tz={tz})")
                self.cube_vertices = Translacao.realizar_translacao3D(self.cube_vertices, tx, ty, tz)
            
            self._log_message(f"2. Aplicar Rotação {rotate_type} (ang={angle})")
            self.cube_vertices = Rotacao.realizar_rotacao3D(self.cube_vertices, angle, rotate_type)

            if tx or ty or tz:
                self._log_message(f"3. Transladar de volta (Tx={-tx}, Ty={-ty}, Tz={-tz})")
                self.cube_vertices = Translacao.realizar_translacao3D(self.cube_vertices, -tx, -ty, -tz)
        #Desenha o novo cubo
        self.redraw()
    
    def reflexao(self, ref_type):
        if self.compose_transformations.get(): # Adiciona reflexao na lista para montar matriz M composta
            self.compose_list.append([ref_type])
            self._log_message(f"'Reflexão {ref_type}' adicionada.")
        else:
            self.cube_vertices = Reflexao.realizar_reflexao3D(self.cube_vertices, ref_type)
        
        #Desenha o novo cubo
        self.redraw()
    
    def cisalhamento(self, a, b, cis_type):
        if self.compose_transformations.get(): # Adiciona translacao na lista para montar matriz M composta
            self.compose_list.append(["Cisalhamento", a, b, cis_type])
            self._log_message(f"Cisalhamento {cis_type} (a={a}, b={b}) adicionado.")
        else:
            tx, ty, tz = self.verificar_se_fora_da_orig() 

            if tx or ty or tz:
                self._log_message(f"\nCubo fora da origem:")
                self._log_message(f"1. Transladar para origem (Tx={tx}, Ty={ty}, Tz={tz})")
                self.cube_vertices = Translacao.realizar_translacao3D(self.cube_vertices, tx, ty, tz)
            
            self._log_message(f"2. Aplicar {cis_type} (a={a}, b={b})")
            self.cube_vertices = Cisalhamento.realizar_cisalhamento3D(self.cube_vertices, a, b, cis_type)

            if tx or ty or tz:
                self._log_message(f"3. Transladar de volta (Tx={-tx}, Ty={-ty}, Tz={-tz})")
                self.cube_vertices = Translacao.realizar_translacao3D(self.cube_vertices, -tx, -ty, -tz)
        #Desenha o novo cubo
        self.redraw()
    
    def aplicar_matriz_composta(self):
        tx, ty, tz = self.verificar_se_fora_da_orig() 
        
        result = MatrizComposta.apply_composite_matrix(self.cube_vertices, self.compose_list, tx, ty, tz, log_callback=self._log_message)
        self.cube_vertices = result[0] #result[0] é o cubo transformado, a funcao tbm retorna a matriz "result[1]"

        # Impressao da Matriz M
        np.set_printoptions(precision=4, suppress=True)
        self._log_message(f"'\nMatriz M:\n {result[1]}")
        np.set_printoptions(precision=8, suppress=False)

        self.redraw()
    
    def resetar_lista_composicao(self):
        self.compose_list = []
    
    # --- Função para atualizar o terminal de mensagens ---
    def update_message_terminal(text_widget, message):
        text_widget.config(state="normal") # Habilita para escrita
        text_widget.insert(tk.END, message + "\n") # Adiciona a mensagem no final
        text_widget.see(tk.END) # Rola para o final para mostrar a nova mensagem
        text_widget.config(state="disabled") # Desabilita novamente para evitar edição pelo usuário

    def exibir_viewport_pixels(self):
        """
        Calcula e exibe as coordenadas de pixel do objeto em relação à tela do dispositivo
        no log principal. Abre uma janela de simulação MENOR que representa a tela do dispositivo
        e desenha a localização do canvas OpenGL e dos pontos do objeto dentro dela, mantendo a proporção.
        """
        self._log_message("Abrindo janela de simulação da Viewport (3D)...")

        # --- Parâmetros da Janela do Mundo (OpenGL gluOrtho2D) ---
        # glOrtho(-self.vp_width/2, self.vp_width/2, -self.vp_height/2, self.vp_height/2, -self.vp_Zaxis/2, self.vp_Zaxis/2)
        x_w_min = -self.vp_width / 2
        x_w_max = self.vp_width / 2
        y_w_min = -self.vp_height / 2
        y_w_max = self.vp_height / 2
        z_w_min = -self.vp_Zaxis / 2
        z_w_max = self.vp_Zaxis / 2

        # --- Parâmetros do seu Canvas OpenGL em Pixels (largura/altura atual) ---
        canvas_width_pixels = self.winfo_width()
        canvas_height_pixels = self.winfo_height()
        
        # --- Posição ABSOLUTA do Canvas OpenGL na Tela do Monitor ---
        ogl_canvas_x_on_screen = self.winfo_rootx() 
        ogl_canvas_y_on_screen = self.winfo_rooty() 

        # --- Criar a nova janela Tkinter (simula a tela do monitor) ---
        viewport_window = tk.Toplevel(self.master)
        viewport_window.title("Simulação Viewport (Pixels do Dispositivo)")
        
        screen_width_real = viewport_window.winfo_screenwidth()
        screen_height_real = viewport_window.winfo_screenheight()

        # --- CALCULAR ESCALA PARA A JANELA DE SIMULAÇÃO ---
        max_sim_width = 800
        max_sim_height = 600

        scale_factor = min(max_sim_width / screen_width_real, max_sim_height / screen_height_real)
        
        sim_window_width = int(screen_width_real * scale_factor)
        sim_window_height = int(screen_height_real * scale_factor)

        viewport_window.geometry(f"{sim_window_width}x{sim_window_height}+100+100")
        viewport_window.resizable(False, False)
        
        # --- Canvas para desenhar os elementos simulados (o "monitor") ---
        pixel_canvas = tk.Canvas(viewport_window, width=sim_window_width, height=sim_window_height, 
                                 bg="lightgray", bd=0, highlightbackground="gray") 
        pixel_canvas.pack(fill="both", expand=True)

        # --- Rótulo para exibir as coordenadas ---
        coords_label = tk.Label(pixel_canvas, text=f"Janela do Dispositivo: {screen_width_real} x {screen_height_real}\n", 
                                 justify=tk.LEFT, anchor="nw", bg="lightgray", font=("Consolas", 10))
        coords_label.place(x=10, y=10)

        # --- LOGAR as Coordenadas no Terminal Principal ---
        self._log_message("--- DETALHES DE MAPEAMENTO 3D ---")
        self._log_message(f"Resolução da Tela REAL:\n {screen_width_real}x{screen_height_real} pixels")
        self._log_message(f"Janela do Mundo (Orthographic):\n X[{x_w_min:.0f}, {x_w_max:.0f}], Y[{y_w_min:.0f}, {y_w_max:.0f}], Z[{z_w_min:.0f}, {z_w_max:.0f}]")
        self._log_message("--- INÍCIO DOS CÁLCULOS DOS VÉRTICES ---")

        # --- Desenhar o Retângulo VERDE (Canvas OpenGL) na simulação ---
        scaled_ogl_canvas_x = int(ogl_canvas_x_on_screen * scale_factor)
        scaled_ogl_canvas_y = int(ogl_canvas_y_on_screen * scale_factor)
        scaled_canvas_width = int(canvas_width_pixels * scale_factor)
        scaled_canvas_height = int(canvas_height_pixels * scale_factor)

        pixel_canvas.create_rectangle(scaled_ogl_canvas_x, scaled_ogl_canvas_y,
                                      scaled_ogl_canvas_x + scaled_canvas_width,
                                      scaled_ogl_canvas_y + scaled_canvas_height,
                                      outline="green", width=2) 
        pixel_canvas.create_text(scaled_ogl_canvas_x + 5, scaled_ogl_canvas_y + 5, anchor="nw",
                                  text=f"Canvas OpenGL\n({canvas_width_pixels}x{canvas_height_pixels})", 
                                  fill="darkgreen", font=("Arial", 7))

        log_coords_list = []
        
        # --- PREPARAR MATRIZES DE TRANSFORMAÇÃO PARA A SIMULAÇÃO ---
        proj_matrix = np.array(glGetDoublev(GL_PROJECTION_MATRIX))

        # Matriz ModelView
        # Inclui as rotações isométricas fixas e a rotação dinâmica da câmera
        mv_matrix = np.array(glGetDoublev(GL_MODELVIEW_MATRIX))

        # Matriz de rotação em X para compensar a rotação isométrica
        angle_correct_x = np.radians(35.36)
        cos_a_x, sin_a_x = np.cos(angle_correct_x), np.sin(angle_correct_x)

        counter_rotation_x_matrix = np.array([
            [1, 0, 0, 0],
            [0, cos_a_x, -sin_a_x, 0],
            [0, sin_a_x, cos_a_x, 0],
            [0, 0, 0, 1]
        ], dtype=np.float32)

        # Matriz MVP combinada
        mvp_matrix = counter_rotation_x_matrix @ mv_matrix
        #mvp_matrix = counter_rotation_y_matrix @ mvp_matrix
        mvp_matrix = proj_matrix @ mvp_matrix
        
        # Lista para armazenar os pontos 2D projetados para desenhar linhas/polígonos
        projected_points_2d = []

        # --- Iterar e Desenhar os Pontos (Vértices do Objeto) na simulação ---        
        for i, point_world in enumerate(self.cube_vertices):
            # point_world_homogeneous é um array numpy [x, y, z, 1]
            x_w, y_w, z_w = point_world[0], point_world[1], point_world[2]

            # 1. Aplicar Matriz Modelo-Visualização-Projeção
            point_clip = mvp_matrix @ point_world

            # 2. Perspectiva (transformar para Normalized Device Coordinates - NDC)
            ndc_x = point_clip[0] / point_clip[3]
            ndc_y = point_clip[1] / point_clip[3]
            ndc_z = point_clip[2] / point_clip[3] # NDC Z é importante para clipping e Z-buffering (embora não usado para desenho 2D aqui)

            # 3. Mapear NDC para Coordenadas de Pixel do Canvas OpenGL (Viewport Transform)
            # Formula: pixel = (NDC + 1) / 2 * dimension
            dc_x_canvas = ((ndc_x + 1) / 2) * canvas_width_pixels
            # Para Y, OpenGL tem Y para cima, Tkinter tem Y para baixo. Invertemos o Y NDC.
            dc_y_canvas = ((ndc_y + 1) / 2) * canvas_height_pixels 

            # 4. Mapeamento para Pixel da Tela do Dispositivo (absoluto na tela REAL)
            dc_x_device_real = int(ogl_canvas_x_on_screen + dc_x_canvas)
            dc_y_device_real = int(ogl_canvas_y_on_screen + dc_y_canvas)
            
            # 5. Escalar as Coordenadas do Dispositivo REAL para a Janela de SIMULAÇÃO
            scaled_dc_x_sim = int(dc_x_device_real * scale_factor)
            scaled_dc_y_sim = int(dc_y_device_real * scale_factor)

            projected_points_2d.append((scaled_dc_x_sim, scaled_dc_y_sim))

            # --- Desenhar o ponto no canvas simulado ---
            radius = 1 
            # Verifica se o ponto projetado está dentro dos limites da janela de simulação
            if 0 <= scaled_dc_x_sim < sim_window_width and 0 <= scaled_dc_y_sim < sim_window_height:
                pixel_canvas.create_oval(scaled_dc_x_sim - radius, scaled_dc_y_sim - radius, 
                                         scaled_dc_x_sim + radius, scaled_dc_y_sim + radius, 
                                         fill="purple", outline="white", width=1)

            # Logar para o terminal principal
            self._log_message(f"{i}: Mundo({x_w:.1f},{y_w:.1f},{z_w:.1f}) -> NDC({ndc_x:.2f},{ndc_y:.2f}) ->  DC({dc_x_device_real},{dc_y_device_real})")

        # --- Desenhar as arestas na simulação ---
        arestas = [
            (0, 1), (1, 2), (2, 3), (3, 0), # Face frontal
            (4, 5), (5, 6), (6, 7), (7, 4), # Face traseira
            (0, 4), (1, 5), (2, 6), (3, 7)  # Conectores
        ]

        for i, j in arestas:
            p1_sim = projected_points_2d[i]
            p2_sim = projected_points_2d[j]

            if p1_sim and p2_sim: # Desenha a linha apenas se ambos os pontos foram projetados
                pixel_canvas.create_line(p1_sim[0], p1_sim[1], p2_sim[0], p2_sim[1], 
                                          fill="blue", width=1)
            else:
                # Opcional: logar se uma aresta não foi totalmente desenhada
                pass # self._log_message(f"AVISO: Aresta entre {i} e {j} não desenhada (um ou ambos os pontos fora de visibilidade).")

        self._log_message("--- FIM DOS CÁLCULOS DOS VÉRTICES ---")
        self._log_message("Simulação Viewport (Coordenadas Dispositivo): Dados no log.")


def desenhar(tab4):
    # Frame esquerdo (Interface do usuário)
    frame_left = tk.Frame(tab4, width=200, height=600)
    frame_left.configure(background="#000C66")
    frame_left.pack(side=tk.LEFT, fill=tk.BOTH, expand=False)

    # Frame para o lado direito (openGL)
    frame_right = tk.Frame(tab4, width=800, height=600)
    frame_right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    # --- Criação do Text Widget para mensagens ---
    message_frame = tk.Frame(frame_left, bg="#000C66")
    message_frame.grid(row=20, column=0, columnspan=4, pady=10, padx=5, sticky="nsew") 
    
    frame_left.grid_rowconfigure(20, weight=1) # Faz a linha do terminal expandir verticalmente
    for i in range(4): # Configura todas as 4 colunas do frame_left para expandir
        frame_left.grid_columnconfigure(i, weight=1)

    message_text_widget = tk.Text(message_frame, height=8, width=25, wrap="word", 
                                  bg="#222222", fg="lightgreen", state="disabled",
                                  font=("Consolas", 8))
    message_text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    scrollbar = tk.Scrollbar(message_frame, command=message_text_widget.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    message_text_widget.config(yscrollcommand=scrollbar.set)
    # ---Fim da criação do widget ----

    # Criando objeto que renderiza o openGL
    ogl_frame = opengl3D(frame_right, width=800, height=600,
                         message_text_widget=message_text_widget)
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
     # Botão para desenhar cubo na origem (0,0,0)
    btn_draw_cube = tk.Button(frame_left, text="Desenhar", command=lambda: ogl_frame.criar_cubo(int(entry_cube.get())))
    btn_draw_cube.grid(row=1, column=2, pady=3, padx=2)
    # Botão para desenhar cubo fora da origem (tx=50, ty=50, tz=50)
    btn_draw_cube = tk.Button(frame_left, text="Des. fora", command=lambda: ogl_frame.criar_cubo(int(entry_cube.get()), 50, 50, 50))
    btn_draw_cube.grid(row=1, column=3, pady=3, padx=2)

    # --- TRANSFORMAÇÕES ---
    # Caixa de entrada para ESCALA (Sx, Sy, Sz)
    entry_Sx = ctk.CTkEntry(frame_left, placeholder_text="Sx", width=50)
    entry_Sx.grid(row=2, column=0, pady=5, padx=5)

    entry_Sy = ctk.CTkEntry(frame_left, placeholder_text="Sy", width=50)
    entry_Sy.grid(row=2, column=1, pady=5, padx=5)

    entry_Sz = ctk.CTkEntry(frame_left, placeholder_text="Sz", width=50)
    entry_Sz.grid(row=2, column=2, pady=5, padx=5)

     # Botão para aplicar escala
    btn_scale = tk.Button(frame_left, text="Scale", command=lambda: ogl_frame.escala(float(entry_Sx.get()), float(entry_Sy.get()), float(entry_Sz.get())))
    btn_scale.grid(row=2, column=3, pady=3, padx=2)

    # Caixa de entrada para TRANSLAÇÃO
    entry_Tx = ctk.CTkEntry(frame_left, placeholder_text="Tx", width=50)
    entry_Tx.grid(row=3, column=0, pady=5, padx=5)

    entry_Ty = ctk.CTkEntry(frame_left, placeholder_text="Ty", width=50)
    entry_Ty.grid(row=3, column=1, pady=5, padx=5)

    entry_Tz = ctk.CTkEntry(frame_left, placeholder_text="Tz", width=50)
    entry_Tz.grid(row=3, column=2, pady=5, padx=5)

     # Botão para aplicar Translação
    btn_translate = tk.Button(frame_left, text="Transl.", command=lambda: ogl_frame.translacao(float(entry_Tx.get()), int(entry_Ty.get()), int(entry_Tz.get())))
    btn_translate.grid(row=3, column=3, pady=3, padx=2)

    # Caixa de entrada para ROTAÇÃO
    entry_angle = ctk.CTkEntry(frame_left, placeholder_text="angle", width=50)
    entry_angle.grid(row=4, column=0, pady=5, padx=5)

    # Botão para aplicar Rotação Rx
    btn_Rx = tk.Button(frame_left, text="Rx", command=lambda: ogl_frame.rotacao(float(entry_angle.get()), "Rx"))
    btn_Rx.grid(row=4, column=1, pady=3, padx=2)

    # Botão para aplicar Rotação Ry
    btn_Ry = tk.Button(frame_left, text="Ry", command=lambda: ogl_frame.rotacao(float(entry_angle.get()), "Ry"))
    btn_Ry.grid(row=4, column=2, pady=3, padx=2)

    # Botão para aplicar Rotação
    btn_Rz = tk.Button(frame_left, text="Rz", command=lambda: ogl_frame.rotacao(float(entry_angle.get()), "Rz"))
    btn_Rz.grid(row=4, column=3, pady=3, padx=2)

    # --- REFLEXÃO ---
    btn_RefXY = tk.Button(frame_left, text="RefXY", command=lambda: ogl_frame.reflexao("RefXY"))
    btn_RefXY.grid(row=5, column=0, pady=3, padx=2)

    btn_RefYZ = tk.Button(frame_left, text="RefYZ", command=lambda: ogl_frame.reflexao("RefYZ"))
    btn_RefYZ.grid(row=5, column=1, pady=3, padx=2)
    
    btn_RefXZ = tk.Button(frame_left, text="RefXZ", command=lambda: ogl_frame.reflexao("RefXZ"))
    btn_RefXZ.grid(row=5, column=2, pady=3, padx=2)

    btn_RefOrig = tk.Button(frame_left, text="RefOrig", command=lambda: ogl_frame.reflexao("RefOrig"))
    btn_RefOrig.grid(row=5, column=3, pady=3, padx=2)

    # --- CISALHAMENTO ---
    # Caixa de entrada para Cisalhamento
    entry_CisA = ctk.CTkEntry(frame_left, placeholder_text="a", width=50)
    entry_CisA.grid(row=6, column=0, pady=5, padx=5)

    entry_CisB = ctk.CTkEntry(frame_left, placeholder_text="b", width=50)
    entry_CisB.grid(row=6, column=1, pady=5, padx=5)

    # Botão para aplicar Cisalhamento
    btn_cisXY = tk.Button(frame_left, text="Cisalhar XY por Z", command=lambda: ogl_frame.cisalhamento(float(entry_CisA.get()), float(entry_CisB.get()), "CisXY"))
    btn_cisXY.grid(row=6, column=2, columnspan=2, pady=3, padx=2)

    btn_cisYZ = tk.Button(frame_left, text="Cisalhar YZ por X", command=lambda: ogl_frame.cisalhamento(float(entry_CisA.get()), float(entry_CisB.get()), "CisYZ"))
    btn_cisYZ.grid(row=7, column=2, columnspan=2, pady=3, padx=2)
    
    btn_cisXZ = tk.Button(frame_left, text="Cisalhar XZ por Y", command=lambda: ogl_frame.cisalhamento(float(entry_CisA.get()), float(entry_CisB.get()), "CisXZ"))
    btn_cisXZ.grid(row=8, column=2, columnspan=2, pady=3, padx=2)

    # --- CAIXA DE SELEÇÃO PARA COMPOR TRANSFORMAÇÕES ---
    check_btn_compor = ctk.CTkCheckBox(frame_left, text="Compor Transformações?",
                                        variable=ogl_frame.compose_transformations, # Linka com a Boolean da classe
                                        onvalue=True, # Valor quando marcado
                                        offvalue=False, # Valor quando desmarcado
                                        text_color= "white") 
    check_btn_compor.grid(row=10, columnspan=4, pady=3, padx=2, sticky="w")

    # Cria o botão para aplicar Composição
    btn_compose = tk.Button(frame_left, text="Aplicar Transf. Composta", command=lambda: ogl_frame.aplicar_matriz_composta())
    btn_compose.grid(row=11, column=0, columnspan=4, pady=3, padx=2, sticky="w") # Posiciona o botão

    # Resetar lista de composicao
    btn_reset_compose = tk.Button(frame_left, text="Resetar comp.", command=lambda: ogl_frame.resetar_lista_composicao())
    btn_reset_compose.grid(row=11, column=3, pady=3, padx=2, sticky="w") # Posiciona o botão

    # --- CÂMERA ---
    # Cria o botão "Girar 30°"
    btn_rotate_30 = tk.Button(frame_left, text="Girar 30°", command=lambda: ogl_frame.rotate_by_angle(30))
    btn_rotate_30.grid(row=12, column=2, pady=3, padx=2) # Posiciona o botão

    # Cria o botão para resetar câmera
    btn_reset_cam = tk.Button(frame_left, text="Resetar câmera", command=lambda: ogl_frame.reset_camera())
    btn_reset_cam.grid(row=12, column=3, pady=3, padx=2) # Posiciona o botão

    # Botão para exibir viewport
    btn_show_viewport = tk.Button(frame_left, text="Viewport", 
                                  command=lambda: ogl_frame.exibir_viewport_pixels())
    btn_show_viewport.grid(row=13, column=0, columnspan=2, pady=5, padx=5, sticky="w")
    
