"""
Quiz Game - Sistema de Quiz Interativo
====================================

Este projeto implementa um sistema de quiz interativo usando Python, CustomTkinter para interface gráfica 
e SQLite para persistência de dados. O sistema oferece diferentes níveis de dificuldade, sistema de 
pontuação dinâmico e gerenciamento completo de jogadores e questões.

Características Principais:
-------------------------
- Múltiplos níveis de dificuldade (Fácil, Médio, Difícil)
- Gerenciamento de jogadores e histórico de pontuações
- Temporizador visual para questões
- Configurações personalizáveis (tempo, número de questões)

Estrutura do Sistema:
-------------------
- MenuPrincipal: Interface inicial e navegação
- Questionario: Implementa a lógica do quiz e pontuação
- PaginaResposta: Exibe resultados e atualiza estatísticas
- PaginaJogador: Gerencia cadastro e pontuações
- SelecaoDificuldade: Controla níveis de dificuldade

Sistema de Pontuação:
-------------------
- Fácil: questões de 5 e 10 pontos
- Médio: questões de 10, 20 e 40 pontos
- Difícil: questões de 40 e 80 pontos

Desenvolvido por:
---------------
- Anderson Gabriel da Silva Campos
- João Pedro Marques Boa Sorte Soares
- Eduardo Moura e Silva
"""

import sqlite3
import customtkinter as ctk
from tkinter import messagebox
from random import randint, choices, choice
import time
import os
from config_global import *

# A classe MenuPrincipal é implementada para criar e gerenciar a interface principal do jogo, fornecendo acesso às diferentes funcionalidades através de botões
class MenuPrincipal:
    # A função __init__ é implementada para inicializar a janela principal e estabelecer conexão com o banco de dados
    def __init__(self, master):
        self.master = master
        self.master.configure(fg_color=COR_FUNDO)
        self.conexao = sqlite3.connect("database/quiz_game.db")
        self.cursor = self.conexao.cursor()
        self.interface_menu()

    # A função interface_menu é implementada para criar e posicionar todos os elementos visuais do menu principal, incluindo título e botões de navegação
    def interface_menu(self):
        for widget in self.master.winfo_children():
            widget.destroy()
            
        self.lb_titulo = ctk.CTkLabel(self.master, text="Quiz Game", 
                                    font=(FONTE_PADRAO, TAMANHO_FONTE_TITULO), text_color=COR_TEXTO)
        self.lb_titulo.place(relx=0.5, rely=0.2, anchor='center')

        self.lb_desenvolvido = ctk.CTkLabel(
            self.master,
            text="Desenvolvido por:",
            font=(FONTE_PADRAO, TAMANHO_FONTE_NORMAL, "bold"),
            text_color=COR_TEXTO
        )
        self.lb_desenvolvido.place(relx=0.95, rely=0.85, anchor='se')


        self.lb_nomes = ctk.CTkLabel(
            self.master,
            text="Anderson Gabriel\nJoão Pedro\nEduardo Moura",
            font=(FONTE_PADRAO, TAMANHO_FONTE_NORMAL),  
            text_color=COR_TEXTO,
            justify="right"
        )
        self.lb_nomes.place(relx=0.95, rely=0.95, anchor='se')

        # Configuração padrão de botões usando dicionário 
        button_configs = {
            'width': BUTTON_WIDTH,
            'height': BUTTON_HEIGHT,
            'fg_color': COR_BOTAO,
            'text_color': COR_TEXTO_BOTAO,
            'hover_color': COR_BOTAO_HOVER,
            'font': (FONTE_PADRAO, TAMANHO_FONTE_NORMAL),
            'corner_radius': CORNER_RADIUS
        }

        self.btn_iniciar = ctk.CTkButton(self.master, text="Iniciar",
                                        command=self.iniciar_questionario,
                                        **button_configs)
        self.btn_iniciar.place(relx=0.5, rely=0.4, anchor='center')

        self.btn_config = ctk.CTkButton(self.master, text="Configurações",
                                        command=self.abrir_configuracao,
                                        **button_configs)
        self.btn_config.place(relx=0.5, rely=0.5, anchor='center')

        self.btn_jogador = ctk.CTkButton(self.master, text="Jogador",
                                        command=self.abrir_jogador,
                                        **button_configs)
        self.btn_jogador.place(relx=0.5, rely=0.6, anchor='center')

        self.btn_sair = ctk.CTkButton(self.master, text="Sair",
                                     command=self.master.quit,
                                     **button_configs)
        self.btn_sair.place(relx=0.5, rely=0.7, anchor='center')

    # A função iniciar_questionario é implementada para limpar a tela atual e iniciar a seleção de dificuldade do quiz
    def iniciar_questionario(self):
        for widget in self.master.winfo_children():
            widget.destroy()
        SelecaoDificuldade(self.master)

    # A função abrir_configuracao é implementada para limpar a tela atual e abrir a página de configurações do jogo
    def abrir_configuracao(self):
        for widget in self.master.winfo_children():
            widget.destroy()
        from configuracao import Configuracao
        Configuracao(self.master)
    def __del__(self):
        if hasattr(self, 'conexao'):
            self.conexao.close()
    # A função abrir_jogador é implementada para limpar a tela atual e abrir a página de seleção/gestão de jogadores
    def abrir_jogador(self):
        for widget in self.master.winfo_children():
            widget.destroy()
        PaginaJogador(self.master)

    def __del__(self):
        if hasattr(self, 'conexao'):
            self.conexao.close()

