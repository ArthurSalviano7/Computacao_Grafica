import numpy as np
from PIL import Image, ImageTk

def soma(imagem1, imagem2):

    imagem1_array = np.array(imagem1)
    imagem2_array = np.array(imagem2)

    imagem_soma = imagem1_array + imagem2_array

    # Aplicar truncamento para manter os valores dentro do intervalo 0-255
    imagem_soma = np.clip(imagem_soma, 0, 255).astype(np.uint8)

    return imagem_soma