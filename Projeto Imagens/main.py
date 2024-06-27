import tkinter as tk
from tkinter import ttk, filedialog
import customtkinter as ctk
from PIL import Image, ImageTk
import imageio
import numpy as np
import Filtros
import Transformacoes
import Equalizacao
import Operacoes

global entry_A, entry_Y


def open_image():
    file_path = filedialog.askopenfilename(filetypes=[("PGM Files", "*.pgm")])
    if file_path:
        # Carregar a imagem PGM usando imageio
        global imagem
        imagem = imageio.imread(file_path)
        
        global original_image
        # Mostrar na janela
        original_image = Image.open(file_path)
        display_image(original_image, imagem_original)

        # Obter a largura (número de colunas) e altura (número de linhas) da imagem
        img_height, img_width = imagem.shape
        print(img_height, " x ", img_width)

def display_image(image, label):
    image.thumbnail((300, 300))  # Reduzir o tamanho para caber na interface
    tk_image = ImageTk.PhotoImage(image)
    label.config(image=tk_image)
    label.image = tk_image

def aplicar_filtro(matriz):
        # Obter valores da matriz de convolução
        lista = []
        for i in range(3):
            linha = []
            for j in range(3):
                try:
                    valor = float(matriz[i][j].get())
                except ValueError:
                    # Se não for possível converter para float, definir como 0
                    valor = 0.0
                linha.append(valor)
            lista.append(linha)
        # Converter a matriz em um numpy array
        matriz_convolucao = np.array(lista)
        
        filtro_selecionado = filtro_val.get()
        if filtro_selecionado == "Filtro da mediana":
            imagem_filtrada = Filtros.filtro_mediana(imagem)
        elif filtro_selecionado == "Filtro da Média":
            imagem_filtrada = Filtros.filtro_media(imagem)
        elif filtro_selecionado == "Operador de Prewitt":
            imagem_filtrada = Filtros.operador_prewitt(imagem)
        elif filtro_selecionado == "Operador de Sobel":
            imagem_filtrada = Filtros.operador_sobel(imagem)
        elif filtro_selecionado == "Operador de Roberts":
            imagem_filtrada = Filtros.operador_roberts(imagem)
        elif filtro_selecionado == "Operador de Roberts cruzado":
            imagem_filtrada = Filtros.operador_roberts_cruzado(imagem)
        elif filtro_selecionado == "Filtragem Alto Reforço(Hight-Boost)":
            A = float(entry_A.get()) if entry_A.get() else 1.1
            imagem_filtrada = Filtros.filtragem_alto_reforco(imagem, A)
        elif filtro_selecionado == "Negativo da Imagem":
            imagem_filtrada = Transformacoes.negativo_da_imagem(imagem)
        elif filtro_selecionado == "Transformação Logaritmo":
            A = float(entry_A.get()) if entry_A.get() else 10
            imagem_filtrada = Transformacoes.logaritmo(imagem, A)
        elif filtro_selecionado == "Transformação Gamma":
            C = float(entry_A.get()) if entry_A.get() else 1
            Y = float(entry_Y.get()) if entry_Y.get() else 1
            imagem_filtrada = Transformacoes.gamma(imagem, C, Y)
        elif filtro_selecionado == "Transformação Linear":
            a = float(entry_A.get()) if entry_A.get() else 1
            b = float(entry_B.get()) if entry_B.get() else 1
            imagem_filtrada = Transformacoes.linear(imagem, a, b)
        elif filtro_selecionado == "Transformação Faixa Dinâmica":
            w = float(entry_A.get()) if entry_A.get() else 255
            imagem_filtrada = Transformacoes.faixa_dinamica(imagem, w)
        elif filtro_selecionado == "Zoom-in":
            imagem_filtrada = Transformacoes.zoom_in(imagem)
        elif filtro_selecionado == "Zoom-out":
            imagem_filtrada = Transformacoes.zoom_out(imagem)
        elif filtro_selecionado == "Rotacionar Imagem":
            ang = float(entry_A.get()) if entry_A.get() else 90
            imagem_filtrada = Transformacoes.rotacionar_imagem(imagem, -ang)
        elif filtro_selecionado == "Reflexão (flip horizontal)":
            imagem_filtrada = Transformacoes.flip_horizontal(imagem)
        elif filtro_selecionado == "Reflexão (flip vertical)":
            imagem_filtrada = Transformacoes.flip_vertical(imagem)
        elif filtro_selecionado == "Warping":
            imagem_filtrada = Transformacoes.warp_losango(imagem)
        else:
            imagem_filtrada = Filtros.aplicar_filtro_personalizado(imagem, matriz_convolucao)
        
        
        
        display_image(imagem_filtrada, imagem_processada) #carrega a imagem na janela

