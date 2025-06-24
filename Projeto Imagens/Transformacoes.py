import math
from turtle import width
import numpy as np
from PIL import Image, ImageTk

# TRANSFORMAÇÕES
def negativo_da_imagem(imagem):
    # Criar uma cópia da imagem para aplicar a Transformação
    imagem_transf = imagem.copy()
    # Obter largura e altura da imagem
    height, width = imagem.shape
    # Converter imagem para matriz numpy
    img_array = np.array(imagem)

    # Aplicar o filtro
    for x in range(0, height):
        for y in range(0, width):
            valor_transformado = 255 - img_array[x, y] # S = 255 - r
            
            imagem_transf[x, y] = valor_transformado

    # Converter a matriz filtrada de volta para imagem PIL
    imagem_transf_convertida = Image.fromarray(imagem_transf.astype('uint8'), 'L')

    print(imagem_transf, "\n")

    return imagem_transf_convertida

def logaritmo(imagem, a):
    # Criar uma cópia da imagem para aplicar a Transformação
    imagem_transf = imagem.copy()
    # Obter largura e altura da imagem
    height, width = imagem.shape
    # Converter imagem para matriz numpy
    img_array = np.array(imagem)
    
    # Aplicar o filtro
    for x in range(0, height):
        for y in range(0, width):
            valor_transformado = a * np.log(img_array[x, y] + 1)   # S = a * log(r + 1)
            
            imagem_transf[x, y] = valor_transformado

    # Converter a matriz filtrada de volta para imagem PIL
    imagem_transf_convertida = Image.fromarray(imagem_transf.astype('uint8'), 'L')

    print(imagem_transf, "\n")

    return imagem_transf_convertida

def gamma(imagem, c, gamma):
    # Criar uma cópia da imagem para aplicar a Transformação
    imagem_transf = imagem.copy()
    # Obter largura e altura da imagem
    height, width = imagem.shape
    # Converter imagem para matriz numpy
    img_array = np.array(imagem)

    # Aplicar o filtro
    for x in range(0, height):
        for y in range(0, width):
            # S = c * r**y
            valor_transformado = round(c * (img_array[x, y] ** gamma))
            valor_transformado = np.clip(valor_transformado, 0, 255)       
            imagem_transf[x, y] = valor_transformado


    # Converter a matriz filtrada de volta para imagem PIL
    imagem_transf_convertida = Image.fromarray(imagem_transf.astype('uint8'), 'L')

    print(imagem_transf, "\n")

    return imagem_transf_convertida

def linear(imagem, a, b):
    # Criar uma cópia da imagem para aplicar a Transformação
    imagem_transf = imagem.copy()
    # Obter largura e altura da imagem
    height, width = imagem.shape
    # Converter imagem para matriz numpy
    img_array = np.array(imagem)

    # Aplicar o filtro
    for x in range(0, height):
        for y in range(0, width):
            # S = a * r + b
            valor_transformado = round(a * img_array[x, y] + b)
            valor_transformado = np.clip(valor_transformado, 0, 255)       
            imagem_transf[x, y] = valor_transformado

    # Converter a matriz filtrada de volta para imagem PIL
    imagem_transf_convertida = Image.fromarray(imagem_transf.astype('uint8'), 'L')

    print(imagem_transf, "\n")

    return imagem_transf_convertida

def faixa_dinamica(imagem, w_target):
    # Criar uma cópia da imagem para aplicar a Transformação
    imagem_transf = imagem.copy()
    # Obter largura e altura da imagem
    height, width = imagem.shape
    # Converter imagem para matriz numpy
    img_array = np.array(imagem)

    #Pegar os valores min e max da imagem (nível de cinza)
    fmin = np.min(img_array)
    fmax = np.max(img_array)

    # Aplicar a transformacao
    for x in range(0, height):
        for y in range(0, width):
            # S = (f - fmin / fmax - fmin) * w_target
            valor_transformado = round(((img_array[x, y] - fmin) / (fmax - fmin)) * w_target)
            valor_transformado = np.clip(valor_transformado, 0, 255)       
            imagem_transf[x, y] = valor_transformado


    # Converter a matriz filtrada de volta para imagem PIL
    imagem_transf_convertida = Image.fromarray(imagem_transf.astype('uint8'), 'L')

    print(imagem_transf, "\n")

    return imagem_transf_convertida

