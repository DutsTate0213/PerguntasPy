import sqlite3
import customtkinter as ctk
from tkinter import messagebox
from random import randint
import time
import os
from config_global import *  # Importa todas as configurações globais


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
        self.lb_titulo = ctk.CTkLabel(self.master, text="Quiz Game", 
                                    font=(FONTE_PADRAO, TAMANHO_FONTE_TITULO), text_color=COR_TEXTO)
        self.lb_titulo.place(relx=0.5, rely=0.2, anchor='center')

        # Configuração dos botões
        button_configs = {
            'width': BUTTON_WIDTH,
            'height': BUTTON_HEIGHT,
            'fg_color': COR_BOTAO,
            'text_color': COR_TEXTO_BOTAO,
            'hover_color': COR_BOTAO_HOVER,
            'font': (FONTE_PADRAO, TAMANHO_FONTE_NORMAL),
            'corner_radius': CORNER_RADIUS
        }

        # Botões principais
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


    def iniciar_questionario(self):
        # Buscar configurações do banco de dados
        self.cursor.execute("SELECT numero_questoes, tempo_questao FROM configuracao")
        config = self.cursor.fetchone()
        if config:
            num_questoes, tempo_questao = config
        else:
            num_questoes, tempo_questao = 5, 30  # valores padrão
            
        for widget in self.master.winfo_children():
            widget.destroy()
        Questionario(self.master, num_questoes, tempo_questao)

    def abrir_configuracao(self):
        # Limpar a tela atual
        for widget in self.master.winfo_children():
            widget.destroy()
        # Abrir a página de configuração
        from configuracao import Configuracao
        Configuracao(self.master)

    def __del__(self):
        if hasattr(self, 'conexao'):
            self.conexao.close()

    def abrir_jogador(self):
        for widget in self.master.winfo_children():
            widget.destroy()
        PaginaJogador(self.master)

