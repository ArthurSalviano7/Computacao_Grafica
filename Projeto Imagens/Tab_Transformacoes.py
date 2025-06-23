import tkinter as tk
from tkinter import ttk, filedialog
import customtkinter as ctk
from PIL import Image, ImageTk
import imageio
import numpy as np
import Transformacoes

# --- Variáveis Globais (para as instâncias de widgets de parâmetro) ---
# Inicialize-as como None ou vazias para que o 'grid_forget' inicial não dê erro
global param_labels, param_entries, frame_parametros_transf
param_labels = {}
param_entries = {}
frame_parametros_transf = None # Será o frame onde os parâmetros dinâmicos aparecerão

global imagem # Imagem carregada (numpy array)
global original_image # Imagem PIL carregada
global imagem_original_label, imagem_processada_label # Labels para exibir imagens
global filtro_val # StringVar do combobox

def open_image():
    file_path = filedialog.askopenfilename(filetypes=[("PGM Files", "*.pgm")])
    if file_path:
        global imagem, original_image
        imagem = imageio.imread(file_path) # numpy array
        original_image = Image.open(file_path) # PIL Image
        
        # Obter a largura (número de colunas) e altura (número de linhas) da imagem
        img_height, img_width = imagem.shape
        print(f"Dimensões da imagem: {img_height} x {img_width}")

        display_image(original_image, imagem_original_label) # Use a global label


def display_image(image, label):
    # Assegure-se de que a imagem esteja em um formato compatível com ImageTk (L ou RGB)
    if image.mode not in ['L', 'RGB', 'RGBA']:
        image = image.convert('L') # Ou 'RGB' se precisar de cores
    #image.thumbnail((300, 300))  # Reduzir o tamanho para caber na interface
    tk_image = ImageTk.PhotoImage(image)
    label.config(image=tk_image)
    label.image = tk_image # Essencial para evitar garbage collection


def aplicar_transf(): # Removi 'matriz' como parâmetro, pois não é usado aqui
    transf_selecionada = filtro_val.get() # Obtém a seleção do combobox
    
    # Adicione a validação da imagem carregada
    global imagem
    if 'imagem' not in globals() or imagem is None:
        print("Nenhuma imagem carregada para aplicar a transformação.")
        return

    if transf_selecionada == "Rotacao": # Nomes precisam ser exatos do Combobox
        try:
            angulo = float(param_entries.get("angulo").get())
            imagem_transformada = Transformacoes.rotacionar_imagem(imagem, angulo)
        except ValueError:
            print("Ângulo inválido. Insira um número.")
            return
    elif transf_selecionada == "Translacao":
        try:
            tx = float(param_entries.get("tx").get())
            ty = float(param_entries.get("ty").get())
            imagem_transformada = Transformacoes.translacao_imagem(imagem, tx, ty) # Supondo essa função
        except ValueError:
            print("Valores de Tx/Ty inválidos. Insira números.")
            return
    elif transf_selecionada == "Escala":
        try:
            sx = float(param_entries.get("sx").get())
            sy = float(param_entries.get("sy").get())
            imagem_transformada = Transformacoes.escala_imagem(imagem, sx, sy) # Supondo essa função
        except ValueError:
            print("Valores de Sx/Sy inválidos. Insira números.")
            return
    elif transf_selecionada == "Cisalhamento":
        try:
            # Cisalhamento em X (a, b) e Y (c, d). No livro, é mais comum A e B.
            # Vamos simplificar para Ax, Ay
            a = float(param_entries.get("a").get()) 
            b = float(param_entries.get("b").get())
            c = float(param_entries.get("c").get())
            d = float(param_entries.get("d").get())
            e = float(param_entries.get("e").get())
            f = float(param_entries.get("f").get())
            i = float(param_entries.get("i").get())
            j = float(param_entries.get("j").get())
            imagem_transformada = Transformacoes.cisalhar_imagem(imagem, a, b, c, d, e, f, i, j) # Supondo essa função
        except ValueError:
            print("Valores de cisalhamento inválidos. Insira números.")
            return
    elif transf_selecionada == "Reflexão (flip horizontal)":
        imagem_transformada = Transformacoes.flip_horizontal(imagem)
    elif transf_selecionada == "Reflexão (flip vertical)":
        imagem_transformada = Transformacoes.flip_vertical(imagem)
    
    # Exibir a imagem processada, se houver
    if imagem_transformada:
        display_image(imagem_transformada, imagem_processada_label)

def clear_param_widgets():
    """Remove todas as labels e entries de parâmetros do frame."""
    global param_labels, param_entries
    for widget in frame_parametros_transf.winfo_children():
        widget.destroy() # Destrói o widget
    param_labels.clear() # Limpa os dicionários de referência
    param_entries.clear()