# A classe SelecaoDificuldade é implementada para permitir que o usuário escolha o nível de dificuldade do quiz antes de iniciá-lo
class SelecaoDificuldade:
    # A função __init__ é implementada para inicializar a interface de seleção de dificuldade e estabelecer conexão com o banco de dados
    def __init__(self, master):
        self.master = master
        self.master.configure(fg_color=COR_FUNDO)
        self.conexao = sqlite3.connect("database/quiz_game.db")
        self.cursor = self.conexao.cursor()
        
        self.lb_titulo = ctk.CTkLabel(
            self.master,
            text="Selecione a Dificuldade",
            font=(FONTE_PADRAO, TAMANHO_FONTE_TITULO),
            text_color=COR_TEXTO
        )
        self.lb_titulo.place(relx=0.5, rely=0.2, anchor='center')

        button_configs = {
            'width': BUTTON_WIDTH,
            'height': BUTTON_HEIGHT,
            'fg_color': COR_BOTAO,
            'text_color': COR_TEXTO_BOTAO,
            'hover_color': COR_BOTAO_HOVER,
            'font': (FONTE_PADRAO, TAMANHO_FONTE_NORMAL),
            'corner_radius': CORNER_RADIUS
        }

        self.btn_facil = ctk.CTkButton(
            self.master,
            text="Fácil",
            command=lambda: self.iniciar_quiz("facil"),
            **button_configs
        )
        self.btn_facil.place(relx=0.5, rely=0.4, anchor='center')

        self.btn_medio = ctk.CTkButton(
            self.master,
            text="Médio",
            command=lambda: self.iniciar_quiz("medio"),
            **button_configs
        )
        self.btn_medio.place(relx=0.5, rely=0.5, anchor='center')

        self.btn_dificil = ctk.CTkButton(
            self.master,
            text="Difícil",
            command=lambda: self.iniciar_quiz("dificil"),
            **button_configs
        )
        self.btn_dificil.place(relx=0.5, rely=0.6, anchor='center')

        self.btn_voltar = ctk.CTkButton(
            self.master,
            text="Voltar",
            command=self.voltar_menu,
            **button_configs
        )
        self.btn_voltar.place(relx=0.5, rely=0.7, anchor='center')

    # A função iniciar_quiz é implementada para buscar as configurações do jogo e iniciar o questionário com a dificuldade selecionada
    def iniciar_quiz(self, dificuldade):
        self.cursor.execute("SELECT numero_questoes, tempo_questao FROM configuracao")
        config = self.cursor.fetchone()
        if config:
            num_questoes, tempo_questao = config
        else:
            num_questoes, tempo_questao = 5, 30

        for widget in self.master.winfo_children():
            widget.destroy()
        Questionario(self.master, num_questoes, tempo_questao, dificuldade)

    # A função voltar_menu é implementada para retornar à tela do menu principal
    def voltar_menu(self):
        for widget in self.master.winfo_children():
            widget.destroy()
        MenuPrincipal(self.master)

    def __del__(self):
        if hasattr(self, 'conexao'):
            self.conexao.close()

