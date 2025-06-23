import tkinter as tk
from tkinter import filedialog, ttk 
from PIL import Image, ImageTk
import numpy as np

def binarizar_por_media(imagem):
    imagem_array = np.array(imagem)
    media = np.sum(imagem_array) / (imagem_array.shape[0] * imagem_array.shape[1])
    imagem_bin = (imagem_array > media).astype(np.uint8) * 255
    return Image.fromarray(imagem_bin)

def erosao(imagem_bin):
    img = np.array(imagem_bin)
    altura, largura = img.shape
    resultado = np.zeros_like(img)

    for x in range(1, altura - 1):
        for y in range(1, largura - 1):
            if (img[x-1, y-1] == 255 and  # superior esquerdo
                img[x-1, y]   == 255 and  # superior
                img[x-1, y+1] == 255 and  # superior direito
                img[x,   y-1] == 255 and  # esquerdo
                img[x,   y]   == 255 and  # centro 
                img[x,   y+1] == 255 and  # direito
                img[x+1, y-1] == 255 and  # inferior esquerdo
                img[x+1, y]   == 255 and  # inferior
                img[x+1, y+1] == 255):   # inferior direito
                resultado[x, y] = 255
    return Image.fromarray(resultado)

def dilatacao(imagem_bin):
    img = np.array(imagem_bin)
    altura, largura = img.shape
    resultado = np.zeros_like(img)

    for x in range(1, altura - 1):
        for y in range(1, largura - 1):
            if (img[x-1, y-1] == 255 or  # superior esquerdo
                img[x-1, y]   == 255 or  # superior
                img[x-1, y+1] == 255 or  # superior direito
                img[x,   y-1] == 255 or  # esquerdo
                img[x,   y]   == 255 or  # centro 
                img[x,   y+1] == 255 or  # direito
                img[x+1, y-1] == 255 or  # inferior esquerdo
                img[x+1, y]   == 255 or  # inferior
                img[x+1, y+1] == 255):   # inferior direito
                resultado[x, y] = 255
                
    return Image.fromarray(resultado)

def display_image(image, label):
    image = image.resize((200, 200))
    tk_image = ImageTk.PhotoImage(image)
    label.config(image=tk_image)
    label.image = tk_image

def mostrar_tela(tab):
    frame = tk.Frame(tab)
    frame.pack(expand=1, fill='both', padx=10, pady=10)

    imagem_original = [None]
    imagem_bin = [None]

    # --- PARTE DE CIMA (Imagem original em tons de cinza) ---
    label_original = tk.Label(frame, text="Imagem Original")
    label_original.grid(row=0, column=0, padx=10, pady=10)

    btn_carregar_original = tk.Button(frame, text="Carregar Imagem Original", command=lambda: carregar_original())
    btn_carregar_original.grid(row=0, column=1, padx=10, pady=10)

    label_imagem_original = tk.Label(frame)
    label_imagem_original.grid(row=1, column=0, padx=10, pady=10)

    def carregar_original():
        caminho = filedialog.askopenfilename(filetypes=[("PGM Files", "*.pgm")])
        if caminho:
            imagem = Image.open(caminho).convert("L")
            imagem_original[0] = imagem
            display_image(imagem, label_imagem_original)

    # --- SEPARADOR ---
    separator = tk.Label(frame, text="─" * 80)
    separator.grid(row=2, column=0, columnspan=2, pady=10)

    # --- PARTE DE BAIXO (Imagem binarizada) ---
    label_bin = tk.Label(frame, text="Imagem Binarizada")
    label_bin.grid(row=3, column=0, padx=10, pady=10)

    btn_carregar_bin = tk.Button(frame, text="Carregar Imagem Binarizada", command=lambda: carregar_binarizada())
    btn_carregar_bin.grid(row=3, column=1, padx=10, pady=10)

    # Frame para imagem + Combobox + Botão + Resultado
    frame_bin = tk.Frame(frame)
    frame_bin.grid(row=4, column=0, columnspan=2, pady=10)

    # Imagem binarizada (lado esquerdo)
    label_imagem_bin = tk.Label(frame_bin)
    label_imagem_bin.pack(side=tk.LEFT, padx=10)

    # Combobox (centro)
    combo_operacoes = ttk.Combobox(
        frame_bin,
        values=["Erosão", "Dilatação"],
        state="readonly"
    )
    combo_operacoes.pack(side=tk.LEFT, padx=10)
    combo_operacoes.set("Erosão")

    # Botão "Aplicar Operação" (centro)
    btn_aplicar = tk.Button(
        frame_bin,
        text="Aplicar Operação",
        command=lambda: aplicar_operacao_binaria()
    )
    btn_aplicar.pack(side=tk.LEFT, padx=10)

    # Imagem resultante (lado direito)
    label_resultado = tk.Label(frame_bin)
    label_resultado.pack(side=tk.LEFT, padx=10)

    def carregar_binarizada():
        caminho = filedialog.askopenfilename(filetypes=[("PGM Files", "*.pgm")])
        if caminho:
            imagem = Image.open(caminho).convert("L")
            imagem_bin[0] = binarizar_por_media(imagem)
            display_image(imagem_bin[0], label_imagem_bin)

    def aplicar_operacao_binaria():
        if imagem_bin[0]:
            operacao = combo_operacoes.get()
            if operacao == "Erosão":
                resultado = erosao(imagem_bin[0])
                display_image(resultado, label_resultado)
            elif operacao == "Dilatação":
                resultado = dilatacao(imagem_bin[0])
                display_image(resultado, label_resultado)