def atualizar_matriz_convolucao(event):
    # Lógica para atualizar os valores na matriz de convolução com base no filtro selecionado
    filtro_selecionado = filtro_val.get()

    valores = [[1 for _ in range(3)] for _ in range(3)]#Preenche a matriz 3x3 com 1
    global entry_A
    global entry_Y, Y_label, entry_B, B_label


    if filtro_selecionado == "Filtro da mediana":
        valores = [[1 for _ in range(3)] for _ in range(3)] 
    elif filtro_selecionado == "Filtro da Média":
        valores = [[0.11 for _ in range(3)] for _ in range(3)]#Preenche a matriz 3x3 com 0.11
    elif filtro_selecionado == "Filtro passa altas básico (Detecção de pontos)":
        # Definir os valores para o filtro passa altas básico
        valores = [[-1, -1, -1],
                   [-1,  8, -1],
                   [-1, -1, -1]]
    elif filtro_selecionado == "Operador de Prewitt em X":
        # Definir os valores para o filtro Prewitt X
        valores = [[-1, -1, -1],
                   [ 0,  0,  0],
                   [ 1,  1,  1]]
    elif filtro_selecionado == "Operador de Prewitt em Y":
        # Definir os valores para o filtro Prewitt Y
        valores = [[-1, 0, 1],
                   [-1, 0, 1],
                   [-1, 0, 1]]
    elif filtro_selecionado == "Operador de Sobel em X":
        # Definir os valores para o filtro Sobel X
        valores = [[-1, -2, -1],
                   [ 0,  0,  0],
                   [ 1,  2,  1]]
    elif filtro_selecionado == "Operador de Sobel em Y":
        # Definir os valores para o filtro Sobel Y
        valores = [[-1, 0, 1],
                   [-2, 0, 2],
                   [-1, 0, 1]]
    elif filtro_selecionado == "Filtragem Alto Reforço(Hight-Boost)":
        A_label = tk.Label(frame_meio, text="A:")
        A_label.grid(row=3, column=0, padx=0, pady=0, sticky="n")
        entry_A = tk.Entry(frame_meio, width=5)
        entry_A.grid(row=4, column=0, padx=0, pady=0, sticky="n")
    elif filtro_selecionado == "Transformação Logaritmo":
        A_label = tk.Label(frame_meio, text="A:")
        A_label.grid(row=3, column=0, padx=0, pady=0, sticky="n")
        entry_A = tk.Entry(frame_meio, width=5)
        entry_A.grid(row=4, column=0, padx=0, pady=0, sticky="n")
    elif filtro_selecionado == "Transformação Gamma":
        A_label = tk.Label(frame_meio, text="C:")
        A_label.grid(row=3, column=0, padx=0, pady=0, sticky="n")
        entry_A = tk.Entry(frame_meio, width=5)
        entry_A.grid(row=4, column=0, padx=0, pady=0, sticky="n")
        Y_label = tk.Label(frame_meio, text="Y:")
        Y_label.grid(row=5, column=0, padx=0, pady=0, sticky="ns")
        entry_Y = tk.Entry(frame_meio, width=5)
        entry_Y.grid(row=6, column=0, padx=0, pady=0, sticky="ns")
    elif filtro_selecionado == "Transformação Linear":
        A_label = tk.Label(frame_meio, text="a:")
        A_label.grid(row=3, column=0, padx=0, pady=0, sticky="n")
        entry_A = tk.Entry(frame_meio, width=5)
        entry_A.grid(row=4, column=0, padx=0, pady=0, sticky="n")
        B_label = tk.Label(frame_meio, text="b:")
        B_label.grid(row=5, column=0, padx=0, pady=0, sticky="ns")
        entry_B = tk.Entry(frame_meio, width=5)
        entry_B.grid(row=6, column=0, padx=0, pady=0, sticky="ns")
    elif filtro_selecionado == "Transformação Faixa Dinâmica":
        A_label = tk.Label(frame_meio, text="w_target:")
        A_label.grid(row=3, column=0, padx=0, pady=0, sticky="n")
        entry_A = tk.Entry(frame_meio, width=5)
        entry_A.grid(row=4, column=0, padx=0, pady=0, sticky="n")
    elif filtro_selecionado == "Rotacionar Imagem":
        A_label = tk.Label(frame_meio, text="angulo:")
        A_label.grid(row=3, column=0, padx=0, pady=0, sticky="n")
        entry_A = tk.Entry(frame_meio, width=5)
        entry_A.grid(row=4, column=0, padx=0, pady=0, sticky="n")
    


    if filtro_selecionado != "Transformação Gamma":
        try:
            entry_Y.grid_forget()
            Y_label.grid_forget()
        except NameError:
            pass

    # Atualizar as Entry widgets com os novos valores da matriz
    for i in range(3):
        for j in range(3):
            matriz_valores[i][j].delete(0, tk.END)
            matriz_valores[i][j].insert(0, str(valores[i][j]))