# A classe Questionario é implementada para gerenciar a execução do quiz,  incluindo apresentação das questões, temporizador e coleta de respostas
class Questionario:
    # A função __init__ é implementada para inicializar o questionário com as configurações específicas de número de questões, tempo e dificuldade
    def __init__(self, master, num_questoes=5, tempo_questao=30, dificuldade="medio"):
        self.master = master
        self.master.configure(fg_color=COR_FUNDO)
        self.conexao = sqlite3.connect("database/quiz_game.db")
        self.cursor = self.conexao.cursor()

        self.cursor.execute("SELECT * FROM perguntas")
        self.questoes = self.cursor.fetchall()

        self.controle = 0
        self.respostas = []
        self.num_questoes = min(num_questoes, len(self.questoes))
        self.tempo_questao = tempo_questao
        self.dificuldade = dificuldade
        
        self.indices_questoes = self.gerar_indices_aleatorios()

        self.lb_enunciado = ctk.CTkLabel(self.master, text="", text_color=COR_TEXTO, 
                                        wraplength=WINDOW_WIDTH-40, justify="left",
                                        font=(FONTE_PADRAO, TAMANHO_FONTE_NORMAL))
        self.lb_enunciado.place(x=20, y=20)

        self.radio_var = ctk.IntVar(value=-1)
        self.radiob_alternativas = []
        for i in range(5):
            rb = ctk.CTkRadioButton(self.master, text="", variable=self.radio_var, value=i,
                                   text_color=COR_TEXTO, fg_color=COR_BOTAO,
                                   font=(FONTE_PADRAO, TAMANHO_FONTE_NORMAL))
            self.radiob_alternativas.append(rb)
            rb.place(x=20, y=100 + i*50)

        self.lb_feedback = ctk.CTkLabel(self.master, text="", text_color=COR_TEXTO,
                                      font=(FONTE_PADRAO, TAMANHO_FONTE_NORMAL))
        self.lb_feedback.place(x=20, y=WINDOW_HEIGHT-200)

        self.progress_bar = ctk.CTkProgressBar(self.master, width=WINDOW_WIDTH-40, height=20)
        self.progress_bar.place(x=20, y=WINDOW_HEIGHT-150)
        self.progress_bar.set(0)

        self.timer = None
        self.is_running = True

        button_configs = {
            'width': BUTTON_WIDTH,
            'height': BUTTON_HEIGHT,
            'fg_color': COR_BOTAO,
            'text_color': COR_TEXTO_BOTAO,
            'hover_color': COR_BOTAO_HOVER,
            'font': (FONTE_PADRAO, TAMANHO_FONTE_NORMAL),
            'corner_radius': CORNER_RADIUS
        }

        self.btn_proximo = ctk.CTkButton(self.master, text="Próximo", 
                                        command=self.pegar_resposta, **button_configs)
        self.btn_proximo.place(x=WINDOW_WIDTH-20, y=WINDOW_HEIGHT-20, anchor='se')

        self.btn_sair = ctk.CTkButton(self.master, text="Sair", 
                                     command=self.sair, **button_configs)
        self.btn_sair.place(x=20, y=WINDOW_HEIGHT-20, anchor='sw')

        self.atualizar_questao()

    # A função gerar_indices_aleatorios é implementada para selecionar questões aleatórias baseadas na dificuldade escolhida, usando um sistema de pesos
    def gerar_indices_aleatorios(self):
        # Mapeamento de pontuações para níveis de dificuldade
        niveis_por_pontos = {
            5: 1,    # 5 pontos = nível 1 (muito fácil)
            10: 2,   # 10 pontos = nível 2 (fácil)
            20: 3,   # 20 pontos = nível 3 (médio)
            40: 4,   # 40 pontos = nível 4 (difícil)
            80: 5    # 80 pontos = nível 5 (muito difícil)
        }
        
        # Define quais pontuações são permitidas para cada dificuldade
        pontos_permitidos = {
            "facil": [5, 10],           # Fácil: questões de 5 e 10 pontos
            "medio": [10, 20, 40],       # Médio: questões de 10, 20 e 40 pontos
            "dificil": [40, 80]          # Difícil: questões de 40 e 80 pontos
        }
        
        indices = []
        questoes_disponiveis = []
        
        # Filtra as questões pela pontuação permitida
        for i, questao in enumerate(self.questoes):
            pontos = int(questao[8])  # Pontuação da questão
            if pontos in pontos_permitidos[self.dificuldade]:
                questoes_disponiveis.append(i)
        
        # Se não houver questões suficientes, inclui questões do próximo nível
        if len(questoes_disponiveis) < self.num_questoes:
            print(f"Aviso: Não há questões suficientes para o nível {self.dificuldade}")
            # Adiciona todas as questões como opção
            questoes_disponiveis = list(range(len(self.questoes)))
        
        # Seleciona aleatoriamente as questões necessárias
        while len(indices) < self.num_questoes and questoes_disponiveis:
            indice = choice(questoes_disponiveis)
            indices.append(indice)
            questoes_disponiveis.remove(indice)
        
        return indices

    # A função atualizar_questao é implementada para exibir a próxima questão e suas alternativas, além de reiniciar o temporizador
    def atualizar_questao(self):
        indice_questao = self.indices_questoes[self.controle]
        questao_atual = self.questoes[indice_questao]
        
        self.lb_enunciado.configure(text=f"{self.controle+1}. {questao_atual[1]}")
        
        alternativas = [questao_atual[2], questao_atual[3], questao_atual[4], 
                       questao_atual[5], questao_atual[6]]
        
        for i, rb in enumerate(self.radiob_alternativas):
            rb.configure(text=alternativas[i])
            
        self.radio_var.set(value=-1)
        self.lb_feedback.configure(text="")
        self.btn_proximo.configure(text="Responder", command=self.pegar_resposta)
        self.iniciar_temporizador()

    # A função pegar_resposta é implementada para verificar a resposta selecionada, fornecer feedback e atualizar o placar
    def pegar_resposta(self, tempo_esgotado=False):
        if self.timer:
            self.master.after_cancel(self.timer)
            self.timer = None

        if tempo_esgotado:
            resposta_selecionada = -1
        else:
            resposta_selecionada = self.radio_var.get()
            if resposta_selecionada == -1:
                messagebox.showwarning("Aviso", "Por favor, selecione uma alternativa antes de prosseguir.")
                self.iniciar_temporizador()
                return

        indice_questao = self.indices_questoes[self.controle]
        questao_atual = self.questoes[indice_questao]
        resposta_correta = int(questao_atual[7])  
        
        if resposta_selecionada != -1:
            if resposta_selecionada == resposta_correta:
                self.lb_feedback.configure(text="Resposta correta!", text_color="green")
            else:
                self.lb_feedback.configure(text=f"Resposta incorreta. A resposta correta era: {questao_atual[resposta_correta + 2]}", 
                                         text_color="red")
        else:
            self.lb_feedback.configure(text="Tempo esgotado! Nenhuma resposta selecionada.", 
                                     text_color="orange")

        self.respostas.append((indice_questao, resposta_selecionada))
        self.btn_proximo.configure(text="Próxima questão", command=self.proxima_questao)

    # A função mostrar_resultados é implementada para exibir a tela final com o desempenho do jogador após todas as questões
    def mostrar_resultados(self):
        self.is_running = False
        if self.timer:
            self.master.after_cancel(self.timer)
            self.timer = None
            
        for widget in self.master.winfo_children():
            widget.destroy()
        PaginaResposta(self.master, self.respostas, self.questoes)

    # A função sair é implementada para sair do quiz e retornar ao menu principal
    def sair(self):
        self.is_running = False  
        if self.timer:
            self.master.after_cancel(self.timer)
            self.timer = None
        if hasattr(self, 'conexao'):
            self.conexao.close()
        for widget in self.master.winfo_children():
            widget.destroy()
        MenuPrincipal(self.master)

    def __del__(self):
        if hasattr(self, 'conexao'):
            self.conexao.close()

    # A função proxima_questao é implementada para avançar para a próxima questão
    def proxima_questao(self):
        self.controle += 1
        if self.controle < self.num_questoes:
            self.atualizar_questao()
        else:
            self.is_running = False  
            self.mostrar_resultados()

    # A função iniciar_temporizador é implementada para iniciar o temporizador
    def iniciar_temporizador(self):
        self.progress_bar.set(0)
        self.atualizar_temporizador()

    # A função atualizar_temporizador é implementada para atualizar o temporizador
    def atualizar_temporizador(self):
        if not self.is_running:
            return

        valor_atual = self.progress_bar.get()
        if valor_atual < 1:
            try:
                self.progress_bar.set(valor_atual + 0.1/self.tempo_questao)   
                self.timer = self.master.after(100, self.atualizar_temporizador)  
            except Exception:
                pass
        else:
            self.pegar_resposta(tempo_esgotado=True)