class Questionario:
    def __init__(self, master, num_questoes=5, tempo_questao=30):
        self.master = master
        self.master.configure(fg_color=COR_FUNDO)
        self.conexao = sqlite3.connect("database/quiz_game.db")
        self.cursor = self.conexao.cursor()

        # Buscar questões do banco de dados
        self.cursor.execute("SELECT * FROM perguntas")
        self.questoes = self.cursor.fetchall()

        #_ Criação da estrutura da pagina _#
        self.controle = 0
        self.respostas = []
        self.num_questoes = min(num_questoes, len(self.questoes))
        self.tempo_questao = tempo_questao
        
        # Cria uma lista de índices aleatórios para as questões
        self.indices_questoes = self.gerar_indices_aleatorios()

        # Interface
        self.lb_enunciado = ctk.CTkLabel(self.master, text="", text_color=COR_TEXTO, 
                                        wraplength=WINDOW_WIDTH-40, justify="left",
                                        font=(FONTE_PADRAO, TAMANHO_FONTE_NORMAL))
        self.lb_enunciado.place(x=20, y=20)

        # Radio buttons para alternativas
        self.radio_var = ctk.IntVar(value=-1)
        self.radiob_alternativas = []
        for i in range(5):
            rb = ctk.CTkRadioButton(self.master, text="", variable=self.radio_var, value=i,
                                   text_color=COR_TEXTO, fg_color=COR_BOTAO,
                                   font=(FONTE_PADRAO, TAMANHO_FONTE_NORMAL))
            self.radiob_alternativas.append(rb)
            rb.place(x=20, y=100 + i*50)

        # Feedback e temporizador
        self.lb_feedback = ctk.CTkLabel(self.master, text="", text_color=COR_TEXTO,
                                      font=(FONTE_PADRAO, TAMANHO_FONTE_NORMAL))
        self.lb_feedback.place(x=20, y=WINDOW_HEIGHT-200)

        self.progress_bar = ctk.CTkProgressBar(self.master, width=WINDOW_WIDTH-40, height=20)
        self.progress_bar.place(x=20, y=WINDOW_HEIGHT-150)
        self.progress_bar.set(0)

        self.timer = None
        self.is_running = True

        # Botões
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

        # Atualiza a primeira questão
        self.atualizar_questao()

    def gerar_indices_aleatorios(self):
        indices = []
        while len(indices) < self.num_questoes:
            indice = randint(0, len(self.questoes) - 1)
            if indice not in indices:
                indices.append(indice)
        return indices

    def atualizar_questao(self):
        indice_questao = self.indices_questoes[self.controle]
        questao_atual = self.questoes[indice_questao]
        
        # Estrutura da tabela perguntas: id, enunciado, alternativa_a, b, c, d, e, correta, dificuldade
        self.lb_enunciado.configure(text=f"{self.controle+1}. {questao_atual[1]}")
        
        alternativas = [questao_atual[2], questao_atual[3], questao_atual[4], 
                       questao_atual[5], questao_atual[6]]
        
        for i, rb in enumerate(self.radiob_alternativas):
            rb.configure(text=alternativas[i])
            
        self.radio_var.set(value=-1)
        self.lb_feedback.configure(text="")
        self.btn_proximo.configure(text="Responder", command=self.pegar_resposta)
        self.iniciar_temporizador()

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

        # Verifica a resposta
        indice_questao = self.indices_questoes[self.controle]
        questao_atual = self.questoes[indice_questao]
        resposta_correta = int(questao_atual[7])  # Converte para inteiro
        
        if resposta_selecionada != -1:
            # Compara diretamente os índices
            if resposta_selecionada == resposta_correta:
                self.lb_feedback.configure(text="Resposta correta!", text_color="green")
            else:
                # Mostra a alternativa correta (soma 2 porque as alternativas começam no índice 2 da tupla)
                self.lb_feedback.configure(text=f"Resposta incorreta. A resposta correta era: {questao_atual[resposta_correta + 2]}", 
                                         text_color="red")
        else:
            self.lb_feedback.configure(text="Tempo esgotado! Nenhuma resposta selecionada.", 
                                     text_color="orange")

        self.respostas.append((indice_questao, resposta_selecionada))
        self.btn_proximo.configure(text="Próxima questão", command=self.proxima_questao)

    def mostrar_resultados(self):
        self.is_running = False
        if self.timer:
            self.master.after_cancel(self.timer)
            self.timer = None
            
        for widget in self.master.winfo_children():
            widget.destroy()
        PaginaResposta(self.master, self.respostas, self.questoes)

    def sair(self):
        self.is_running = False  # Marca o questionário como inativo
        # Cancela o temporizador se ainda estiver ativo
        if self.timer:
            self.master.after_cancel(self.timer)
            self.timer = None
        # Fecha a conexão com o banco de dados
        if hasattr(self, 'conexao'):
            self.conexao.close()
        # Limpa a janela e volta para o menu principal
        for widget in self.master.winfo_children():
            widget.destroy()
        MenuPrincipal(self.master)

    def __del__(self):
        if hasattr(self, 'conexao'):
            self.conexao.close()

    def proxima_questao(self):
        self.controle += 1
        if self.controle < self.num_questoes:
            self.atualizar_questao()
        else:
            self.is_running = False  # Marca o questionário como inativo
            self.mostrar_resultados()

    def iniciar_temporizador(self):
        self.progress_bar.set(0)
        self.atualizar_temporizador()

    def atualizar_temporizador(self):
        if not self.is_running:
            return

        valor_atual = self.progress_bar.get()
        if valor_atual < 1:
            try:
                self.progress_bar.set(valor_atual + 0.1/self.tempo_questao)   
                self.timer = self.master.after(100, self.atualizar_temporizador)  
            except Exception:
                # Se ocorrer um erro ao atualizar a progress bar, vai simplismente ingnorar
                pass
        else:
            self.pegar_resposta(tempo_esgotado=True)
