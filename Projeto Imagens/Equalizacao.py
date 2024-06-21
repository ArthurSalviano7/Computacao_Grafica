import numpy as np
import tkinter as tk
from tkinter import ttk, filedialog
import matplotlib.pyplot as plt
from PIL import Image, ImageTk
import Operacoes
import main

def display_image(image, label):
    image.thumbnail((300, 300))  # Reduzir o tamanho para caber na interface
    tk_image = ImageTk.PhotoImage(image)
    label.config(image=tk_image)
    label.image = tk_image

def equalizar_imagem(imagem):
    # Converter imagem para matriz numpy
    img_array = np.array(imagem)

    # Calcular o histograma da imagem original
    hist, bins = np.histogram(img_array.flatten(), bins=256, range=(0,256))

    # Calcular a função de distribuição acumulada (CDF - Cumulative Distribution Function)
    cdf = hist.cumsum()
    cdf_normalized = cdf / cdf.max()  # Normalizar para valores entre 0 e 1

    # Equalização: mapear os valores originais para novos valores equalizados usando a CDF
    img_equalizada = np.interp(img_array.flatten(), bins[:-1], cdf_normalized * 255)
    img_equalizada = img_equalizada.reshape(img_array.shape).astype(np.uint8)

    # Criar imagem PIL a partir da matriz equalizada
    imagem_equalizada = Image.fromarray(img_equalizada.astype('uint8'), 'L')

    print(imagem_equalizada)
    return imagem_equalizada


def mostrar_histograma_original(imagem):
    # Função para criar uma nova janela com o histograma da imagem original
    histograma_original = tk.Toplevel()
    histograma_original.title("Histograma da Imagem Original")

    img_array = np.array(imagem)
    hist, bins = np.histogram(img_array.flatten(), bins=256, range=(0, 256))

    plt.figure(figsize=(8, 4))
    plt.hist(img_array.flatten(), bins=256, range=(0, 256), color='b', alpha=0.7)
    plt.xlabel('Valor do Pixel')
    plt.ylabel('Frequência')
    plt.title('Histograma da Imagem Original')
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def mostrar_histograma_equalizada(imagem_equalizada):
    # Função para criar uma nova janela com o histograma da imagem equalizada
    histograma_equalizado = tk.Toplevel()
    histograma_equalizado.title("Histograma da Imagem Equalizada")

    img_array = np.array(imagem_equalizada)
    hist, bins = np.histogram(img_array.flatten(), bins=256, range=(0, 256))

    plt.figure(figsize=(8, 4))
    plt.hist(img_array.flatten(), bins=256, range=(0, 256), color='b', alpha=0.7)
    plt.xlabel('Valor do Pixel')
    plt.ylabel('Frequência')
    plt.title('Histograma da Imagem Equalizada')
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def equalizar_lena(tab2):

    imagem = Image.open('./imagens/lena.pgm')

    imagem_equalizada = equalizar_imagem(imagem)
    # Frame dentro da aba 'Filtros' para organizar com grid
    frame_imagens = tk.Frame(tab2)
    frame_imagens.pack(expand=1, fill='both', padx=10, pady=10)

    text_original = tk.Label(frame_imagens, text="Imagem Original:")
    text_original.grid(row=0, column=0, padx=10, pady=5)
    # Labels para exibir as imagens
    imagem_lena = tk.Label(frame_imagens)
    imagem_lena.grid(row=1, column=0, padx=10, pady=10)
    
    display_image(imagem, imagem_lena)

    # Botão histograma original
    button_original = tk.Button(frame_imagens, text="Histograma original", command=lambda: mostrar_histograma_original(imagem))
    button_original.grid(row=7, column=0, padx=10, pady=10)

    text_equalizada = tk.Label(frame_imagens, text="Imagem Equalizada:")
    text_equalizada.grid(row=0, column=3, padx=10, pady=5)

    imagem_equalizada_label = tk.Label(frame_imagens)
    imagem_equalizada_label.grid(row=1, column=3, padx=10, pady=10)

    # Botão histograma equalizado
    button_eq = tk.Button(frame_imagens, text="Histograma equalizado", command=lambda: mostrar_histograma_equalizada(imagem_equalizada))
    button_eq.grid(row=7, column=3, padx=10, pady=10)

    global frame_meio
    frame_meio = tk.Frame(frame_imagens)
    frame_meio.grid(row=0, column=1, rowspan=5, columnspan=7, padx=300)
    
    display_image(imagem_equalizada, imagem_equalizada_label)
    
    