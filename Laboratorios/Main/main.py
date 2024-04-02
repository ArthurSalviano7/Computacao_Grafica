import tkinter as tk
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

from opengl_frame import AppOgl


def main():
    root = tk.Tk()
    root.geometry("1000x600")
    root.configure(background="#000C66")

    # Frame para o lado esquerdo
    frame_left = tk.Frame(root, width=300, height=600)
    frame_left.configure(background="#000C66")
    frame_left.pack(side=tk.LEFT, fill=tk.BOTH, expand=False)

    # Frame para o lado direito
    frame_right = tk.Frame(root, width=700, height=600)
    frame_right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=False)
    
    # Adicionar o frame OpenGL ao lado direito
    ogl_frame = AppOgl(frame_right, width=700, height=600)
    ogl_frame.pack(fill=tk.BOTH, expand=False)  # Definindo expand=False para manter o tamanho fixo

    ogl_frame.animate = 1

    # Caixa de entrada para o tamanho do quadrado
    lbl_tamanho = tk.Label(frame_left, text="Tamanho do Quadrado:")
    lbl_tamanho.pack(pady=5)
    entry_tamanho = tk.Entry(frame_left)
    entry_tamanho.pack(pady=5)

    # Botão para desenhar um quadrado, chama a função desejada ao apertar botão(command=funcao_executada)
    btn_desenhar_quadrado = tk.Button(frame_left, text="Desenhar", command=lambda: ogl_frame.square_points(int(entry_tamanho.get())))
    btn_desenhar_quadrado.pack()

    # Caixa de entrada para escala
    lbl_escala = tk.Label(frame_left, text="Escala:")
    lbl_escala.pack(pady=10)
    entry_escala = tk.Entry(frame_left)
    entry_escala.pack(pady=5)

    # Botão para Escala
    btn_escala = tk.Button(frame_left, text="Aplicar", command=lambda: ogl_frame.escala(int(entry_escala.get())))
    btn_escala.pack()



    root.mainloop()

if __name__ == '__main__':
    main()