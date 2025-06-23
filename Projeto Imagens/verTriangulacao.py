import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import Delaunay
from PIL import Image

def visualizar_morfismo(img0_path, img1_path, v_path, w_path, add_cantos=True):
    # Carregar imagens
    img0 = Image.open(img0_path).convert('L')
    img1 = Image.open(img1_path).convert('L')
    width, height = img0.size

    # Carregar pontos
    v = np.load(v_path)
    w = np.load(w_path)

    # Adicionar os 4 cantos
    corners = np.array([
        [0, 0], [width - 1, 0],
        [0, height - 1], [width - 1, height - 1]
    ], dtype=np.float32)
    v = np.vstack([v, corners])
    w = np.vstack([w, corners])

    # Triangulação Delaunay sobre v
    try:
        delaunay = Delaunay(v)
        triangles = delaunay.simplices
    except Exception as e:
        print(f"Erro na triangulação Delaunay: {e}")
        return

    # Visualização
    fig, axs = plt.subplots(1, 2, figsize=(14, 7))

    # Imagem inicial com triangulação
    axs[0].imshow(img0, cmap='gray')
    axs[0].triplot(v[:, 0], v[:, 1], triangles, color='lime')
    axs[0].scatter(v[:, 0], v[:, 1], color='red', s=10)
    axs[0].set_title("Imagem Inicial (v) + Triangulação")

    # Imagem final com os mesmos triângulos, mas em w
    axs[1].imshow(img1, cmap='gray')
    axs[1].triplot(w[:, 0], w[:, 1], triangles, color='orange')
    axs[1].scatter(w[:, 0], w[:, 1], color='blue', s=10)
    axs[1].set_title("Imagem Final (w) + Triângulos Correspondentes")

    plt.tight_layout()
    plt.show()

# --- Execução
if __name__ == "__main__":
    visualizar_morfismo(
        img0_path="./imagens/jessica-alba1.pgm",
        img1_path="./imagens/jessica-alba2.pgm",
        v_path="v_pontos.npy",
        w_path="w_pontos.npy",
        add_cantos=False  # Troque para False se já adicionou antes
    )