# A classe PaginaResposta é implementada para mostrar os resultados finais do quiz e atualizar a pontuação do jogador no banco de dados
class PaginaResposta:
    # A função __init__ é implementada para calcular e exibir os resultados, além de atualizar as estatísticas do jogador
    def __init__(self, master, respostas, questoes):
        self.master = master
        self.master.configure(fg_color=COR_FUNDO)
        self.conexao = sqlite3.connect("database/quiz_game.db")
        self.cursor = self.conexao.cursor()

        self.corretas = 0
        pontos_totais = 0
        
        for indice_questao, resposta in respostas:
            if resposta != -1:  
                questao = questoes[indice_questao]
                resposta_correta = int(questao[7])
                if resposta == resposta_correta:
                    self.corretas += 1
                    pontos_totais += int(questao[8])

        self.cursor.execute("SELECT jogador_atual FROM configuracao")
        jogador_atual_id = self.cursor.fetchone()[0]
        
        if jogador_atual_id:
            self.cursor.execute("""
                UPDATE jogadores 
                SET pontos = pontos + ?,
                    acertos = acertos + ?,
                    erros = erros + ?
                WHERE id = ?
            """, (pontos_totais, self.corretas, len(respostas) - self.corretas, jogador_atual_id))
            self.conexao.commit()

        self.lb_titulo = ctk.CTkLabel(
            self.master, 
            text="Resultados", 
            font=(FONTE_PADRAO, TAMANHO_FONTE_TITULO), 
            text_color=COR_TEXTO
        )
        self.lb_titulo.place(relx=0.5, rely=0.3, anchor='center')

        resultado_texto = f"Você acertou {self.corretas} de {len(respostas)} questões!"
        if jogador_atual_id:  
            resultado_texto += f"\nPontos ganhos: {pontos_totais}"
        
        self.lb_resultado = ctk.CTkLabel(
            self.master, 
            text=resultado_texto,
            font=(FONTE_PADRAO, TAMANHO_FONTE_NORMAL), 
            text_color=COR_TEXTO
        )
        self.lb_resultado.place(relx=0.5, rely=0.5, anchor='center')

        button_configs = {
            'width': BUTTON_WIDTH,
            'height': BUTTON_HEIGHT,
            'fg_color': COR_BOTAO,
            'text_color': COR_TEXTO_BOTAO,
            'hover_color': COR_BOTAO_HOVER,
            'font': (FONTE_PADRAO, TAMANHO_FONTE_NORMAL),
            'corner_radius': CORNER_RADIUS
        }

        self.btn_voltar = ctk.CTkButton(
            self.master, 
            text="Voltar ao Menu", 
            command=self.voltar_menu,
            **button_configs
        )
        self.btn_voltar.place(relx=0.5, rely=0.7, anchor='center')

    # A função voltar_menu é implementada para retornar ao menu principal após a visualização dos resultados
    def voltar_menu(self):
        x = self.master.winfo_x()
        y = self.master.winfo_y()
        
        if hasattr(self, 'conexao'):
            self.conexao.close()
            
        for widget in self.master.winfo_children():
            widget.destroy()
            
        MenuPrincipal(self.master) 
 
    def __del__(self):
        if hasattr(self, 'conexao'):
            self.conexao.close()

