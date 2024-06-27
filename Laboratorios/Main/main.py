import tkinter as tk
from tkinter import ttk, filedialog
import customtkinter as ctk
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *


from opengl_frame import AppOgl
import opengl3Dframe_ponto_de_fuga
import opengl3Dframe_projecao_isometrica
import opengl3Dframe_galpao_faces
import opengl3Dframe_projecao_ortografica
import opengl2D_reta_circ
import opengl_frame


def main():
    root = tk.Tk()
    root.title("Computação Gráfica")
    root.geometry("1000x600")
    root.configure(background="#000C66")

    # Configuração das abas
    tab_control = ttk.Notebook(root)

    tab1 = tk.Frame(tab_control)
    tab2 = tk.Frame(tab_control)
    tab3 = tk.Frame(tab_control)
    tab4 = tk.Frame(tab_control)
    tab5 = tk.Frame(tab_control)
    tab6 = tk.Frame(tab_control)

    tab_control.add(tab1, text='2D')
    tab_control.add(tab2, text='3D - Ponto de Fuga')
    tab_control.add(tab3, text='3D - Isométrica')
    tab_control.add(tab4, text='3D - Mult. Faces')
    tab_control.add(tab5, text='3D - Ortográfica')
    tab_control.add(tab6, text='Retas e Círculo')

    
    tab_control.pack(expand=1, fill='both')

    opengl3Dframe_ponto_de_fuga.desenhar(tab2)
    opengl3Dframe_projecao_isometrica.desenhar(tab3)
    opengl3Dframe_galpao_faces.desenhar(tab4)
    opengl3Dframe_projecao_ortografica.desenhar(tab5)
    opengl2D_reta_circ.desenhar(tab6)


    # Frame para o lado esquerdo
    frame_left = tk.Frame(tab1, width=150, height=600)
    frame_left.configure(background="#000C66")
    frame_left.pack(side=tk.LEFT, fill=tk.BOTH, expand=False)

    # Frame intermediário1
    frame_mid1 = tk.Frame(tab1, width=75, height=600)
    frame_mid1.configure(background="#000C66")
    frame_mid1.pack(side=tk.LEFT, fill=tk.BOTH, expand=False)

    # Frame intermediário2
    frame_mid2 = tk.Frame(tab1, width=75, height=600)
    frame_mid2.configure(background="#000C66")
    frame_mid2.pack(side=tk.RIGHT, fill=tk.BOTH, expand=False)

    # Frame para o lado direito
    frame_right = tk.Frame(tab1, width=700, height=600)
    frame_right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=False)
    
    # Adicionar o frame OpenGL ao lado direito
    ogl_frame = AppOgl(frame_right, width=700, height=600)
    ogl_frame.pack(fill=tk.BOTH, expand=False)  # Definindo expand=False para manter o tamanho fixo
    ogl_frame.animate = 1

    # Botão para desenhar um quadrado, chama a função desejada ao apertar botão(command=funcao_executada)
    btn_desenhar_quadrado = tk.Button(frame_left, text="Desenhar\nQuadrado", command=lambda: ogl_frame.square_points(int(entry_tamanho.get())))
    btn_desenhar_quadrado.pack()

    # Caixa de entrada para o tamanho do quadrado
    entry_tamanho = ctk.CTkEntry(frame_left, placeholder_text="size", height=10, width=40)
    entry_tamanho.pack(pady=0)

    # Botão para Escala
    btn_scale = tk.Button(frame_left, text="Aplicar\nEscala", command=lambda: ogl_frame.escala(float(entry_sx.get()), float(entry_sy.get()))) #Converter para int sempre que chamar a função
    btn_scale.pack()

    # Caixa de entrada para Fator de escala Sx
    entry_sx = ctk.CTkEntry(frame_left, placeholder_text="sx", height=10, width=40)
    entry_sx.pack(pady=0)

    # Caixa de entrada para Fator de escala Sy
    entry_sy = ctk.CTkEntry(frame_left, placeholder_text="sy", height=10, width=40)
    entry_sy.pack(pady=0)

    # Botão para Translação
    btn_translate = tk.Button(frame_left, text="Aplicar\nTranslação", command=lambda: ogl_frame.translacao(int(entry_tx.get()), int(entry_ty.get())))
    btn_translate.pack()

    # Caixa de entrada para Translação Tx
    entry_tx = ctk.CTkEntry(frame_left, placeholder_text="Tx", height=10, width=40)
    entry_tx.pack(pady=0)

    # Caixa de entrada para Translação Ty
    entry_ty = ctk.CTkEntry(frame_left, placeholder_text="Ty", height=10, width=40)
    entry_ty.pack(pady=0)

    # Botão para Rotação
    btn_translate = tk.Button(frame_left, text="Aplicar\nRotação", command=lambda: ogl_frame.rotacao(int(entry_rot.get())))
    btn_translate.pack()

    # Caixa de entrada para ângulo de Rotação
    entry_rot = ctk.CTkEntry(frame_left, placeholder_text="ang", height=10, width=40)
    entry_rot.pack(pady=0)

    # Botão para Cisalhamento
    btn_translate = tk.Button(frame_left, text="Aplicar\nCisalhamento", command=lambda: ogl_frame.cisalhamento(int(entry_a.get()), int(entry_b.get())))
    btn_translate.pack()

    # Caixa de entrada para Fator A de cisalhamento
    entry_a = ctk.CTkEntry(frame_left, placeholder_text="a", height=10, width=40)
    entry_a.pack(pady=0)

    # Caixa de entrada para Fator B de cisalhamento
    entry_b = ctk.CTkEntry(frame_left, placeholder_text="b", height=10, width=40)
    entry_b.pack(pady=0)

    # Botão para Reflexão em X
    btn_translate = tk.Button(frame_mid1, text="Ref X", command=lambda: ogl_frame.reflexaoX())
    btn_translate.pack()

    # Botão para Reflexão em Y
    btn_translate = tk.Button(frame_mid1, text="Ref Y", command=lambda: ogl_frame.reflexaoY())
    btn_translate.pack()

    # Botão para Reflexão na Origem
    btn_translate = tk.Button(frame_mid1, text="Ref Origem", command=lambda: ogl_frame.reflexaoOrigem())
    btn_translate.pack()

    # Botão para Reflexão na Reta de 45 graus
    btn_translate = tk.Button(frame_mid1, text="Ref Reta 45", command=lambda: ogl_frame.reflexao45())
    btn_translate.pack()

    # Botão para Reflexão Qualquer
    btn_translate = tk.Button(frame_left, text="Aplicar\nReflexao\nQualquer", command=lambda: ogl_frame.reflexaoQualquer(float(entry_m.get()), float(entry_b_reta.get())))
    btn_translate.pack()

    # Caixa de entrada para M da Reta da Reflexão Qualquer
    entry_m = ctk.CTkEntry(frame_left, placeholder_text="m", height=10, width=40)
    entry_m.pack(pady=0)

    # Caixa de entrada para B da Reta da Reflexão Qualquer
    entry_b_reta = ctk.CTkEntry(frame_left, placeholder_text="b", height=10, width=40)
    entry_b_reta.pack(pady=0)

    # Botão para Limpar objetos desenhados
    btn_desenhar_circulo = tk.Button(frame_left, text="Limpar", command=lambda: ogl_frame.limpar())
    btn_desenhar_circulo.pack(pady=20)

    root.mainloop()

if __name__ == '__main__':
    main()