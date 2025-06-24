import numpy as np
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os
import re
from scipy.spatial import Delaunay # Fundamental para a triangulação

# Função para pegar o nivel de cinza do pixel e garantir que esteja
# dentro dos limites da imagem (no caso de x, y serem modificados após calculos)
def get_pixel_grayscale(image, x, y, width, height):
    # Garante que as coordenadas estejam dentro dos limites (0 - width-1)(0 - heigth-1)
    x_trunc = int(np.clip(x, 0, width - 1))
    y_trunc = int(np.clip(y, 0, height - 1))
    return image.getpixel((x_trunc, y_trunc))

# Função para determinar se um ponto está dentro do triangulo (Passo 7)
# p = u_pixel e tri_vertices = u_i(t), u_j(t), u_k(t) = [[x1,y1],[x2,y2],[x3,y3]]
def get_barycentric_coords(p, tri_vertices):
    """
    Calcula as coordenadas baricêntricas de um ponto p=(px,py) em relação a um triângulo
    cujos vértices são tri_vertices = [[x1,y1],[x2,y2],[x3,y3]].
    Retorna (ci, cj, ck) ou None se o triângulo for degenerado ou o ponto estiver fora.
    """
    p = np.array(p, dtype=np.float32)
    p1, p2, p3 = tri_vertices[0], tri_vertices[1], tri_vertices[2]

    # Calcular o dobro da área do triângulo de referência (denominador)
    # ou, de forma equivalente, o determinante da matriz formada pelos vetores das arestas.
    den = (p2[0] - p1[0]) * (p3[1] - p1[1]) - (p3[0] - p1[0]) * (p2[1] - p1[1])
    
    # Se o denominador é zero, o triângulo é degenerado (pontos colineares)
    if abs(den) < 1e-6: # Usar uma pequena tolerância para float comparison
        return None

    # Calcular as coordenadas baricêntricas cᵢ + cⱼ + cₖ = 1 (Equação 11)
    ci = ((p2[0] - p[0]) * (p3[1] - p[1]) - (p3[0] - p[0]) * (p2[1] - p[1])) / den
    cj = ((p3[0] - p[0]) * (p1[1] - p[1]) - (p1[0] - p[0]) * (p3[1] - p[1])) / den
    ck = 1.0 - ci - cj # Última coordenada

    # Pequena tolerância para pontos na borda do triângulo
    epsilon = 1e-5
    if not ((-epsilon <= ci <= 1 + epsilon) and \
            (-epsilon <= cj <= 1 + epsilon) and \
            (-epsilon <= ck <= 1 + epsilon)):
        return None # Ponto fora do triângulo (mesmo se Delaunay o encontrou)

    return ci, cj, ck


