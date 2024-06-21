import numpy as np
from PIL import Image, ImageTk
import Operacoes

def aplicar_filtro_personalizado(imagem, matriz_convolucao):
    
    # Criar uma cópia da imagem para aplicar o filtro
    imagem_filtrada = imagem.copy()

    # Obter largura e altura da imagem
    width, height = imagem.shape

    # Converter imagem para matriz numpy
    img_array = np.array(imagem)

    # Aplicar o filtro personalizado
    for y in range(1, height - 1):
        for x in range(1, width - 1):
            # Calcular o produto escalar entre a vizinhança e a mascara
            # Extrair a vizinhança 3x3 do pixel atual (y-1 até y+2 seleciona as 
            # linhas 'y-1', 'y' e 'y+1' da matriz, o mesmo acontece com as colunas(x-1 até x+2))
            vizinhanca = img_array[y - 1:y + 1 + 1,
                                     x - 1:x + 1 + 1]
            filtered_value = int(np.sum(vizinhanca * matriz_convolucao))

            # Limitar o valor resultante ao intervalo de 0 a 255 (Truncamento)
            filtered_value = np.clip(filtered_value, 0, 255)

            imagem_filtrada[y, x] = filtered_value

    # Converter a matriz filtrada de volta para imagem PIL
    imagem_filtrada_convertida = Image.fromarray(imagem_filtrada.astype('uint8'), 'L')

    print(imagem_filtrada, "\n")

    return imagem_filtrada_convertida

def filtro_media(imagem):
    
    # Criar uma cópia da imagem para aplicar o filtro
    imagem_filtrada = imagem.copy()

    # Obter largura e altura da imagem
    height, width = imagem.shape

    # Converter imagem para matriz numpy
    img_array = np.array(imagem)
    
    '''
    1/9 * [ 1, 1, 1]
          [ 1, 1, 1]
          [ 1, 1, 1]
    '''
    matriz_convolucao = np.ones((3, 3)) / 9 

    # Aplicar o filtro
    for y in range(1, height - 1):
        for x in range(1, width - 1):
            # Calcular a média da vizinhança usando a mascara
            vizinhanca = img_array[y - 1:y + 2, x - 1:x + 2]
            filtered_value = round(np.sum(vizinhanca * matriz_convolucao)) # arredondar o resultado da convolucao

            # Limitar o valor resultante ao intervalo de 0 a 255
            filtered_value = np.clip(filtered_value, 0, 255)

            imagem_filtrada[y, x] = filtered_value
    
    # Converter a matriz filtrada de volta para imagem PIL
    imagem_filtrada_convertida = Image.fromarray(imagem_filtrada.astype('uint8'), 'L')
    
    print(imagem_filtrada, "\n")

    return imagem_filtrada_convertida

def filtro_mediana(imagem):
    # Criar uma cópia da imagem para aplicar o filtro
    imagem_filtrada = imagem.copy()

    # Obter largura e altura da imagem
    height, width = imagem.shape

    # Converter imagem para matriz numpy
    img_array = np.array(imagem)

    # Aplicar o filtro da mediana
    for y in range(1, height - 1):
        for x in range(1, width - 1):
            # Extrair a vizinhança 3x3 do pixel atual (y-1 até y+2 seleciona as 
            # linhas 'y-1', 'y' e 'y+1' da matriz, o mesmo acontece com as colunas(x-1 até x+2))
            vizinhanca = img_array[y - 1:y + 2, x - 1:x + 2]
            
            # Calcular a mediana da vizinhança
            mediana = np.median(vizinhanca)
            
            mediana = np.clip(mediana, 0, 255) # Limitar o valor resultante ao intervalo de 0 a 255
            
            # Atribuir a mediana ao pixel correspondente na imagem filtrada
            imagem_filtrada[y, x] = mediana

    # Converter a matriz filtrada de volta para imagem PIL
    imagem_filtrada_convertida = Image.fromarray(imagem_filtrada.astype('uint8'), 'L')

    print(imagem_filtrada, "\n")

    return imagem_filtrada_convertida