class PaginaResposta:
    def __init__(self, master, respostas, questoes):
        self.master = master
        self.master.configure(fg_color=COR_FUNDO)
        self.conexao = sqlite3.connect("database/quiz_game.db")
        self.cursor = self.conexao.cursor()

        # Calcula o número de respostas corretas
        self.corretas = 0
        pontos_totais = 0
        
        for indice_questao, resposta in respostas:
            if resposta != -1:  # Verifica se uma pergunta foi respondida
                questao = questoes[indice_questao]
                resposta_correta = int(questao[7])
                if resposta == resposta_correta:
                    self.corretas += 1
                    dificuldade = questao[8]
                    pontos = {
                        1: 5,    # fácil
                        2: 10,   # médio
                        3: 20,   # difícil
                        4: 40,   # especialista
                        5: 80    # extremo
                    }.get(dificuldade, 5)
                    pontos_totais += pontos

        # Busca o jogador atual da tabela configuração
        self.cursor.execute("SELECT jogador_atual FROM configuracao")
        jogador_atual_id = self.cursor.fetchone()[0]
        
        if jogador_atual_id:
            # Atualiza pontuação apenas do jogador atual
            self.cursor.execute("""
                UPDATE jogadores 
                SET pontos = pontos + ?,
                    acertos = acertos + ?,
                    erros = erros + ?
                WHERE id = ?
            """, (pontos_totais, self.corretas, len(respostas) - self.corretas, jogador_atual_id))
            self.conexao.commit()

        # Interface
        self.lb_titulo = ctk.CTkLabel(
            self.master, 
            text="Resultados", 
            font=(FONTE_PADRAO, TAMANHO_FONTE_TITULO), 
            text_color=COR_TEXTO
        )
        self.lb_titulo.place(relx=0.5, rely=0.3, anchor='center')

        # Texto do resultado
        resultado_texto = f"Você acertou {self.corretas} de {len(respostas)} questões!"
        if jogador_atual_id:  # Se houver jogador, mostra os pontos
            resultado_texto += f"\nPontos ganhos: {pontos_totais}"
        
        self.lb_resultado = ctk.CTkLabel(
            self.master, 
            text=resultado_texto,
            font=(FONTE_PADRAO, TAMANHO_FONTE_NORMAL), 
            text_color=COR_TEXTO
        )
        self.lb_resultado.place(relx=0.5, rely=0.5, anchor='center')

        # Botão para voltar ao menu
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

    def voltar_menu(self):
        # Salva a posição atual da janela
        x = self.master.winfo_x()
        y = self.master.winfo_y()
        
        # Fecha a conexão com o banco de dados
        if hasattr(self, 'conexao'):
            self.conexao.close()
            
        # Limpa a tela atual
        for widget in self.master.winfo_children():
            widget.destroy()
            
        # Volta para o menu principal
        MenuPrincipal(self.master) 
 
    def __del__(self):
        if hasattr(self, 'conexao'):
            self.conexao.close()
class PaginaJogador:
    def __init__(self, master):
        self.master = master
        self.master.configure(fg_color=COR_FUNDO)
        self.conexao = sqlite3.connect("database/quiz_game.db")
        self.cursor = self.conexao.cursor()
        self.interface_jogador()

    def interface_jogador(self):
        # Título da página
        self.lb_titulo = ctk.CTkLabel(
            self.master, 
            text="Seleção de Jogador",
            font=(FONTE_PADRAO, TAMANHO_FONTE_TITULO),
            text_color=COR_TEXTO
        )
        self.lb_titulo.place(relx=0.5, rely=0.1, anchor='center')

        # Frame para lista de jogadores
        self.frame_jogadores = ctk.CTkScrollableFrame(
            self.master,
            width=400,
            height=400,
            fg_color=COR_FUNDO
        )
        self.frame_jogadores.place(relx=0.5, rely=0.45, anchor='center')

        # Cabeçalho da lista
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

        # Buscar jogadores do banco
        self.cursor.execute("SELECT id, nome, pontos FROM jogadores ORDER BY pontos DESC")
        jogadores = self.cursor.fetchall()

        # Variável para armazenar o jogador selecionado
        self.jogador_var = ctk.IntVar()

        # Buscar jogador atual
        self.cursor.execute("SELECT jogador_atual FROM configuracao")
        jogador_atual = self.cursor.fetchone()[0]
        if jogador_atual:
            self.jogador_var.set(jogador_atual)

        # Listar jogadores
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

        # Botões
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

    def atualizar_jogador(self):
        jogador_selecionado = self.jogador_var.get()
        self.cursor.execute("UPDATE configuracao SET jogador_atual = ?", (jogador_selecionado,))
        self.conexao.commit()

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
    # Obtém as dimensões da tela do computador
    largura_tela = app.winfo_screenwidth()
    altura_tela = app.winfo_screenheight()
    # define a posicao da pagina 
    pos_x = (largura_tela // 2) - (WINDOW_WIDTH // 3)
    pos_y = (altura_tela // 3) - (WINDOW_HEIGHT // 3)
    app.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}+{pos_x}+{pos_y}")
    app.resizable(False, False)
    app.title("Quiz game")

    menu_principal = MenuPrincipal(app)
    app.mainloop()