def intensidade_geral(imagem, largura):
    # Criar uma cópia da imagem para aplicar a Transformação
    imagem_transf = imagem.copy()
    height, width = imagem.shape
    
    # Converter imagem para matriz numpy
    img_array = np.array(imagem, dtype=np.float64)
    
    # Pegar o centro dos valores da imagem (nível de cinza)
    w = int(np.max(img_array) / 2) # Ex: L = 256, w = 127

    # Aplicar a transformação intensidade geral
    for x in range(0, height):
        for y in range(0, width):
            # S = 255*(1 / 1 + e^ -(r - w)/largura
            valor_transformado = int(255 * ( 1 / (1 + np.exp( -( (img_array[x, y] - w) / largura )))))
            valor_transformado = np.clip(valor_transformado, 0, 255)       
            imagem_transf[x, y] = valor_transformado

    # Arredondar para os valores inteiros mais próximos
    img_array = np.round(imagem_transf).astype(np.uint8)

    # Converter a matriz filtrada de volta para imagem PIL
    imagem_transf_convertida = Image.fromarray(img_array, 'L')

    return imagem_transf_convertida


# TRANSFORMAÇÕES GEOMÉTRICAS
def escala_imagem(imagem_original_np, sx, sy):
    altura_original, largura_original = imagem_original_np.shape
    
    # Calcular as novas dimensões de acordo com os fatores de escala
    # Sua convenção: Sx afeta a altura (Eixo X), Sy afeta a largura (Eixo Y)
    nova_altura = int(altura_original * sx)
    nova_largura = int(largura_original * sy)

    # Criar uma nova matriz para a imagem escalada, preenchida com zeros (preto)
    img_escalada_np = np.zeros((nova_altura, nova_largura), dtype=np.uint8)

    # Percorrer cada pixel da NOVA imagem (img_escalada_np)
    # y_novo é o índice da linha na nova imagem (vertical)
    # x_novo é o índice da coluna na nova imagem (horizontal)
    for x_novo in range(nova_altura):  # Itera o EIXO X (VERTICAL) da nova imagem
        for y_novo in range(nova_largura): # Itera o EIXO Y (HORIZONTAL) da nova imagem
            
            # Mapeamento inverso para encontrar a coordenada correspondente na imagem original         
            x_original_float = x_novo / sx
            y_original_float = y_novo / sy

            # Interpolação Vizinho Mais Próximo:
            # Arredonda para o inteiro mais próximo.
            x_original_int = int(np.round(x_original_float))
            y_original_int = int(np.round(y_original_float))

            # Garante que as coordenadas estejam dentro dos limites da imagem original
            # x_original_int deve estar no range [0, altura_original - 1]
            # y_original_int deve estar no range [0, largura_original - 1]
            x_original_clamped = np.clip(x_original_int, 0, altura_original - 1)
            y_original_clamped = np.clip(y_original_int, 0, largura_original - 1)

            # Atribui o valor do pixel da imagem original para a nova imagem
            # Acesso ao array NumPy: [linha, coluna]
            img_escalada_np[x_novo, y_novo] = imagem_original_np[x_original_clamped, y_original_clamped]
    
    # Converter a matriz NumPy de volta para uma imagem PIL para retorno
    imagem_escalada_pil = Image.fromarray(img_escalada_np)
    
    print(f"Transformação de Escala aplicada: Sx={sx} (vertical), Sy={sy} (horizontal)")
    print(f"Dimensões originais: {largura_original}x{altura_original}")
    print(f"Dimensões escaladas: {nova_largura}x{nova_altura}")

    return imagem_escalada_pil

def translacao_imagem(imagem, tx, ty):
    altura_original, largura_original = imagem.shape

    # Criar uma nova matriz para a imagem transladada, preenchida com zeros (preto)
    img_transladada_np = np.zeros((altura_original, largura_original), dtype=np.uint8)

    # Percorrer cada pixel da NOVA imagem (img_transladada_np), que tem o mesmo tamanho da original
    for x in range(altura_original):
        for y in range(largura_original):
            # X' = X + DeltaX => DeltaX = desloc. vertical
            # Y' = Y + DeltaY => DeltaY = desloc. horizontal
            x_novo = x + int(tx) 
            y_novo = y + int(ty)
            
            # Verificar se a coordenada original está dentro dos limites da imagem original
            if 0 <= x_novo < altura_original and \
               0 <= y_novo < largura_original:
                # Se sim, pega o pixel da imagem original
                img_transladada_np[x_novo, y_novo] = imagem[x, y]
    
    # Converter a matriz NumPy de volta para uma imagem PIL para retorno
    imagem_transladada_pil = Image.fromarray(img_transladada_np)
    
    print(f"Transformação de Translação aplicada (tamanho fixo): Tx={tx}, Ty={ty}")
    print(f"Dimensões: {largura_original}x{altura_original} -> {largura_original}x{altura_original}")

    return imagem_transladada_pil