def operador_prewitt(imagem):
    # Criar uma cópia da imagem para aplicar o filtro
    imagem_filtrada_em_x = imagem.copy()
    imagem_filtrada_em_y = imagem.copy()

    height, width = imagem.shape
    
    img_array_x = np.array(imagem)
    img_array_y = np.array(imagem)


    #"Operador de Prewitt em X":
    matriz_x = [[-1, -1, -1],
               [ 0,  0,  0],
               [ 1,  1,  1]]
    #"Operador de Prewitt em Y":
    matriz_y = [[-1, 0, 1],
               [-1, 0, 1],
               [-1, 0, 1]]

    for y in range(1, height - 1):
        for x in range(1, width - 1):
            # Operador de prewitt em X:
            vizinhanca_x = img_array_x[y - 1:y + 2, x - 1:x + 2]
            
            filtered_value_x = round(np.sum(vizinhanca_x * matriz_x))
            filtered_value_x = np.clip(filtered_value_x, 0, 255) #Truncamento
            # Atribuir ao pixel correspondente na imagem filtrada
            imagem_filtrada_em_x[y, x] = filtered_value_x
            

            # Operador de prewitt em Y:
            vizinhanca_y = img_array_x[y - 1:y + 2, x - 1:x + 2]
            
            filtered_value_y = round(np.sum(vizinhanca_y * matriz_y))
            filtered_value_y = np.clip(filtered_value_y, 0, 255)
            
            # Atribuir ao pixel correspondente na imagem filtrada
            imagem_filtrada_em_y[y, x] = filtered_value_y

    #Soma o resultado das duas operações
    imagem_filtrada = Operacoes.soma(imagem_filtrada_em_x, imagem_filtrada_em_y)

    # Converter a matriz filtrada de volta para imagem PIL
    imagem_filtrada_convertida = Image.fromarray(imagem_filtrada.astype('uint8'), 'L')

    return imagem_filtrada_convertida

def operador_sobel(imagem):
    # Criar uma cópia da imagem para aplicar o filtro
    imagem_filtrada_em_x = imagem.copy()
    imagem_filtrada_em_y = imagem.copy()

    height, width = imagem.shape
    
    img_array_x = np.array(imagem)
    img_array_y = np.array(imagem)


    #"Operador de Prewitt em X":
    matriz_x = [[-1, -2, -1],
               [ 0,  0,  0],
               [ 1,  2,  1]]
    #"Operador de Prewitt em Y":
    matriz_y = [[-1, 0, 1],
               [-2, 0, 2],
               [-1, 0, 1]]

    for y in range(1, height - 1):
        for x in range(1, width - 1):
            # Operador de prewitt em X:
            vizinhanca_x = img_array_x[y - 1:y + 2, x - 1:x + 2]
            
            filtered_value_x = round(np.sum(vizinhanca_x * matriz_x))
            filtered_value_x = np.clip(filtered_value_x, 0, 255) #Truncamento
            # Atribuir ao pixel correspondente na imagem filtrada
            imagem_filtrada_em_x[y, x] = filtered_value_x
            

            # Operador de prewitt em Y:
            vizinhanca_y = img_array_y[y - 1:y + 2, x - 1:x + 2]
            
            filtered_value_y = round(np.sum(vizinhanca_y * matriz_y))
            filtered_value_y = np.clip(filtered_value_y, 0, 255)
            
            # Atribuir ao pixel correspondente na imagem filtrada
            imagem_filtrada_em_y[y, x] = filtered_value_y

    #Soma o resultado das duas operações
    imagem_filtrada = Operacoes.soma(imagem_filtrada_em_x, imagem_filtrada_em_y)
    
    # Converter a matriz filtrada de volta para imagem PIL
    imagem_filtrada_convertida = Image.fromarray(imagem_filtrada.astype('uint8'), 'L')

    return imagem_filtrada_convertida

