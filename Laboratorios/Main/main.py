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
import opengl3D


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
    tab_control.add(tab2, text='3D')
    #tab_control.add(tab2, text='3D - Ponto de Fuga')
    tab_control.add(tab3, text='3D - Isométrica')
    #tab_control.add(tab4, text='3D')
    #tab_control.add(tab5, text='3D - Ortográfica')
    tab_control.add(tab6, text='Retas e Círculo')

    
    tab_control.pack(expand=1, fill='both')

    opengl_frame.desenhar(tab1)
    opengl3D.desenhar(tab2)
    #opengl3Dframe_ponto_de_fuga.desenhar(tab2)
    opengl3Dframe_projecao_isometrica.desenhar(tab3)
    #opengl3Dframe_galpao_faces.desenhar(tab4)
    #opengl3Dframe_projecao_ortografica.desenhar(tab5)
    opengl2D_reta_circ.desenhar(tab6)

    root.mainloop()

if __name__ == '__main__':
    main()