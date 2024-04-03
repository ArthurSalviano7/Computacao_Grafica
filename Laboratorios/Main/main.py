import tkinter as tk
import customtkinter as ctk
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
    btn_scale = tk.Button(frame_left, text="Aplicar", command=lambda: ogl_frame.escala(float(entry_escala.get()))) #Converter para int sempre que chamar a função
    btn_scale.pack()

    # Caixa de entrada para Translação Tx
    lbl_tx = tk.Label(frame_left, text="Translação:")
    lbl_tx.pack(pady=10)
    entry_tx = ctk.CTkEntry(frame_left, placeholder_text="Tx", height=30, width=40)
    entry_tx.pack(pady=5)

    # Caixa de entrada para Translação Ty
    entry_ty = ctk.CTkEntry(frame_left, placeholder_text="Ty", height=30, width=40)
    entry_ty.pack(pady=5)

    # Botão para Translação
    btn_translate = tk.Button(frame_left, text="Aplicar", command=lambda: ogl_frame.translacao(int(entry_tx.get()), int(entry_ty.get())))
    btn_translate.pack()

    # Caixa de entrada para Rotacao
    lbl_rot = tk.Label(frame_left, text="Rotação:")
    lbl_rot.pack(pady=10)
    entry_rot = ctk.CTkEntry(frame_left, placeholder_text="ang", height=30, width=40)
    entry_rot.pack(pady=5)

    # Botão para Rotação
    btn_translate = tk.Button(frame_left, text="Aplicar", command=lambda: ogl_frame.rotacao(int(entry_rot.get())))
    btn_translate.pack()

    # Label para Reflexao
    lbl_rot = tk.Label(frame_left, text="Reflexao:")
    lbl_rot.pack(pady=10)
    
    # Botão para Reflexão em x
    btn_translate = tk.Button(frame_left, text="Em X", command=lambda: ogl_frame.reflexaoX(int(entry_rot.get())))
    btn_translate.pack()

    btn_translate = tk.Button(frame_left, text="Em Y", command=lambda: ogl_frame.reflexaoY(int(entry_rot.get())))
    btn_translate.pack()

    btn_translate = tk.Button(frame_left, text="Em X", command=lambda: ogl_frame.reflexao_origem(int(entry_rot.get())))
    btn_translate.pack()

    btn_translate = tk.Button(frame_left, text="Em Y", command=lambda: ogl_frame.reflexao_reta(int(entry_rot.get())))
    btn_translate.pack()


    root.mainloop()

if __name__ == '__main__':
    main()