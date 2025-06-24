import tkinter as tk
from tkinter import filedialog, ttk 
from PIL import Image, ImageTk
import numpy as np

def dilatacao_cinza(imagem):
    largura, altura = imagem.size
    pixels = imagem.load()
    nova_imagem = Image.new("L", (largura, altura))
    novos_pixels = nova_imagem.load()

    for y in range(1, altura - 1):
        for x in range(1, largura - 1):
            vizinhos = []
            for j in range(-1, 2):
                for i in range(-1, 2):
                    vizinhos.append(pixels[x + i, y + j])
            novos_pixels[x, y] = max(vizinhos)

    return nova_imagem

def erosao_cinza(imagem):
    largura, altura = imagem.size
    pixels = imagem.load()
    nova_imagem = Image.new("L", (largura, altura))
    novos_pixels = nova_imagem.load()

    for y in range(1, altura - 1):
        for x in range(1, largura - 1):
            vizinhos = []
            for j in range(-1, 2):
                for i in range(-1, 2):
                    vizinhos.append(pixels[x + i, y + j])
            novos_pixels[x, y] = min(vizinhos)

    return nova_imagem



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

def abertura(imagem_bin):
    img_erosao = erosao(imagem_bin)
    img_abertura = dilatacao(img_erosao)

    return img_abertura

def fechamento(image_bin):
    img_dilatacao = dilatacao(image_bin)
    img_fechamento = erosao(img_dilatacao)

    return img_fechamento

def gradiente(imagem_bin):
    img_dilatada = np.array(dilatacao(imagem_bin))
    img_erodida = np.array(erosao(imagem_bin))
    grad = img_dilatada - img_erodida
    grad = np.clip(grad, 0, 255).astype(np.uint8)

    return Image.fromarray(grad)

def contorno_interno(imagem_bin):
    img = np.array(imagem_bin)
    img_erodida = np.array(erosao(imagem_bin))
    return Image.fromarray((img - img_erodida).astype(np.uint8))

def contorno_externo(imagem_bin):
    img = np.array(imagem_bin)
    img_dilatada = np.array(dilatacao(imagem_bin))
    return Image.fromarray((img_dilatada - img).astype(np.uint8))

def top_hat(imagem_bin):
    img = np.array(imagem_bin)
    img_abertura = np.array(abertura(imagem_bin))
    th = img - img_abertura
    return Image.fromarray(np.clip(th, 0, 255).astype(np.uint8))

def bottom_hat(imagem_bin):
    img = np.array(imagem_bin)
    img_fechamento = np.array(fechamento(imagem_bin))
    bh = img_fechamento - img
    return Image.fromarray(np.clip(bh, 0, 255).astype(np.uint8))


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
    # Container principal (igual ao da parte binária)
    frame_cinza = tk.Frame(frame)
    frame_cinza.grid(row=0, column=0, columnspan=2, pady=10)

    # Label "Imagem Original" (igual ao "Imagem Binarizada" da parte inferior)
    label_original = tk.Label(frame_cinza, text="Imagem Original")
    label_original.grid(row=0, column=0, padx=10, pady=10)

    # Frame para controles (igual ao frame_bin da parte inferior)
    frame_controles_cinza = tk.Frame(frame_cinza)
    frame_controles_cinza.grid(row=1, column=0, columnspan=2, pady=5)

    # Imagem original (lado esquerdo) - igual à parte binária
    label_imagem_original = tk.Label(frame_controles_cinza)
    label_imagem_original.pack(side=tk.LEFT, padx=10)

    # Combobox central - mantendo o mesmo estilo
    combo_operacoes_original = ttk.Combobox(
        frame_controles_cinza,
        values=[ "Dilatação", "Erosão",],
        state="readonly",
        width=15
    )
    combo_operacoes_original.pack(side=tk.LEFT, padx=10)
    combo_operacoes_original.set("Dilatação")

    # Botão "Aplicar Operação" - mesmo estilo da parte binária
    btn_aplicar_original = tk.Button(
        frame_controles_cinza,
        text="Aplicar Operação",
        command=lambda: aplicar_operacao_original()
    )
    btn_aplicar_original.pack(side=tk.LEFT, padx=10)

    # Imagem resultado (lado direito) - igual ao label_resultado da parte binária
    label_resultado_original = tk.Label(frame_controles_cinza)
    label_resultado_original.pack(side=tk.LEFT, padx=10)

    # Botão "Carregar Imagem Original" (posicionado igual ao da parte binária)
    btn_carregar_original = tk.Button(frame_cinza, text="Carregar Imagem Original", command=lambda: carregar_original())
    btn_carregar_original.grid(row=0, column=1, padx=10, pady=10)

    def carregar_original():
        caminho = filedialog.askopenfilename(filetypes=[("PGM Files", "*.pgm")])
        if caminho:
            imagem = Image.open(caminho).convert("L")
            imagem_original[0] = imagem
            display_image(imagem, label_imagem_original)

    # --- SEPARADOR ---
    separator = tk.Label(frame, text="─" * 80)
    separator.grid(row=2, column=0, columnspan=2, pady=10)

    # --- PARTE DE BAIXO
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


    combo_operacoes = ttk.Combobox(
        frame_bin,
        values=["Dilatação", "Erosão",  "Abertura", "Fechamento", "Gradiente",  "Contorno interno", "Contorno externo", "Top-hat" , "Bottom-hat"],
        state="readonly"
    )
    combo_operacoes.pack(side=tk.LEFT, padx=10)
    combo_operacoes.set("Dilatação")

    # Botão "Aplicar Operação" (centro)
    btn_aplicar = tk.Button(
        frame_bin,
        text="Aplicar Operação",
        command=lambda: aplicar_operacao_binaria()
    )
    btn_aplicar.pack(side=tk.LEFT, padx=10)


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
            elif operacao == "Abertura":
                resultado = abertura(imagem_bin[0])
                display_image(resultado, label_resultado)
            elif operacao == "Fechamento":
                resultado = fechamento(imagem_bin[0])
                display_image(resultado, label_resultado)
            elif operacao == "Gradiente":
                resultado = gradiente(imagem_bin[0])
                display_image(resultado, label_resultado)
            elif operacao == "Contorno interno":
                resultado = contorno_interno(imagem_bin[0])
                display_image(resultado, label_resultado)
            elif operacao == "Contorno externo":
                resultado = contorno_externo(imagem_bin[0])
                display_image(resultado, label_resultado)
            elif operacao == "Top-hat":
                resultado = top_hat(imagem_bin[0])
                display_image(resultado, label_resultado)
            elif operacao == "Bottom-hat":
                resultado = bottom_hat(imagem_bin[0])
                display_image(resultado, label_resultado)
    
    def aplicar_operacao_original():
        if imagem_original[0]:
            operacao = combo_operacoes_original.get()
            if operacao == "Dilatação":
                resultado = dilatacao_cinza(imagem_original[0])
                display_image(resultado, label_resultado_original)
            elif operacao == "Erosão":
                resultado = erosao_cinza(imagem_original[0])
                display_image(resultado, label_resultado_original)