def rotacionar_imagem(imagem, angulo):
    altura_original, largura_original = imagem.shape
    
    # Converter imagem para matriz numpy
    img_array = np.array(imagem)
    
    # Converter ângulo para radianos
    angulo_rad = math.radians(angulo)
    
    # Calcular as dimensões da imagem rotacionada
    largura_rotacionada = int(abs(largura_original * math.cos(angulo_rad)) + abs(altura_original * math.sin(angulo_rad)))
    altura_rotacionada = int(abs(altura_original * math.cos(angulo_rad)) + abs(largura_original * math.sin(angulo_rad)))
    
    # Criar matriz para a imagem rotacionada
    img_rotacionada = np.zeros((altura_rotacionada, largura_rotacionada), dtype=np.uint8)
    
    # Calcular centro da imagem original
    centro_x = altura_original // 2
    centro_y = largura_original // 2
    
    # Calcular centro da imagem rotacionada
    centro_x_rot = altura_rotacionada // 2
    centro_y_rot = largura_rotacionada // 2
    
    # Rotação da imagem
    for x in range(altura_original):
        for y in range(largura_original):
            # Calcular coordenadas rotacionadas
            # X′ = X⋅cos(Ang)+Y⋅sin(Ang)
            # Y′ = Y⋅cos(Ang)−X⋅sin(Ang)
            x_rot = int((x - centro_x) * math.cos(angulo_rad) + (y - centro_y) * math.sin(angulo_rad) + centro_x_rot )
            y_rot = int((y - centro_y) * math.cos(angulo_rad) - (x - centro_x) * math.sin(angulo_rad) + centro_y_rot)
            
            # Verificar limites
            if 0 <= y_rot < largura_rotacionada and 0 <= x_rot < altura_rotacionada:
                img_rotacionada[x_rot, y_rot] = img_array[x, y]
    
    # Converter matriz de volta para imagem PIL
    imagem_rotacionada = Image.fromarray(img_rotacionada)
    
    return imagem_rotacionada

def flip_horizontal(imagem):
    altura_original, largura_original  = imagem.shape
    
    # Converter imagem para matriz numpy
    img_array = np.array(imagem)
    
    # Criar matriz transposta
    img_transposta = np.transpose(img_array)
        
    # Criar matriz para rotacionar a imagem transposta
    imagem_flipada = rotacionar_imagem(img_transposta, 90)
    
    return imagem_flipada

def flip_vertical(imagem):
    # Converter imagem para matriz numpy
    img_array = np.array(imagem)
    
    # Criar matriz transposta
    img_transposta = np.transpose(img_array)
    
    # Criar matriz para a imagem rotacionada 90 graus no sentido horário
    imagem_flipada = rotacionar_imagem(img_transposta, 270)
    
    return imagem_flipada

def cisalhar_imagem(imagem, a, b, c, d, e, f, i, j):
    altura_original, largura_original  = imagem.shape
    
    # Converter imagem para matriz numpy
    img_array = np.array(imagem)
    
    # Calcular a dimensão da nova imagem para garantir que cabe o losango
    largura_nova = int(np.sqrt((largura_original**2 + altura_original**2) / 2) * 2)
    altura_nova = largura_nova
    img_cis = np.zeros((altura_nova, largura_nova), dtype=img_array.dtype)
    
    # Coeficientes para a transformação padrão:
    #a, b, c = 1, 0.5, 0
    #d, e, f = 0.5, 1, 0
    #i, j = 0, 0
    
    # Centro da imagem original
    centro_x = largura_original // 2
    centro_y = altura_original // 2
    
    # Centro da nova imagem
    centro_x_nova = largura_nova // 2
    centro_y_nova = altura_nova // 2
    
    for x in range(altura_nova):
        for y in range(largura_nova):
            # Calcular as coordenadas originais usando a transformação inversa
            # denominador = i*X + j*Y + 1
            denom = i * (x - centro_x_nova) + j * (y - centro_y_nova) + 1
            if denom == 0:
                continue
            
            x_original = (a * (x - centro_x_nova) + b * (y - centro_y_nova) + c) / denom
            y_original = (d * (x - centro_x_nova) + e * (y - centro_y_nova) + f) / denom
            
            x_original = int(x_original + centro_x)
            y_original = int(y_original + centro_y)
            
            # Verificar se as coordenadas originais estão dentro dos limites da imagem original
            if 0 <= x_original < largura_original and 0 <= y_original < altura_original:
                img_cis[x, y] = img_array[x_original, y_original]
    
    # Converter matriz de volta para imagem PIL
    imagem_cis = Image.fromarray(img_cis)
    
    return imagem_cis