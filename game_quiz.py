import sqlite3
import customtkinter as ctk
import pandas as pd
from tkinter import messagebox
from random import randint
import time
import os


class MenuPrincipal:

    def __init__(self, master):
        self.master = master
        self.master.configure(fg_color=COR_FUNDO)
        self.conexao = sqlite3.connect("database/quiz_game.db")
        self.cursor = self.conexao.cursor()

        self.interface_menu()


    def interface_menu(self):
        # Limpar a tela
        for widget in self.master.winfo_children():
            widget.destroy()
            
        # Título da página
        self.lb_titulo = ctk.CTkLabel(self.master, text="Configuração", 
                                    font=(FONTE_PADRAO, TAMANHO_FONTE_TITULO), text_color=COR_TEXTO)
        self.lb_titulo.place(relx=0.5, rely=0.2, anchor='center')

        # Configuração dos botões
        button_configs = {
            'width': 200,
            'height': 40,
            'fg_color': "#333333",
            'text_color': "white",
            'hover_color': "#444444",
            'font': ("Arial", 14),
            'corner_radius': 10
        }

        # Botões principais
        self.btn_iniciar = ctk.CTkButton(self.master, text="Iniciar",
                                             **button_configs)
        self.btn_iniciar.place(relx=0.5, rely=0.4, anchor='center')

        self.btn_config_jogo = ctk.CTkButton(self.master, text="Configurações do Jogo",
                                             **button_configs)
        self.btn_config_jogo.place(relx=0.5, rely=0.5, anchor='center')

        self.btn_jogador = ctk.CTkButton(self.master, text="Jogador",
                                             **button_configs)
        self.btn_jogador.place(relx=0.5, rely=0.6, anchor='center')

        self.btn_sair = ctk.CTkButton(self.master, text="Sair",
                                             **button_configs)
        self.btn_sair.place(relx=0.5, rely=0.7, anchor='center')














if __name__ == "__main__":
    app = ctk.CTk()
    app.geometry("1280x720")
    app.title("Quiz game")

    FONTE_PADRAO = "Arial"
    TAMANHO_FONTE_TITULO = 24
    TAMANHO_FONTE_TEXTO = 16
    TAMANHO_FONTE_NORMAL = 14
    COR_TEXTO = "white"
    COR_FUNDO = "#242424"
    COR_BOTAO = "#333333"
    COR_TEXTO_BOTAO = "white"
    COR_BOTAO_HOVER = "#444444"
    BUTTON_WIDTH = 200
    BUTTON_HEIGHT = 40
    CORNER_RADIUS = 10

    menu_principal = MenuPrincipal(app)
    app.mainloop()