# A classe PaginaJogador é implementada para gerenciar a seleção e visualização dos jogadores cadastrados
class PaginaJogador:
    # A função __init__ é implementada para inicializar a interface de gerenciamento de jogadores
    def __init__(self, master):
        self.master = master
        self.master.configure(fg_color=COR_FUNDO)
        self.conexao = sqlite3.connect("database/quiz_game.db")
        self.cursor = self.conexao.cursor()
        self.interface_jogador()

    # A função interface_jogador é implementada para criar a interface visual com a lista de jogadores e suas pontuações
    def interface_jogador(self):
        self.lb_titulo = ctk.CTkLabel(
            self.master, 
            text="Seleção de Jogador",
            font=(FONTE_PADRAO, TAMANHO_FONTE_TITULO),
            text_color=COR_TEXTO
        )
        self.lb_titulo.place(relx=0.5, rely=0.1, anchor='center')

        self.frame_jogadores = ctk.CTkScrollableFrame(
            self.master,
            width=400,
            height=400,
            fg_color=COR_FUNDO
        )
        self.frame_jogadores.place(relx=0.5, rely=0.45, anchor='center')

        self.lb_header_nome = ctk.CTkLabel(
            self.frame_jogadores,
            text="Nome do Jogador",
            font=(FONTE_PADRAO, TAMANHO_FONTE_NORMAL, 'bold'),
            text_color=COR_TEXTO
        )
        self.lb_header_nome.grid(row=0, column=0, padx=10, pady=5)

        self.lb_header_pontos = ctk.CTkLabel(
            self.frame_jogadores,
            text="Pontos",
            font=(FONTE_PADRAO, TAMANHO_FONTE_NORMAL, 'bold'),
            text_color=COR_TEXTO
        )
        self.lb_header_pontos.grid(row=0, column=1, padx=10, pady=5)

        self.cursor.execute("SELECT id, nome, pontos FROM jogadores ORDER BY pontos DESC")
        jogadores = self.cursor.fetchall()

        self.jogador_var = ctk.IntVar()

        self.cursor.execute("SELECT jogador_atual FROM configuracao")
        jogador_atual = self.cursor.fetchone()[0]
        if jogador_atual:
            self.jogador_var.set(jogador_atual)

        for i, (id_jogador, nome, pontos) in enumerate(jogadores, start=1):
            ctk.CTkLabel(
                self.frame_jogadores,
                text=nome,
                font=(FONTE_PADRAO, TAMANHO_FONTE_NORMAL),
                text_color=COR_TEXTO
            ).grid(row=i, column=0, padx=10, pady=5)

            ctk.CTkLabel(
                self.frame_jogadores,
                text=str(pontos),
                font=(FONTE_PADRAO, TAMANHO_FONTE_NORMAL),
                text_color=COR_TEXTO
            ).grid(row=i, column=1, padx=10, pady=5)

            ctk.CTkRadioButton(
                self.frame_jogadores,
                text="",
                variable=self.jogador_var,
                value=id_jogador,
                command=self.atualizar_jogador,
                fg_color=COR_BOTAO
            ).grid(row=i, column=2, padx=10, pady=5)

        button_configs = {
            'width': BUTTON_WIDTH,
            'height': BUTTON_HEIGHT,
            'fg_color': COR_BOTAO,
            'text_color': COR_TEXTO_BOTAO,
            'hover_color': COR_BOTAO_HOVER,
            'font': (FONTE_PADRAO, TAMANHO_FONTE_NORMAL),
            'corner_radius': CORNER_RADIUS
        }

        self.btn_voltar = ctk.CTkButton(
            self.master,
            text="Voltar ao Menu",
            command=self.voltar_menu,
            **button_configs
        )
        self.btn_voltar.place(relx=0.5, rely=0.8, anchor='center')

    # A função atualizar_jogador é implementada para salvar no banco de dados o jogador atualmente selecionado
    def atualizar_jogador(self):
        jogador_selecionado = self.jogador_var.get()
        self.cursor.execute("UPDATE configuracao SET jogador_atual = ?", (jogador_selecionado,))
        self.conexao.commit()

    # A função voltar_menu é implementada para retornar ao menu principal
    def voltar_menu(self):
        if hasattr(self, 'conexao'):
            self.conexao.close()
        for widget in self.master.winfo_children():
            widget.destroy()
        MenuPrincipal(self.master)

    def __del__(self):
        if hasattr(self, 'conexao'):
            self.conexao.close()

if __name__ == "__main__":
    app = ctk.CTk()
    app.geometry("1280x720")
    largura_tela = app.winfo_screenwidth()
    altura_tela = app.winfo_screenheight()
    pos_x = (largura_tela // 2) - (WINDOW_WIDTH // 3)
    pos_y = (altura_tela // 3) - (WINDOW_HEIGHT // 3)
    app.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}+{pos_x}+{pos_y}")
    app.resizable(False, False)
    app.title("Quiz game")

    menu_principal = MenuPrincipal(app)
    app.mainloop()