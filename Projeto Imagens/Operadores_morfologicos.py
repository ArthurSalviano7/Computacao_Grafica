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
            max_valor = -float('inf')  
            for j in range(-1, 2):
                for i in range(-1, 2):
                    valor_somado = pixels[x + i, y + j] + 1  
                    if valor_somado > max_valor:
                        max_valor = valor_somado
            novos_pixels[x, y] = max_valor

    return nova_imagem

def erosao_cinza(imagem):
    largura, altura = imagem.size
    pixels = imagem.load()
    nova_imagem = Image.new("L", (largura, altura))
    novos_pixels = nova_imagem.load()

    for y in range(1, altura - 1): 
        for x in range(1, largura - 1):
            min_valor = float('inf')  
            for j in range(-1, 2):  
                for i in range(-1, 2):
                    valor_subtraido = pixels[x + i, y + j] - 1  
                    if valor_subtraido < min_valor:
                        min_valor = valor_subtraido
            novos_pixels[x, y] = min_valor

    return nova_imagem

def abertura_cinza(imagem):
    img_erosao = erosao_cinza(imagem)
    img_abertura = dilatacao_cinza(img_erosao)

    return img_abertura

def fechamento_cinza(imagem):
    img_dilatacao = dilatacao_cinza(imagem)
    img_fechamento = erosao_cinza(img_dilatacao)

    return img_fechamento

def gradiente_cinza(imagem):

    img_dilatada = dilatacao_cinza(imagem)
    img_erodida = erosao_cinza(imagem)
    array_dilatacao = np.array(img_dilatada)
    array_erosao = np.array(img_erodida)
    grad = array_dilatacao - array_erosao
   
    
    return Image.fromarray(grad)

def contorno_interno_cinza(imagem):
    img_erodida = erosao_cinza(imagem)
    arr_orig = np.array(imagem)
    arr_ero = np.array(img_erodida)
    contorno = arr_orig - arr_ero
    
    return Image.fromarray(contorno)

def contorno_externo_cinza(imagem):
    img_dilatada = dilatacao_cinza(imagem)
    arr_dil = np.array(img_dilatada)
    arr_orig = np.array(imagem) 
    contorno = arr_dil - arr_orig
    
    return Image.fromarray(contorno)

def top_hat_cinza(imagem):
    img_abertura = abertura_cinza(imagem)
    arr_orig = np.array(imagem)
    arr_abert = np.array(img_abertura)
    top_hat = arr_orig - arr_abert
    
    return Image.fromarray(top_hat)

def bottom_hat_cinza(imagem):
    img_fechamento = fechamento_cinza(imagem)
    arr_fech = np.array(img_fechamento)
    arr_orig = np.array(imagem)
    bottom_hat = arr_fech - arr_orig
    
    return Image.fromarray(bottom_hat)

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
    frame_cinza = tk.Frame(frame)
    frame_cinza.grid(row=0, column=0, columnspan=2, pady=10)

    # Label "Imagem Original" 
    label_original = tk.Label(frame_cinza, text="Imagem Original")
    label_original.grid(row=0, column=0, padx=10, pady=10)

    # Frame para controles 
    frame_controles_cinza = tk.Frame(frame_cinza)
    frame_controles_cinza.grid(row=1, column=0, columnspan=2, pady=5)

    # Imagem original (lado esquerdo) 
    label_imagem_original = tk.Label(frame_controles_cinza)
    label_imagem_original.pack(side=tk.LEFT, padx=10)

    # Combobox central 
    combo_operacoes_original = ttk.Combobox(
        frame_controles_cinza,
        values=[ "Dilatação", "Erosão","Abertura", "Fechamento", "Gradiente","Contorno interno", "Contorno externo", "Top-hat" , "Bottom-hat" ],
        state="readonly",
        width=15
    )
    combo_operacoes_original.pack(side=tk.LEFT, padx=10)
    combo_operacoes_original.set("Dilatação")

    # Botão "Aplicar Operação" 
    btn_aplicar_original = tk.Button(
        frame_controles_cinza,
        text="Aplicar Operação",
        command=lambda: aplicar_operacao_cinza()
    )
    btn_aplicar_original.pack(side=tk.LEFT, padx=10)

    # Imagem resultado (lado direito)
    label_resultado_original = tk.Label(frame_controles_cinza)
    label_resultado_original.pack(side=tk.LEFT, padx=10)

    # Botão "Carregar Imagem Original" 
    btn_carregar_original = tk.Button(frame_cinza, text="Carregar Imagem", command=lambda: carregar_original())
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
    
    def aplicar_operacao_cinza():
        if imagem_original[0]:
            operacao = combo_operacoes_original.get()
            if operacao == "Dilatação":
                resultado = dilatacao_cinza(imagem_original[0])
                display_image(resultado, label_resultado_original)
            elif operacao == "Erosão":
                resultado = erosao_cinza(imagem_original[0])
                display_image(resultado, label_resultado_original)
            elif operacao == "Abertura":
                resultado = abertura_cinza(imagem_original[0])
                display_image(resultado, label_resultado_original)
            elif operacao == "Fechamento":
                resultado = fechamento_cinza(imagem_original[0])
                display_image(resultado, label_resultado_original)
            elif operacao == "Gradiente":
                resultado = gradiente_cinza(imagem_original[0])
                display_image(resultado, label_resultado_original)
            elif operacao == "Contorno interno":
                resultado = contorno_interno_cinza(imagem_original[0])
                display_image(resultado, label_resultado_original)
            elif operacao == "Contorno externo":
                resultado = contorno_externo_cinza(imagem_original[0])
                display_image(resultado, label_resultado_original)
            elif operacao == "Top-hat":
                resultado = top_hat_cinza(imagem_original[0])
                display_image(resultado, label_resultado_original)
            elif operacao == "Bottom-hat":
                resultado = bottom_hat_cinza(imagem_original[0])
                display_image(resultado, label_resultado_original)