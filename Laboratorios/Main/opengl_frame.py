'''
    Classe que renderiza o OpenGl na tela
'''

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import numpy as np
from pyopengltk import OpenGLFrame
import tkinter as tk
import customtkinter as ctk

from Transformações import Rotacao
from Transformações import Translacao
from Transformações import Escala
from Transformações import Cisalhamento
from Transformações import Reflexao
from Transformações import ReflexaoQualquer
from Transformações import MatrizComposta
from Recorte import Cohen_sutherland

class AppOgl(OpenGLFrame):
    def __init__(self, master=None, message_text_widget=None, **kw):
        self.message_text_widget = message_text_widget # Salva a referência ao widget
        super().__init__(master, **kw)
        self.root_window = master.winfo_toplevel() # Isso obtém a janela Toplevel à qual o frame_right pertence

        self.points = []  # Lista de pontos para armazenar o desenho (para DDA)
        self.square_points_list = [] # Lista de vértices do quadrado atual
        self.compose_transformations = tk.BooleanVar(value=False)
        self.compose_list = [] # Lista que armazena as tranformações a serem aplicadas

        # Teste para log de mensagem
        if self.message_text_widget:
            self._log_message("Sistema de visualização 2D iniciado.")
       
    def initgl(self):
        """Inicializa o ambiente OpenGL com configurações genéricas."""
        glClearColor(0.7, 0.7, 0.7, 0.0) # Cor de fundo do OpenGL
        self.vp_width = self.winfo_reqwidth()
        self.vp_height = self.winfo_reqheight()
        print("width x height: ", self.vp_width, "x", self.vp_height)
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
    
    # --- Função para atualizar o terminal de mensagens ---
    def update_message_terminal(text_widget, message):
        text_widget.config(state="normal") # Habilita para escrita
        text_widget.insert(tk.END, message + "\n") # Adiciona a mensagem no final
        text_widget.see(tk.END) # Rola para o final para mostrar a nova mensagem
        text_widget.config(state="disabled") # Desabilita novamente para evitar edição pelo usuário
    
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
            #print(point[0], point[1])
            glVertex2f(point[0], point[1])
        
        for point in self.square_points_list: # somente vértices
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
        
        self.points.append((x, y))
        for k in range(int(steps)):
            x += xIncrement
            y += yIncrement
            self.points.append((x, y))
            #self.points.append(round(x), round(y))
        
        
    #Método para desenhar quadrado na origem, usa o método DDA
    def square_points(self, size):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT) # Quando desenhar novo quadrado, limpa a tela antes
        self.points = []
        self.square_points_list = []

        x = round(size)/2
        y = round(size)/2
        self.DDA(0, 0, size, 0) # Ex: Desenha reta do ponto (0, 0) a (50, 0)
        self.DDA(size, 0, size, size)
        self.DDA(size, size, 0, size)
        self.DDA(0, size, 0, 0)

        #Lista para armazenar os vértices do quadrado (x, y)
        self.square_points_list = [(0, 0), (0, size), (size, size), (size, 0)]

        self.redraw()

        return (0, 0), (0, size), (size, size), (size, 0)
    
    #Método para desenhar quadrado após a transformação
    def draw_square(self, point1, point2, point3, point4):
        # Antes de passar para algoritmo da reta, verificar recorte de cohen e passar novos pontos já recortados

        # Lista de pares de pontos que formam o quadrado
        segments = [
            (point1, point2),
            (point2, point3),
            (point3, point4),
            (point4, point1)
        ]

        # Itera sobre cada segmento do quadrado
        for p_start, p_end in segments:
            self._log_message("-" * 30) # Imprimir cada passo de recorte separado
            self._log_message(f"Processando segmento: \n({p_start[0]:.1f}, {p_start[1]:.1f}) -> ({p_end[0]:.1f}, {p_end[1]:.1f})")
            
            # Chama a função de recorte para o segmento atual
            # Passa os pontos do segmento e as coordenadas da janela
            recorte_result = Cohen_sutherland.aplicar_recorte_cohen(
                p_start, p_end, 
                -self.vp_width/2, self.vp_width/2, -self.vp_height/2, self.vp_height/2,
                logCallback = self._log_message
            )

            # Verifica o resultado do recorte
            if recorte_result is not None:
                # Se a linha não foi rejeitada (retornou pontos válidos)
                final_p_start, final_p_end = recorte_result
                # Chama o algoritmo DDA com os novos pontos recortados
                self.DDA(final_p_start[0], final_p_start[1], final_p_end[0], final_p_end[1])

                self._log_message(f"Segmento recortado:\n ({final_p_start[0]:.1f}, {final_p_start[1]:.1f}) -> ({final_p_end[0]:.1f}, {final_p_end[1]:.1f})")
                

        self.redraw()

    #Transformações no Quadrado
    def escala(self, sx, sy):
        if self.compose_transformations.get(): # Adiciona escala a lista para montar matriz M composta
            self.compose_list.append(["Escala", sx, sy])
            self._log_message(f"'Escala (Sx={sx}, Sy={sy})' adicionada.")
        else:
            tx, ty = self.verificar_se_fora_da_orig() 

            if tx or ty:
                self._log_message(f"\nObjeto fora da origem:")
                self._log_message(f"1. Transladar para origem (Tx={tx}, Ty={ty})")
                self.square_points_list = Translacao.realizar_translacao(self.square_points_list, tx, ty)

            self._log_message(f"2. Aplicar Escala (Sx={sx}, Sy={sy})")
            self.square_points_list = Escala.realizar_escala(self.square_points_list, sx, sy)

            if tx or ty:
                self._log_message(f"3. Transladar de volta (Tx={-tx}, Ty={-ty})")
                self.square_points_list = Translacao.realizar_translacao(self.square_points_list, -tx, -ty)
        #Remove o quadrado anterior
        self.points = [] 

        #Desenha o novo quadrado
        self.draw_square(*self.square_points_list) #passa os parametros da função ao desempacotar a lista (p1, p2, etc.)

    def translacao(self, tx, ty):
        if self.compose_transformations.get(): # Adiciona escala a lista para montar matriz M composta
            self.compose_list.append(["Translacao", tx, ty])
            self._log_message(f"'Translação (Tx={tx}, Ty={ty})' adicionada.")
        else:
            self.square_points_list = Translacao.realizar_translacao(self.square_points_list, tx, ty)

        #Remove o quadrado anterior
        self.points = []

        #Desenha o novo quadrado transladado
        self.draw_square(*self.square_points_list)
    
    def rotacao(self, angle):
        if self.compose_transformations.get(): # Adiciona rotacao a lista para montar matriz M composta
            self.compose_list.append(["Rotacao", angle])
            self._log_message(f"Rotacao (ang={angle}º) adicionada.")
        else:
            tx, ty = self.verificar_se_fora_da_orig() 

            if tx or ty:
                self._log_message(f"\nObjeto fora da origem:")
                self._log_message(f"1. Transladar para origem (Tx={tx}, Ty={ty})")
                self.square_points_list = Translacao.realizar_translacao(self.square_points_list, tx, ty)

            self._log_message(f"2. Aplicar Rotacao (ang={angle}º)")
            self.square_points_list = Rotacao.realizar_rotacao(self.square_points_list, angle)

            if tx or ty:
                self._log_message(f"3. Transladar de volta (Tx={-tx}, Ty={-ty})")
                self.square_points_list = Translacao.realizar_translacao(self.square_points_list, -tx, -ty)

        #Remove o quadrado anterior
        self.points = []

        #Desenha o novo quadrado rotacionado
        self.draw_square(*self.square_points_list)
    
    def cisalhamento(self, a, b):
        if self.compose_transformations.get(): # Adiciona cisalhamento a lista para montar matriz M composta
            self.compose_list.append(["Cisalhamento", a, b])
            self._log_message(f"Cisalhamento (a={a}, b={b}) adicionada.")
        else:
            tx, ty = self.verificar_se_fora_da_orig() 

            if tx or ty:
                self._log_message(f"\nObjeto fora da origem:")
                self._log_message(f"1. Transladar para origem (Tx={tx}, Ty={ty})")
                self.square_points_list = Translacao.realizar_translacao(self.square_points_list, tx, ty)
            
            self.square_points_list = Cisalhamento.realizar_cisalhamento(self.square_points_list, a, b)

            if tx or ty:
                self._log_message(f"3. Transladar de volta (Tx={-tx}, Ty={-ty})")
                self.square_points_list = Translacao.realizar_translacao(self.square_points_list, -tx, -ty)

        #Remove o quadrado anterior
        self.points = []

        #Desenha o novo quadrado rotacionado
        self.draw_square(*self.square_points_list)
    
    def reflexaoX(self):
        if self.compose_transformations.get(): # Adiciona RefX a lista para montar matriz M composta
            self.compose_list.append(["RefX"])
            self._log_message(f"Reflexão em X adicionada.")
        else:
            self.square_points_list = Reflexao.realizar_reflexaoX(self.square_points_list)

        #Remove o quadrado anterior
        self.points = []

        #Desenha o novo quadrado rotacionado
        self.draw_square(*self.square_points_list)
    
    def reflexaoY(self):
        if self.compose_transformations.get(): # Adiciona RefX a lista para montar matriz M composta
            self.compose_list.append(["RefY"])
            self._log_message(f"Reflexão em Y adicionada.")
        else:
            self.square_points_list = Reflexao.realizar_reflexaoY(self.square_points_list)

        #Remove o quadrado anterior
        self.points = []

        #Desenha o novo quadrado rotacionado
        self.draw_square(*self.square_points_list)

    def reflexaoOrigem(self):
        if self.compose_transformations.get(): # Adiciona RefX a lista para montar matriz M composta
            self.compose_list.append(["RefOrig"])
            self._log_message(f"Reflexão Origem adicionada.")
        else:
            self.square_points_list = Reflexao.realizar_reflexaoOrigem(self.square_points_list)

        #Remove o quadrado anterior
        self.points = []

        #Desenha o novo quadrado rotacionado
        self.draw_square(*self.square_points_list)

    def reflexao45(self):
        if self.compose_transformations.get(): # Adiciona RefX a lista para montar matriz M composta
            self.compose_list.append(["Ref45"])
            self._log_message(f"Reflexão em 45º adicionada.")
        else:
            self.square_points_list = Reflexao.realizar_reflexao45(self.square_points_list)

        #Remove o quadrado anterior
        self.points = []

        #Desenha o novo quadrado rotacionado
        self.draw_square(*self.square_points_list)
    
    def reflexaoQualquer(self, m, b):
        if self.compose_transformations.get(): # Adiciona RefX a lista para montar matriz M composta
            self.compose_list.append(["RefAny", m, b])
            self._log_message(f"Reflexão reta (m={m}, b={b}) adicionada.")
        else:
            self.square_points_list = ReflexaoQualquer.realizar_reflexao_qualquer(self.square_points_list, m, b)

        #Remove o quadrado anterior
        self.points = []

        #Desenha o novo quadrado rotacionado
        self.draw_square(*self.square_points_list)
    
    def aplicar_matriz_composta2D(self):
        tx, ty = self.verificar_se_fora_da_orig() 
        
        result = MatrizComposta.apply_composite_matrix2D(self.square_points_list, self.compose_list, tx, ty, log_callback=self._log_message)
        self.square_points_list = result[0] #result[0] é o cubo transformado, a funcao tbm retorna a matriz "result[1]"

        # Impressao da Matriz M
        np.set_printoptions(precision=4, suppress=True)
        self._log_message(f"'\nMatriz M:\n {result[1]}")
        np.set_printoptions(precision=8, suppress=False)

        #Remove o quadrado anterior
        self.points = [] 
        #Desenha o novo quadrado
        self.draw_square(*self.square_points_list)
        self.redraw()
    
    # Função para verificar se está fora da origem:
    def verificar_se_fora_da_orig(self):
        tx, ty = 0, 0
        x = self.points[0][0]
        y = self.points[0][1]

        if x > 0: # ponto X fora da origem
            tx = -x 
        elif x < 0: # ponto X fora da origem (lado negativo)
            tx = -x # Sempre o negativo do valor atual para ir para 0
                             # Se x é -50, tx = -(-50) = 50
        
        if y > 0: # ponto Y fora da origem
            ty = -y
        elif y < 0: # ponto Y fora da origem (lado negativo)
            ty = -y
        
        return tx, ty
    
    def resetar_lista_composicao(self):
        self.compose_list = []
    
    def exibir_viewport_pixels(self):
        """
        Calcula e exibe as coordenadas de pixel dos vértices do cubo em relação à tela do dispositivo
        no log principal. Abre uma janela de simulação MENOR que representa a tela do dispositivo
        e desenha a localização do canvas OpenGL e dos pontos do objeto dentro dela, mantendo a proporção.
        """
        self._log_message("Abrindo janela de simulação da Viewport...")

        # --- Parâmetros da Janela do Mundo (OpenGL gluOrtho2D) ---
        x_w_min = -self.vp_width / 2
        x_w_max = self.vp_width / 2
        y_w_min = -self.vp_height / 2
        y_w_max = self.vp_height / 2

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
        # Definimos um tamanho MÁXIMO para a janela de simulação, por exemplo, 800 pixels de largura
        max_sim_width = 800
        max_sim_height = 600 # Para telas muito largas/altas

        # Calcula o fator de escala para manter a proporção da tela real
        scale_factor = min(max_sim_width / screen_width_real, max_sim_height / screen_height_real)
        
        sim_window_width = int(screen_width_real * scale_factor)
        sim_window_height = int(screen_height_real * scale_factor)

        viewport_window.geometry(f"{sim_window_width}x{sim_window_height}+100+100") # Posição inicial da janela de simulação
        viewport_window.resizable(False, False) # Janela de simulação não redimensionável
        
        # --- Canvas para desenhar os elementos simulados (o "monitor") ---
        pixel_canvas = tk.Canvas(viewport_window, width=sim_window_width, height=sim_window_height, 
                                 bg="lightgray", bd=0, highlightbackground="gray") 
        pixel_canvas.pack(fill="both", expand=True)

        # --- Rótulo para exibir as coordenadas (fixo no topo do Canvas, sem background branco) ---
        # Posicionamos o label fixo no topo-esquerda do canvas para não interferir nos desenhos
        coords_label = tk.Label(pixel_canvas, text=f"Janela do Dispositivo: {screen_width_real} x {screen_height_real}\n", 
                                justify=tk.LEFT, anchor="nw", bg="lightgray", font=("Consolas", 10))
        coords_label.place(x=10, y=10) # Posição absoluta dentro do pixel_canvas

        # --- LOGAR as Coordenadas no Terminal Principal (como antes) ---
        self._log_message("--- DETALHES DE MAEPEAMENTO ---")
        self._log_message(f"Resolução da Tela REAL:\n {screen_width_real}x{screen_height_real} pixels")
        self._log_message(f"Janela do Mundo (OpenGL gluOrtho2D):\n X[{x_w_min:.0f}, {x_w_max:.0f}], Y[{y_w_min:.0f}, {y_w_max:.0f}]")
        self._log_message("--- INÍCIO DOS CÁLCULOS DOS VÉRTICES ---")

        # --- Desenhar o Retângulo VERDE (Canvas OpenGL) na simulação ---
        # As coordenadas do canvas OpenGL na tela real são escaladas para a janela de simulação
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
                                 fill="darkgreen", font=("Arial", 7)) # Fonte menor para caber

        log_coords_list = [] # Lista para acumular as coordenadas para o Label

        log_coords_list.append(f"Vértice Mundo (X,Y) -> Dispositivo (X,Y)")
        
        # --- Iterar e Desenhar os Pontos (Vértices do Objeto) na simulação ---        
        for i, point_world in enumerate(self.points):
            if len(point_world) < 2:
                self._log_message(f"AVISO: Ponto {i} em self.points não tem coordenadas X e Y suficientes: {point_world}")
                continue

            x_w, y_w = point_world[0], point_world[1] 

            # --- 1. Mapeamento para Pixel do Canvas OpenGL (dentro do próprio canvas) ---
            dc_x_canvas = ((x_w - x_w_min) * canvas_width_pixels) / (x_w_max - x_w_min)
            dc_y_opengl_up = ((y_w - y_w_min) * canvas_height_pixels) / (y_w_max - y_w_min)
            dc_y_canvas_inverted = canvas_height_pixels - dc_y_opengl_up 

            # --- 2. Mapeamento para Pixel da Tela do Dispositivo (absoluto na tela REAL) ---
            dc_x_device_real = int(ogl_canvas_x_on_screen + dc_x_canvas)
            dc_y_device_real = int(ogl_canvas_y_on_screen + dc_y_canvas_inverted)
            
            # --- 3. Escalar as Coordenadas do Dispositivo REAL para a Janela de SIMULAÇÃO ---
            scaled_dc_x_sim = int(dc_x_device_real * scale_factor)
            scaled_dc_y_sim = int(dc_y_device_real * scale_factor)

            # --- Desenhar o ponto no canvas simulado ---
            radius = 3 # Raio menor para pontos
            if 0 <= scaled_dc_x_sim < sim_window_width and 0 <= scaled_dc_y_sim < sim_window_height:
                pixel_canvas.create_oval(scaled_dc_x_sim - radius, scaled_dc_y_sim - radius, 
                                        scaled_dc_x_sim + radius, scaled_dc_y_sim + radius, 
                                        fill="purple", outline="white", width=1)
            else:
                self._log_message(f"AVISO: Vértice {i} ({x_w:.1f},{y_w:.1f}) está fora da tela REAL em pixels: ({dc_x_device_real},{dc_y_device_real})")

            # Logar para o terminal principal (como antes)
            self._log_message(f"{i}: ({x_w:.1f},{y_w:.1f}) -> DC({dc_x_device_real},{dc_y_device_real})")

        self._log_message("--- FIM DOS CÁLCULOS DOS VÉRTICES ---")
        self._log_message("Simulação Viewport (Coordenadas Dispositivo): Dados no log.")

