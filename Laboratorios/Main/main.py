import tkinter as tk
from tkinter import ttk, filedialog
import customtkinter as ctk
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

from opengl_frame import AppOgl
import opengl2D_heart_simulation
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

    tab_control.add(tab1, text='2D')
    tab_control.add(tab2, text='3D')
    tab_control.add(tab3, text='Simulação batimentos coração')
    tab_control.add(tab4, text='Retas e Círculo')

    tab_control.pack(expand=1, fill='both')

    opengl_frame.desenhar(tab1)
    opengl3D.desenhar(tab2)
    opengl2D_heart_simulation.desenhar(tab3)
    opengl2D_reta_circ.desenhar(tab4)

    root.mainloop()

if __name__ == '__main__':
    main()