def main():
    root = tk.Tk()
    root.geometry("1000x600")
    width = root.winfo_width()
    height = root.winfo_height()
    root.configure(background="#000C66")

    global imagem_original, imagem_processada  # Para acessar as labels dentro das funções

    # Configuração das abas
    tab_control = ttk.Notebook(root)

    tab1 = tk.Frame(tab_control)
    tab2 = tk.Frame(tab_control)
    tab3 = tk.Frame(tab_control)

    tab_control.add(tab1, text='Filtros')
    tab_control.add(tab2, text='Equalização')
    tab_control.add(tab3, text='Operações')
    
    tab_control.pack(expand=1, fill='both')

    Equalizacao.equalizar_lena(tab2)
    Operacoes.mostrar_tela(tab3)

    # Frame dentro da aba 'Filtros' para organizar com grid
    frame_filtros = tk.Frame(tab1)
    frame_filtros.pack(expand=1, fill='both', padx=10, pady=10)

    # Labels para exibir as imagens
    imagem_original = tk.Label(frame_filtros)
    imagem_original.grid(row=0, column=0, padx=10, pady=10)

    imagem_processada = tk.Label(frame_filtros)
    imagem_processada.grid(row=0, column=8, padx=10, pady=10)
    
    # Botão para abrir a imagem 
    filter_button = tk.Button(frame_filtros, text="Selecionar Imagem", command=open_image)
    filter_button.grid(row=1, column=0, padx=10, pady=10)
    
    # Frame para o seletor de filtros, matriz e botão de aplicar filtro
    global frame_meio
    frame_meio = tk.Frame(frame_filtros)
    frame_meio.grid(row=0, column=1, rowspan=5, columnspan=7, pady=10)

    # Texto antes do seletor de filtros
    filter_label = tk.Label(frame_meio, text="Selecione um Filtro:")
    filter_label.grid(row=0, column=0, padx=10, pady=5, sticky='w')

    # Seletor de filtros
    global filtro_val
    filtro_val = tk.StringVar(value="Filtro da mediana")
    filters = ["Filtro da mediana", "Filtro da Média", "Filtro passa altas básico (Detecção de pontos)", 
               "Filtragem Alto Reforço(Hight-Boost)", "Operador de Roberts", "Operador de Roberts cruzado", 
               "Operador de Sobel", "Operador de Sobel em X", "Operador de Sobel em Y", "Operador de Prewitt", 
               "Operador de Prewitt em X", "Operador de Prewitt em Y", "Filtro Livre", "Negativo da Imagem",
               "Transformação Logaritmo", "Transformação Gamma", "Transformação Linear", "Transformação Faixa Dinâmica",
               "Zoom-in", "Zoom-out", "Rotacionar Imagem", "Reflexão (flip horizontal)", "Reflexão (flip vertical)",
               "Warping"]
    filter_menu = ttk.Combobox(frame_meio, textvariable=filtro_val, values=filters, width=40)
    filter_menu.grid(row=1, column=0, padx=10, pady=5, sticky='nsew')
    filter_menu.bind("<<ComboboxSelected>>", atualizar_matriz_convolucao)


    # Grade para mostrar a matriz editável
    matriz_frame = tk.Frame(frame_meio)
    matriz_frame.grid(row=2, column=0, padx=10, pady=10, sticky="n")  

    global matriz_valores
    matriz_valores = [[tk.Entry(matriz_frame, width=5)
                       for j in range(3)] for i in range(3)]
    for i in range(3):
        for j in range(3):
            matriz_valores[i][j].grid(row=i, column=j, padx=3, pady=3)
    
    # Botão para aplicar o filtro
    apply_button = tk.Button(frame_meio, text="Aplicar Filtro", command=lambda: aplicar_filtro(matriz_valores))
    apply_button.grid(row=7, column=0, padx=10, pady=10)

    print(imagem_original)
    
    root.mainloop()

if __name__ == '__main__':
    main()