# --- Função principal de morfismo ---
def create_morphing(img0_path, img1_path, t_values, v_path='v_pontos.npy', w_path='w_pontos.npy',
                     output_folder='morfismo_output'):

    # Carregar imagens em modo 'L' (escala de cinza)
    try:
        img0 = Image.open(img0_path).convert('L') # Imagem inicial (rho0)
        img1 = Image.open(img1_path).convert('L') # Imagem final (rho1)
    except FileNotFoundError:
        print(f"Erro: Arquivo não encontrado. Verifique os caminhos: \n{img0_path}\n{img1_path}")
        return
    except Exception as e:
        print(f"Erro ao carregar imagens: {e}")
        return

    # Garante que as imagens tenham o mesmo tamanho
    if img0.size != img1.size:
        print(f"As imagens não têm o mesmo tamanho. Redimensionando a imagem final ({img1.size}) para ({img0.size}).")
        img1 = img1.resize(img0.size, Image.LANCZOS)

    width, height = img0.size

    # Carregar pontos clicados (características)
    try:
        v_features = np.load(v_path)
        w_features = np.load(w_path)
    except FileNotFoundError:
        print(f"Erro: Arquivos de pontos ({v_path} ou {w_path}) não encontrados.")
        print("Você precisa gerar esses arquivos primeiro, por exemplo, usando um script para clicar em pontos.")
        return
    
    if v_features.shape != w_features.shape:
        print("Erro: O número de pontos nos arquivos v_pontos.npy e w_pontos.npy é diferente.")
        return


    # Adicionar pontos de grade regulares para cobrir toda a imagem
    # Estes pontos da grade são adicionados aos conjuntos de pontos de AMBAS as imagens
    #grid_points = gerar_pontos_de_grade(width, height, spacing=20)
    corners = np.array([
            [0, 0], [width - 1, 0],
            [0, height - 1], [width - 1, height - 1]
        ], dtype=np.float32)
    
    # Combinar pontos de características e pontos da grade
    v_all = np.vstack([v_features, corners])
    w_all = np.vstack([w_features, corners])

    # Triangulação Delaunay sobre o conjunto de pontos da imagem inicial (v_all)
    try:
        tri = Delaunay(v_all)
        triangles_indices = tri.simplices # Retorna os índices dos vértices de cada triângulo
    except Exception as e:
        print(f"Erro na triangulação Delaunay. {e}")
        print("Certifique-se de que os pontos não são colineares ou muito próximos e que 'scipy' está instalado.")
        return


    # Cria a pasta de saída se não existir
    os.makedirs(output_folder, exist_ok=True)
    print(f"Pasta de saída criada/verificada: {output_folder}")

    # Valores de t a serem gerados
    # Incluí 0 e 1 para garantir que as imagens originais sejam geradas também,
    t_values_to_generate = t_values
    #t_values_to_generate = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]

    print("Iniciando geração das imagens de morfismo...")
    for t in t_values_to_generate:
        print(f"Gerando imagem para t = {t:.2f}...")
        
        # Criar nova imagem para o resultado deste t, em nível de cinza
        morphed_image = Image.new('L', (width, height))
        
        # Passo 4: Encontre os pontos de vértice u_i(t) para o morfismo da imagem
        u_all_t = (1 - t) * v_all + t * w_all

        # Iterar sobre cada pixel da imagem morfada
        for y in range(height):
            for x in range(width):
                u_pixel = np.array([x, y], dtype=np.float32) # O ponto 'u' do livro (pixel no quadro morfado)

                # Passo 6: Encontre o triângulo da triangulação ao qual u_pixel pertence
                # Usar tri.find_simplex pra isso.
                simplex_index = tri.find_simplex(u_pixel)
                
                if simplex_index == -1:
                    # Se o pixel não está em nenhum triângulo da triangulação
                    # faz uma mistura dos niveis de cinza originais.
                    rho0_u = get_pixel_grayscale(img0, x, y, width, height)
                    rho1_u = get_pixel_grayscale(img1, x, y, width, height)
                    rho_t_u = (1 - t) * rho0_u + t * rho1_u
                    morphed_image.putpixel((x, y), int(np.clip(rho_t_u, 0, 255)))
                    continue # Próximo pixel


                # Se o pixel está em um triângulo:
                indices_do_tri = triangles_indices[simplex_index] # Índices dos vértices do triângulo na lista v_all
                
                # Obter os vértices do triângulo atual no tempo t (u_i(t), u_j(t), u_k(t))
                u_tri_vertices = u_all_t[indices_do_tri]
                
                # Passo 7: Expresse u como uma combinação convexa de u_i(t), u_j(t), u_k(t)
                # Calcula as coordenadas baricêntricas do u_pixel em relação a u_tri_vertices
                bary_coords = get_barycentric_coords(u_pixel, u_tri_vertices)

                if bary_coords is None:
                    # Caso em que as coordenadas nao foram obtidas 
                    rho0_u = get_pixel_grayscale(img0, x, y, width, height)
                    rho1_u = get_pixel_grayscale(img1, x, y, width, height)
                    rho_t_u = (1 - t) * rho0_u + t * rho1_u # Determine a densidade de imagem e adiciona a imagem
                    morphed_image.putpixel((x, y), int(np.clip(rho_t_u, 0, 255)))
                    continue
                
                ci, cj, ck = bary_coords # c_i, c_j, c_k do livro

                # Passo 8: Determine a localização do ponto u nas imagens inicial e final
                # Usando as coordenadas baricêntricas e os vértices originais (v_i, v_j, v_k) e (w_i, w_j, w_k)
                v_tri_vertices = v_all[indices_do_tri]
                w_tri_vertices = w_all[indices_do_tri]

                # u = c_i * u_i(t) + c_j * u_j(t) + c_k * u_k(t)
                # v = c_i * v_i + c_j * v_j + c_k * v_k
                # w = c_i * w_i + c_j * w_j + c_k * w_k
                
                v_pixel_coords = ci * v_tri_vertices[0] + cj * v_tri_vertices[1] + ck * v_tri_vertices[2]
                w_pixel_coords = ci * w_tri_vertices[0] + cj * w_tri_vertices[1] + ck * w_tri_vertices[2]

                # Passo 9: Determine a densidade de imagem ρₜ(u)
                rho0_val = get_pixel_grayscale(img0, v_pixel_coords[0], v_pixel_coords[1], width, height)
                rho1_val = get_pixel_grayscale(img1, w_pixel_coords[0], w_pixel_coords[1], width, height)
                
                rho_t_u = (1 - t) * rho0_val + t * rho1_val
                
                # Definir o pixel na imagem resultante
                morphed_image.putpixel((x, y), int(np.clip(rho_t_u, 0, 255)))
        
        # Salva a imagem resultante
        output_path = os.path.join(output_folder, f"morphed_t_{t:.2f}.pgm")
        morphed_image.save(output_path)
        print(f"Imagem salva: {output_path}")

    print("\nProcesso de geração de morfismo concluído.")
    print(f"As imagens foram salvas na pasta: {output_folder}")