def update_transform_parameters(event): # Renomeei para ser mais específico
    """
    Atualiza as caixas de inserção de parâmetros com base na transformação selecionada.
    """
    selected_transf = filtro_val.get() # Variável filtro_val é global

    clear_param_widgets() # Limpa widgets anteriores

    row_offset = 0 # Para posicionar os novos widgets

    if selected_transf == "Escala":
        param_labels["sx"] = tk.Label(frame_parametros_transf, text="Sx:")
        param_labels["sx"].grid(row=row_offset, column=0, padx=5, pady=2, sticky="w")
        param_entries["sx"] = tk.Entry(frame_parametros_transf, width=10)
        param_entries["sx"].grid(row=row_offset, column=1, padx=5, pady=2, sticky="w")
        
        row_offset += 1
        param_labels["sy"] = tk.Label(frame_parametros_transf, text="Sy:")
        param_labels["sy"].grid(row=row_offset, column=0, padx=5, pady=2, sticky="w")
        param_entries["sy"] = tk.Entry(frame_parametros_transf, width=10)
        param_entries["sy"].grid(row=row_offset, column=1, padx=5, pady=2, sticky="w")
        
    elif selected_transf == "Translacao":
        param_labels["tx"] = tk.Label(frame_parametros_transf, text="Tx:")
        param_labels["tx"].grid(row=row_offset, column=0, padx=5, pady=2, sticky="w")
        param_entries["tx"] = tk.Entry(frame_parametros_transf, width=10)
        param_entries["tx"].grid(row=row_offset, column=1, padx=5, pady=2, sticky="w")
        
        row_offset += 1
        param_labels["ty"] = tk.Label(frame_parametros_transf, text="Ty:")
        param_labels["ty"].grid(row=row_offset, column=0, padx=5, pady=2, sticky="w")
        param_entries["ty"] = tk.Entry(frame_parametros_transf, width=10)
        param_entries["ty"].grid(row=row_offset, column=1, padx=5, pady=2, sticky="w")

    elif selected_transf == "Rotacao":
        param_labels["angulo"] = tk.Label(frame_parametros_transf, text="Ângulo (graus):")
        param_labels["angulo"].grid(row=row_offset, column=0, padx=5, pady=2, sticky="w")
        param_entries["angulo"] = tk.Entry(frame_parametros_transf, width=10)
        param_entries["angulo"].grid(row=row_offset, column=1, padx=5, pady=2, sticky="w")

    elif selected_transf == "Cisalhamento":
        param_labels["a"] = tk.Label(frame_parametros_transf, text="a:")
        param_labels["a"].grid(row=row_offset, column=0, padx=5, pady=2, sticky="w")
        param_entries["a"] = tk.Entry(frame_parametros_transf, width=10)
        param_entries["a"].grid(row=row_offset, column=1, padx=5, pady=2, sticky="w", )
        param_entries["a"].insert(0, 1) # inserindo valor padrao para cisalhamento

        row_offset += 1
        param_labels["b"] = tk.Label(frame_parametros_transf, text="b:")
        param_labels["b"].grid(row=row_offset, column=0, padx=5, pady=2, sticky="w")
        param_entries["b"] = tk.Entry(frame_parametros_transf, width=10)
        param_entries["b"].grid(row=row_offset, column=1, padx=5, pady=2, sticky="w")
        param_entries["b"].insert(0, 0.5)

        row_offset += 1
        param_labels["c"] = tk.Label(frame_parametros_transf, text="c:")
        param_labels["c"].grid(row=row_offset, column=0, padx=5, pady=2, sticky="w")
        param_entries["c"] = tk.Entry(frame_parametros_transf, width=10)
        param_entries["c"].grid(row=row_offset, column=1, padx=5, pady=2, sticky="w")
        param_entries["c"].insert(0, 0)

        row_offset += 1
        param_labels["d"] = tk.Label(frame_parametros_transf, text="d:")
        param_labels["d"].grid(row=row_offset, column=0, padx=5, pady=2, sticky="w")
        param_entries["d"] = tk.Entry(frame_parametros_transf, width=10)
        param_entries["d"].grid(row=row_offset, column=1, padx=5, pady=2, sticky="w")
        param_entries["d"].insert(0, 0.5)

        row_offset=0
        param_labels["e"] = tk.Label(frame_parametros_transf, text="e:")
        param_labels["e"].grid(row=row_offset, column=2, padx=5, pady=2, sticky="w")
        param_entries["e"] = tk.Entry(frame_parametros_transf, width=10)
        param_entries["e"].grid(row=row_offset, column=3, padx=5, pady=2, sticky="w")
        param_entries["e"].insert(0, 1)

        row_offset += 1 
        param_labels["f"] = tk.Label(frame_parametros_transf, text="f:")
        param_labels["f"].grid(row=row_offset, column=2, padx=5, pady=2, sticky="w")
        param_entries["f"] = tk.Entry(frame_parametros_transf, width=10)
        param_entries["f"].grid(row=row_offset, column=3, padx=5, pady=2, sticky="w")
        param_entries["f"].insert(0, 0)

        row_offset += 1 
        param_labels["i"] = tk.Label(frame_parametros_transf, text="i:")
        param_labels["i"].grid(row=row_offset, column=2, padx=5, pady=2, sticky="w")
        param_entries["i"] = tk.Entry(frame_parametros_transf, width=10)
        param_entries["i"].grid(row=row_offset, column=3, padx=5, pady=2, sticky="w")
        param_entries["i"].insert(0, 0)

        row_offset += 1 
        param_labels["j"] = tk.Label(frame_parametros_transf, text="j:")
        param_labels["j"].grid(row=row_offset, column=2, padx=5, pady=2, sticky="w")
        param_entries["j"] = tk.Entry(frame_parametros_transf, width=10)
        param_entries["j"].grid(row=row_offset, column=3, padx=5, pady=2, sticky="w")
        param_entries["j"].insert(0, 0)

    # Se precisar de outros campos (como os que você mencionou "c, d" e "e, f, i, i"),
    # você precisará mapeá-los para os parâmetros da sua função de cisalhamento.
    # Por exemplo, se sua função Transformacoes.cisalhamento_imagem aceita 4 ou 6 parâmetros,
    # você criaria as entries correspondentes aqui.

    # definir valores padrão para as entries
    for key, entry_widget in param_entries.items():
        if key == "angulo": entry_widget.insert(0, "90")
        elif key == "sx" or key == "sy": entry_widget.insert(0, "1.5")
        elif key == "tx" or key == "ty": entry_widget.insert(0, "50")
        elif key == "ax" or key == "ay": entry_widget.insert(0, "0.2")

    # Isso substituirá a função atualizar_matriz_convolucao no combobox bind.
    # Se você ainda tiver filtros de convolução na mesma combobox, você precisará
    # refatorar para ter uma combobox para transformações e outra para filtros,
    # ou uma lógica mais complexa dentro de update_transform_parameters para distinguir.