def desenhar(tab1):
     # Frame para o lado esquerdo
    frame_left = tk.Frame(tab1, width=200, height=600)
    frame_left.configure(background="#000C66")
    frame_left.pack(side=tk.LEFT, fill=tk.BOTH, expand=False)

    # Frame para o lado direito (openGL)
    frame_right = tk.Frame(tab1, width=800, height=600)
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
    
    # Adicionar o frame OpenGL ao lado direito
    ogl_frame = AppOgl(frame_right, width=800, height=600,
                        message_text_widget=message_text_widget)
    ogl_frame.pack(fill=tk.BOTH, expand=True)  # Definindo expand=False para manter o tamanho fixo

    # Inserir tamanho da janela mundo
    entry_width = ctk.CTkEntry(frame_left, placeholder_text="Largura", width=50)
    entry_width.grid(row=0, column=0, pady=1, padx=1)

    entry_height = ctk.CTkEntry(frame_left, placeholder_text="Altura", width=50)
    entry_height.grid(row=0, column=1, pady=1, padx=1)

    # Botão para definir janela mundo
    btn_janela_mundo = tk.Button(frame_left, text="Def. Janela\nMundo", command=lambda: ogl_frame.definir_janela_mundo(int(entry_width.get()), int(entry_height.get())))
    btn_janela_mundo.grid(row=0, column=2, pady=1, padx=1)
    
    # Caixa de entrada para o tamanho do quadrado
    entry_tamanho = ctk.CTkEntry(frame_left, placeholder_text="size", height=10, width=40)
    entry_tamanho.grid(row=1, column=0, pady=1, padx=1)
    
    # Botão para desenhar um quadrado, chama a função desejada ao apertar botão(command=funcao_executada)
    btn_desenhar_quadrado = tk.Button(frame_left, text="Desenhar\nQuadrado", command=lambda: ogl_frame.square_points(int(entry_tamanho.get())))
    btn_desenhar_quadrado.grid(row=1, column=1, pady=1, padx=1)

    # Caixa de entrada para Fator de escala Sx
    entry_sx = ctk.CTkEntry(frame_left, placeholder_text="sx", height=10, width=40)
    entry_sx.grid(row=2, column=0, pady=1, padx=1)

    # Caixa de entrada para Fator de escala Sy
    entry_sy = ctk.CTkEntry(frame_left, placeholder_text="sy", height=10, width=40)
    entry_sy.grid(row=2, column=1, pady=1, padx=1)
    
    # Botão para Escala
    btn_scale = tk.Button(frame_left, text="Aplicar\nEscala", command=lambda: ogl_frame.escala(float(entry_sx.get()), float(entry_sy.get()))) #Converter para int sempre que chamar a função
    btn_scale.grid(row=2, column=2, pady=1, padx=1)

    # Caixa de entrada para Translação Tx
    entry_tx = ctk.CTkEntry(frame_left, placeholder_text="Tx", height=10, width=40)
    entry_tx.grid(row=3, column=0, pady=1, padx=1)

    # Caixa de entrada para Translação Ty
    entry_ty = ctk.CTkEntry(frame_left, placeholder_text="Ty", height=10, width=40)
    entry_ty.grid(row=3, column=1, pady=1, padx=1)

    # Botão para Translação
    btn_translate = tk.Button(frame_left, text="Aplicar\nTranslação", command=lambda: ogl_frame.translacao(int(entry_tx.get()), int(entry_ty.get())))
    btn_translate.grid(row=3, column=2, pady=1, padx=1)

    # Caixa de entrada para ângulo de Rotação
    entry_rot = ctk.CTkEntry(frame_left, placeholder_text="ang", height=10, width=40)
    entry_rot.grid(row=4, column=0, pady=1, padx=1)

    # Botão para Rotação
    btn_translate = tk.Button(frame_left, text="Aplicar\nRotação", command=lambda: ogl_frame.rotacao(int(entry_rot.get())))
    btn_translate.grid(row=4, column=1, pady=1, padx=1)

    # Caixa de entrada para Fator A de cisalhamento
    entry_a = ctk.CTkEntry(frame_left, placeholder_text="a", height=10, width=40)
    entry_a.grid(row=5, column=0, pady=1, padx=1)

    # Caixa de entrada para Fator B de cisalhamento
    entry_b = ctk.CTkEntry(frame_left, placeholder_text="b", height=10, width=40)
    entry_b.grid(row=5, column=1, pady=1, padx=1)

    # Botão para Cisalhamento
    btn_cis = tk.Button(frame_left, text="Aplicar\nCisalhamento", command=lambda: ogl_frame.cisalhamento(int(entry_a.get()), int(entry_b.get())))
    btn_cis.grid(row=5, column=2, pady=1, padx=1)

    # Caixa de entrada para M da Reta da Reflexão Qualquer
    entry_m = ctk.CTkEntry(frame_left, placeholder_text="m", height=10, width=40)
    entry_m.grid(row=6, column=0, pady=1, padx=1)

    # Caixa de entrada para B da Reta da Reflexão Qualquer
    entry_b_reta = ctk.CTkEntry(frame_left, placeholder_text="b", height=10, width=40)
    entry_b_reta.grid(row=6, column=1, pady=1, padx=1)
    
    # Botão para Reflexão Qualquer
    btn_ref_qualquer = tk.Button(frame_left, text="Aplicar Ref.\nQualquer", command=lambda: ogl_frame.reflexaoQualquer(float(entry_m.get()), float(entry_b_reta.get())))
    btn_ref_qualquer.grid(row=6, column=2, pady=1, padx=1)

    # Botão para Reflexão em X
    btn_refx = tk.Button(frame_left, text="Ref X", command=lambda: ogl_frame.reflexaoX())
    btn_refx.grid(row=7, column=0, pady=1, padx=1)

    # Botão para Reflexão em Y
    btn_refy = tk.Button(frame_left, text="Ref Y", command=lambda: ogl_frame.reflexaoY())
    btn_refy.grid(row=7, column=1, pady=1, padx=1)

    # Botão para Reflexão na Origem
    btn_ref_orig = tk.Button(frame_left, text="Ref Origem", command=lambda: ogl_frame.reflexaoOrigem())
    btn_ref_orig.grid(row=7, column=2, pady=1, padx=1)

    # Botão para Reflexão na Reta de 45 graus
    btn_ref45 = tk.Button(frame_left, text="Ref Reta 45", command=lambda: ogl_frame.reflexao45())
    btn_ref45.grid(row=8, column=0, pady=1, padx=1)

    # --- CAIXA DE SELEÇÃO PARA COMPOR TRANSFORMAÇÕES ---
    check_btn_compor = ctk.CTkCheckBox(frame_left, text="Compor Transformações?",
                                        variable=ogl_frame.compose_transformations, # Linka com a Boolean da classe
                                        onvalue=True, # Valor quando marcado
                                        offvalue=False, # Valor quando desmarcado
                                        text_color= "white") 
    check_btn_compor.grid(row=9, columnspan=3, pady=3, padx=2, sticky="w")

    # Cria o botão para aplicar Composição
    btn_compose = tk.Button(frame_left, text="Aplicar Transf. Composta", command=lambda: ogl_frame.aplicar_matriz_composta2D())
    btn_compose.grid(row=10, column=0, columnspan=2, pady=3, padx=2, sticky="w") # Posiciona o botão

    # Resetar lista de composicao
    btn_reset_compose = tk.Button(frame_left, text="Resetar comp.", command=lambda: ogl_frame.resetar_lista_composicao())
    btn_reset_compose.grid(row=10, column=2, pady=3, padx=2, sticky="w") # Posiciona o botão

    # Botão para Limpar objetos desenhados
    btn_limpar = tk.Button(frame_left, text="Limpar", command=lambda: ogl_frame.limpar())
    btn_limpar.grid(row=11, column=2, pady=1, padx=1)

    # Botão para exibir viewport
    btn_show_viewport = tk.Button(frame_left, text="Exibir Viewport", 
                                  command=lambda: ogl_frame.exibir_viewport_pixels())
    btn_show_viewport.grid(row=11, column=0, columnspan=2, pady=5, padx=5, sticky="w")