def display_image(image, label):
    image.thumbnail((300, 300))  # Reduzir o tamanho para caber na interface
    tk_image = ImageTk.PhotoImage(image)
    label.config(image=tk_image)
    label.image = tk_image

# --- função para exibir a tela de morfismo com o slider ---
def mostrar_tela_morfismo_viewer(tab4, image_folder="morfismo_output"):
    # Frame principal para organizar os widgets dentro da tab4
    main_frame = ttk.Frame(tab4, padding="10")
    main_frame.pack(expand=True, fill="both")

    # --- Carregar Imagens de Morfismo ---
    morphed_images = []
    frame_t_values = []
    
    image_files = sorted([f for f in os.listdir(image_folder) if f.startswith("morphed_t_") and f.endswith(".pgm")])

    for filename in image_files:
        filepath = os.path.join(image_folder, filename)
        try:
            img = Image.open(filepath)
            morphed_images.append(img)
            
            match = re.search(r'morphed_t_(\d+\.\d+)\.pgm', filename)
            if match:
                frame_t_values.append(float(match.group(1)))
            else:
                frame_t_values.append(0.0)
        except Exception as e:
            print(f"Erro ao carregar a imagem {filename}: {e}")
            
    # --- Widgets da Interface ---
    # Label para exibir a imagem
    image_label = tk.Label(main_frame)
    image_label.pack(pady=10)

    # Label para exibir o valor de t
    t_value_label = ttk.Label(main_frame, text="t = 0.00")
    t_value_label.pack(pady=5)

    # Função de atualização para o slider
    # Ela precisa de acesso aos 'morphed_images', 'frame_t_values', 'image_label', 't_value_label'
    def update_image_display(scale_value):
        try:
            # Scale retorna string, float, depois int
            frame_index = int(float(scale_value)) 
        except ValueError:
            frame_index = 0

        if 0 <= frame_index < len(morphed_images):
            current_image_pil = morphed_images[frame_index]
            current_t = frame_t_values[frame_index]

            tk_image = ImageTk.PhotoImage(current_image_pil)
            image_label.config(image=tk_image)
            image_label.image = tk_image

            t_value_label.config(text=f"t = {current_t:.2f}")
        else:
            print(f"Índice de frame inválido: {frame_index}")

    # Slider (Scale) para controlar o frame
    frame_slider = ttk.Scale(
        main_frame,
        from_=0,
        to_=len(morphed_images) - 1,
        orient="horizontal",
        command=update_image_display
    )
    frame_slider.pack(fill="x", padx=20, pady=10)

    # Exibir a primeira imagem ao iniciar
    update_image_display(0) # Inicia a exibição com o primeiro frame

# --- Execução do Morfismo ---
def mostrar_tela(tab4):
    # Caminhos para suas imagens PGM de entrada
    img_start = './imagens/jessica-alba1.pgm'
    img_final = './imagens/jessica-alba2.pgm'

    img1 = Image.open(img_start)
    img2 = Image.open(img_final)
    
    # Mudar aqui os valores de t
    #t = [0.0, 0.25, 0.50, 0.75, 1.0]
    t = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]

    # Chama a função para criar morfismo
    # Pode desativar após criar imagens
    create_morphing(img_start, img_final, t_values=t)

    mostrar_tela_morfismo_viewer(tab4)