def operador_roberts(imagem):
    # Criar uma cópia da imagem para aplicar o filtro
    imagem_filtrada_em_x = imagem.copy()
    imagem_filtrada_em_y = imagem.copy()

    height, width = imagem.shape
    
    img_array = np.array(imagem)

    #"Operador de Roberts cruzado em X":
    matriz_x = np.array([[0,  0, 0],
                         [0,  1, 0],
                         [0, -1, 0]])
    
    #"Operador de Roberts cruzado em Y":
    matriz_y = np.array([[0,  0, 0],
                         [0,  1, -1],
                         [0,  0, 0]])

    for y in range(1, height - 1):
        for x in range(1, width - 1):
            # Extrair a vizinhança 3x3
            vizinhanca = img_array[y - 1:y + 2, x - 1:x + 2]
            
            filtered_value_x = round(np.sum(vizinhanca * matriz_x))
            filtered_value_x = np.clip(filtered_value_x, 0, 255) #Truncamento
            # Atribuir ao pixel correspondente na imagem filtrada
            imagem_filtrada_em_x[y, x] = filtered_value_x

            
            filtered_value_y = round(np.sum(vizinhanca * matriz_y))
            filtered_value_y = np.clip(filtered_value_y, 0, 255)
            
            # Atribuir ao pixel correspondente na imagem filtrada
            imagem_filtrada_em_y[y, x] = filtered_value_y

    #Soma o resultado das duas operações
    imagem_filtrada = Operacoes.soma(imagem_filtrada_em_x, imagem_filtrada_em_y)
    
    # Converter a matriz filtrada de volta para imagem PIL
    imagem_filtrada_convertida = Image.fromarray(imagem_filtrada.astype('uint8'), 'L')

    return imagem_filtrada_convertida

def operador_roberts_cruzado(imagem):
    # Criar uma cópia da imagem para aplicar o filtro
    imagem_filtrada_em_x = imagem.copy()
    imagem_filtrada_em_y = imagem.copy()

    height, width = imagem.shape
    
    img_array = np.array(imagem)

    #"Operador de Roberts cruzado em X":
    matriz_x = np.array([[0,  0,  0],
                         [0,  1,  0],
                         [0,  0, -1]])
    
    #"Operador de Roberts cruzado em Y":
    matriz_y = np.array([[0,  0,  0],
                         [0,  0,  1],
                         [0, -1,  0]])

    for y in range(1, height - 1):
        for x in range(1, width - 1):
            # Extrair a vizinhança 3x3
            vizinhanca = img_array[y - 1:y + 2, x - 1:x + 2]
            
            filtered_value_x = round(np.sum(vizinhanca * matriz_x))
            filtered_value_x = np.clip(filtered_value_x, 0, 255) #Truncamento
            # Atribuir ao pixel correspondente na imagem filtrada
            imagem_filtrada_em_x[y, x] = filtered_value_x
            
            filtered_value_y = round(np.sum(vizinhanca * matriz_y))
            filtered_value_y = np.clip(filtered_value_y, 0, 255)
            
            # Atribuir ao pixel correspondente na imagem filtrada
            imagem_filtrada_em_y[y, x] = filtered_value_y

    #Soma o resultado das duas operações
    imagem_filtrada = Operacoes.soma(imagem_filtrada_em_x, imagem_filtrada_em_y)
    
    # Converter a matriz filtrada de volta para imagem PIL
    imagem_filtrada_convertida = Image.fromarray(imagem_filtrada.astype('uint8'), 'L')

    return imagem_filtrada_convertida

def filtragem_alto_reforco(imagem, A):
    # Criar uma cópia da imagem para aplicar o filtro
    imagem_filtrada = imagem.copy()
    # Obter largura e altura da imagem
    height, width = imagem.shape
    # Converter imagem para matriz numpy
    img_array = np.array(imagem)
    
    W = 9 * A - 1
    print("W", W)
    matriz = [[-1,  -1,  -1],
             [-1,  W,  -1],
             [-1, -1,  -1]]

    # Aplicar o filtro
    for y in range(1, height - 1):
        for x in range(1, width - 1):
            # Extrair a vizinhança 3x3 do pixel atual (y-1 até y+2 seleciona as 
            # linhas 'y-1', 'y' e 'y+1' da matriz, o mesmo acontece com as colunas(x-1 até x+2))
            vizinhanca = img_array[y - 1:y + 2, x - 1:x + 2]
            
            filtered_value = round(np.sum(vizinhanca * matriz))
            
            imagem_filtrada[y, x] = filtered_value

    # Converter a matriz filtrada de volta para imagem PIL
    imagem_filtrada_convertida = Image.fromarray(imagem_filtrada.astype('uint8'), 'L')

    print(imagem_filtrada, "\n")

    return imagem_filtrada_convertida
