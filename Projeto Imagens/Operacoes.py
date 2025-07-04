import numpy as np
import tkinter as tk
from tkinter import ttk, filedialog
from PIL import Image, ImageTk

def soma(imagem1, imagem2):

    imagem1_array = np.array(imagem1)
    imagem2_array = np.array(imagem2)

    imagem_soma = imagem1_array + imagem2_array

    # Aplicar truncamento para manter os valores dentro do intervalo 0-255
    imagem_soma = np.clip(imagem_soma, 0, 255).astype(np.uint8)

    return imagem_soma

def display_image(image, label):
    image.thumbnail((300, 300))  # Reduzir o tamanho para caber na interface
    tk_image = ImageTk.PhotoImage(image)
    label.config(image=tk_image)
    label.image = tk_image

def realizar_operacao(image1, image2, operacao):
    largura, altura = image1.size
    
    # Criar nova imagem para o resultado
    result_image = Image.new('L', (largura, altura))
    
    # Percorrer cada pixel das imagens
    for y in range(altura):
        for x in range(largura):
            pixel1 = image1.getpixel((x, y))
            pixel2 = image2.getpixel((x, y))
            
            if operacao == "Soma":
                result_pixel = pixel1 + pixel2
            elif operacao == "Subtração":
                result_pixel = pixel1 - pixel2
            elif operacao == "Multiplicação":
                result_pixel = pixel1 * pixel2
            elif operacao == "Divisão":
                result_pixel = pixel1 / (pixel2 + 1e-5)  # Adicionar uma pequena constante para evitar divisão por zero
            
            # Normalizar o valor do pixel para a faixa [0, 255]
            result_pixel = int(min(max(result_pixel, 0), 255))
            
            # Definir o pixel na imagem resultante
            result_image.putpixel((x, y), result_pixel)
    
    return result_image

def aplicar_operacao(imagem1, imagem2):
     # Lógica para atualizar os valores na matriz de convolução com base no filtro selecionado
    operacao_selecionada = filtro_val.get()

    if operacao_selecionada == "Soma":
        img_resultado = realizar_operacao(imagem1, imagem2, "Soma")
    elif operacao_selecionada == "Subtração":
        img_resultado = realizar_operacao(imagem1, imagem2, "Subtração")
    elif operacao_selecionada == "Multiplicação":
        img_resultado = realizar_operacao(imagem1, imagem2, "Multiplicação")
    elif operacao_selecionada == "Divisão":
        img_resultado = realizar_operacao(imagem1, imagem2, "Divisão")
    elif operacao_selecionada == "AND lógico":
        img_resultado, _, _ = operacoes_logicas(imagem1, imagem2)
    elif operacao_selecionada == "OR lógico":
        _, img_resultado, _ = operacoes_logicas(imagem1, imagem2)
    elif operacao_selecionada == "XOR lógico":
        _, _, img_resultado = operacoes_logicas(imagem1, imagem2)
    else:
        return  # Nenhuma operação válida

    display_image(img_resultado, resultado_label)


def operacoes_logicas(imagem1, imagem2):
    imagem1_array = np.array(imagem1)
    imagem2_array = np.array(imagem2)

    altura, largura = imagem1_array.shape
    and_result = np.zeros((altura, largura), dtype=np.uint8)
    or_result  = np.zeros((altura, largura), dtype=np.uint8)
    xor_result = np.zeros((altura, largura), dtype=np.uint8)

    for y in range(altura):
        for x in range(largura):
            p1 = imagem1_array[y][x]
            p2 = imagem2_array[y][x]

    
            and_result[y][x] = p1 & p2
            or_result[y][x]  = p1 | p2
            xor_result[y][x] = p1 ^ p2

    # Converte para imagens PIL
    and_img = Image.fromarray(and_result)
    or_img = Image.fromarray(or_result)
    xor_img = Image.fromarray(xor_result)

    return and_img, or_img, xor_img



def mostrar_tela(tab3):
    imagem = Image.open('./imagens/lena.pgm')

    imagem2 = Image.open('./imagens/airplane.pgm')
    # Frame dentro da aba 'Filtros' para organizar com grid
    frame_filtros = tk.Frame(tab3)
    frame_filtros.pack(expand=1, fill='both', padx=10, pady=10)

    #bin1, bin2, and_img, or_img, xor_img = operacoes_logicas(imagem, imagem2)

    #bin_label1 = tk.Label(frame_filtros)
    #bin_label1.grid(row=1, column=0)

    #bin_label2 = tk.Label(frame_filtros)
    #bin_label2.grid(row=1, column=8)


# Mostrando as binarizadas
    #display_image(bin1, bin_label1)
    #display_image(bin2, bin_label2)



    # Labels para exibir as imagens
    imagem_1_label = tk.Label(frame_filtros)
    imagem_1_label.grid(row=0, column=0, padx=10, pady=10)

    display_image(imagem, imagem_1_label)
    
    imagem_2_label = tk.Label(frame_filtros)
    imagem_2_label.grid(row=0, column=8, padx=10, pady=10) 
    display_image(imagem2, imagem_2_label)

    global resultado_label
    resultado_label = tk.Label(frame_filtros)
    resultado_label.grid(row=1, column=1, padx=0, pady=0) 

    # Frame para o seletor de filtros, matriz e botão de aplicar filtro
    global frame_meio
    frame_meio = tk.Frame(frame_filtros)
    frame_meio.grid(row=0, column=1, rowspan=5, columnspan=7, pady=10)

  
    filter_label = tk.Label(frame_meio, text="Selecione um Filtro:")
    filter_label.grid(row=0, column=0, padx=10, pady=5, sticky='w')

    # Seletor de filtros
    global filtro_val
    filtro_val = tk.StringVar(value="Soma")
    filters = ["Soma", "Subtração", "Divisão", "Multiplicação", 
           "AND lógico", "OR lógico", "XOR lógico"]
    filter_menu = ttk.Combobox(frame_meio, textvariable=filtro_val, values=filters, width=40)
    filter_menu.grid(row=1, column=0, padx=10, pady=5, sticky='nsew')

    
 
    apply_button = tk.Button(frame_meio, text="Aplicar Filtro", command=lambda: aplicar_operacao(imagem, imagem2))
    apply_button.grid(row=2, column=0, padx=10, pady=0)