# --- Função para mostrar a tela de Transformações (tab5) ---
def mostrar_tela(tab5): 
    global imagem_original_label, imagem_processada_label, filtro_val, frame_parametros_transf

    # Frame dentro da aba para organizar com grid
    frame_transformacoes = tk.Frame(tab5)
    frame_transformacoes.pack(expand=1, fill='both', padx=10, pady=10)

    # Labels para exibir as imagens
    imagem_original_label = tk.Label(frame_transformacoes) # Definindo a global
    imagem_original_label.grid(row=0, column=0, padx=10, pady=10)

    imagem_processada_label = tk.Label(frame_transformacoes) # Definindo a global
    imagem_processada_label.grid(row=0, column=8, padx=10, pady=10)
    
    # Botão para abrir a imagem 
    filter_button = tk.Button(frame_transformacoes, text="Selecionar Imagem", command=open_image)
    filter_button.grid(row=1, column=0, padx=10, pady=10)
    
    # Frame para o seletor de transformações, parâmetros e botão de aplicar
    global frame_meio # Já era global
    frame_meio = tk.Frame(frame_transformacoes)
    frame_meio.grid(row=0, column=1, rowspan=5, columnspan=7, pady=10)

    # Texto antes do seletor de transformações
    filter_label = tk.Label(frame_meio, text="Selecione a transformação:")
    filter_label.grid(row=0, column=0, padx=10, pady=5, sticky='w')

    # Seletor de transformações
    filtro_val = tk.StringVar(value="Rotacao") # Valor inicial para testar
    # Adicionei Escala, Translacao, Rotacao e Cisalhamento
    transform_options = ["Escala", "Translacao", "Rotacao", "Reflexão (flip horizontal)", "Reflexão (flip vertical)", "Cisalhamento"]
    filter_menu = ttk.Combobox(frame_meio, textvariable=filtro_val, values=transform_options, width=40)
    filter_menu.grid(row=1, column=0, padx=10, pady=5, sticky='nsew')
    # Binda a nova função de atualização de parâmetros
    filter_menu.bind("<<ComboboxSelected>>", update_transform_parameters)

    # Frame específico para os parâmetros da transformação
    # Este frame será limpo e preenchido dinamicamente
    frame_parametros_transf = tk.Frame(frame_meio, bd=2, relief="groove", padx=5, pady=5)
    frame_parametros_transf.grid(row=2, column=0, padx=10, pady=10, sticky="ew")

    # Botão para aplicar a transformação
    apply_button = tk.Button(frame_meio, text="Aplicar Transformação", command=aplicar_transf)
    apply_button.grid(row=7, column=0, padx=10, pady=10) # Ajuste a linha se necessário

    # Chamada inicial para mostrar os parâmetros da transformação padrão (Rotacao)
    update_transform_parameters(None) # Passa None para o evento, já que não é disparado por um bind