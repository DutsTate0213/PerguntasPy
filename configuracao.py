import sqlite3
import customtkinter as ctk
from tkinter import messagebox
from PIL import Image
from config_global import *  # Importa todas as configurações globais

# A classe Configuracao é implementada para gerenciar a interface principal de configurações
# e controlar a navegação entre diferentes páginas de configuração
class Configuracao:
    # A função __init__ é implementada para inicializar a interface e estabelecer conexão com o banco de dados
    def __init__(self, master):
        self.master = master
        self.master.configure(fg_color=COR_FUNDO)
        self.conexao = sqlite3.connect("database/quiz_game.db")
        self.cursor = self.conexao.cursor()
        
        self.criar_interface()

    # A função criar_interface é implementada para construir a interface gráfica principal
    # e configurar os botões de navegação
    def criar_interface(self):
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
        self.btn_questoes = ctk.CTkButton(self.master, text="Gerenciar Questões", 
                             command=self.abrir_questoes, **button_configs)
        self.btn_questoes.place(relx=0.5, rely=0.4, anchor='center')

        self.btn_config_jogo = ctk.CTkButton(self.master, text="Configurações do Jogo", 
                                            command=self.abrir_config_jogo, **button_configs)
        self.btn_config_jogo.place(relx=0.5, rely=0.5, anchor='center')

        self.btn_jogador = ctk.CTkButton(self.master, text="Gerenciar Jogador",
                                        command=self.abrir_jogador, **button_configs)
        self.btn_jogador.place(relx=0.5, rely=0.6, anchor='center')

        self.btn_voltar = ctk.CTkButton(self.master, text="Voltar",
                                       command=self.voltar_menu,
                                       **button_configs)
        self.btn_voltar.place(relx=0.5, rely=0.7, anchor='center')

    # A função voltar_menu é implementada para retornar ao menu principal
    # e limpar recursos utilizados
    def voltar_menu(self):
        # Fecha a conexão com o banco de dados
        if hasattr(self, 'conexao'):
            self.conexao.close()
        # Limpa a tela atual
        for widget in self.master.winfo_children():
            widget.destroy()
        # Importa e abre o menu principal
        from game_quiz import MenuPrincipal
        MenuPrincipal(self.master)

    def abrir_questoes(self):
        PaginaQuestoes(self.master)

    def abrir_config_jogo(self):
        PaginaConfiguracao(self.master)

    def abrir_jogador(self):
        PaginaJogador(self.master)

    def __del__(self):
        if hasattr(self, 'conexao'):
            self.conexao.close()

# A classe PaginaQuestoes é implementada para gerenciar o CRUD de questões
# e fornecer interface para edição do banco de questões
class PaginaQuestoes:
    # A função __init__ é implementada para inicializar a interface de questões
    # e carregar questões existentes do banco de dados
    def __init__(self, master):
        self.master = master
        self.conexao = sqlite3.connect("database/quiz_game.db")
        self.cursor = self.conexao.cursor()
        
        self.cursor.execute("SELECT * FROM perguntas")
        self.questoes = self.cursor.fetchall()

        # Configuração dos botões simplificada usando dicionário para centralizar estilos
        self.button_configs = {
            'width': 200,
            'height': 40,
            'fg_color': "#333333",
            'text_color': "white",
            'hover_color': "#444444",
            'font': ("Arial", 14),
            'corner_radius': 10
        }
        
        # Limpar a tela antes de criar a nova interface
        for widget in self.master.winfo_children():
            widget.destroy()
            
        self.pagina_questoes()

    # A função pagina_questoes é implementada para criar a interface de listagem de questões
    # e configurar os controles de edição
    def pagina_questoes(self):
        # Frame principal
        main_frame = ctk.CTkFrame(self.master, fg_color="#2b2b2b")
        main_frame.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.8, relheight=0.8)

        # Título
        label_questoes = ctk.CTkLabel(main_frame, text="Gerenciar Questões", 
                                     font=("Arial", 24, "bold"))
        label_questoes.place(relx=0.5, rely=0.05, anchor="center")

        # Frame scrollável para as questões
        scrollable_frame = ctk.CTkScrollableFrame(main_frame, 
                                                width=900, 
                                                height=400,
                                                fg_color="#333333")
        scrollable_frame.place(relx=0.5, rely=0.45, anchor="center")

        # Grid para organizar o conteúdo
        scrollable_frame.grid_columnconfigure(1, weight=1)  # Coluna da questão expande

        # Cabeçalho da lista de questões com larguras específicas
        header_frame = ctk.CTkFrame(scrollable_frame, fg_color="transparent")
        header_frame.grid(row=0, column=0, columnspan=3, sticky="ew", padx=20, pady=(0, 10))
        header_frame.grid_columnconfigure(1, weight=1)  # Coluna do meio expande

        # Configuração das larguras das colunas
        numero_width = 60
        acoes_width = 100

        ctk.CTkLabel(header_frame, text="Nº", font=("Arial", 14, "bold"), width=numero_width).grid(
            row=0, column=0, padx=(20, 0))
        
        ctk.CTkLabel(header_frame, text="Questão", font=("Arial", 14, "bold")).grid(
            row=0, column=1, padx=10, sticky="w")
        
        ctk.CTkLabel(header_frame, text="Editar", font=("Arial", 14, "bold"), width=acoes_width).grid(
            row=0, column=2, padx=(0, 20))

        # Linha separadora
        separator = ctk.CTkFrame(scrollable_frame, height=2, fg_color="gray50")
        separator.grid(row=1, column=0, columnspan=3, sticky="ew", padx=20, pady=(0, 10))

        # Lista de questões
        for numero, questao in enumerate(self.questoes):
            # Frame para cada questão
            questao_frame = ctk.CTkFrame(scrollable_frame, fg_color="transparent")
            questao_frame.grid(row=numero + 2, column=0, columnspan=3, sticky="ew", padx=20, pady=5)
            questao_frame.grid_columnconfigure(1, weight=1)  # Coluna do meio expande

            # Número da questão
            label_numero = ctk.CTkLabel(questao_frame, 
                                      text=f"{numero + 1}",
                                      font=("Arial", 12),
                                      width=numero_width)
            label_numero.grid(row=0, column=0, padx=(20, 0))

            # Texto da questão (limitado a 80 caracteres)
            texto_questao = questao[1][:80] + "..." if len(questao[1]) > 80 else questao[1]
            label_questao = ctk.CTkLabel(questao_frame, 
                                       text=texto_questao,
                                       font=("Arial", 12))
            label_questao.grid(row=0, column=1, padx=10, sticky="w")

            # Botão de editar
            imagem_botao = ctk.CTkImage(light_image=Image.open("img/botao-editar.png"),
                                       dark_image=Image.open("img/botao-editar.png"),
                                       size=(20, 20))
            
            btn_questao = ctk.CTkButton(questao_frame, 
                                       text="", 
                                       image=imagem_botao, 
                                       width=30, 
                                       height=30,
                                       fg_color="transparent",
                                       hover_color="#444444",
                                       command=lambda n=numero: self.editar_questao(n))
            btn_questao.grid(row=0, column=2, padx=(0, 20))

        # Frame para botões de ação
        botoes_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        botoes_frame.place(relx=0.5, rely=0.9, anchor="center")

        btn_adicionar_questao = ctk.CTkButton(botoes_frame, 
                                             text="Adicionar Questão", 
                                             command=self.adicionar_questao, 
                                             **self.button_configs)
        btn_adicionar_questao.grid(row=0, column=1, padx=10)

        btn_voltar = ctk.CTkButton(botoes_frame, 
                                  text="Voltar", 
                                  command=self.voltar_configuracao, 
                                  **self.button_configs)
        btn_voltar.grid(row=0, column=0, padx=10)

    # A função adicionar_questao é implementada para criar interface de nova questão
    # e configurar campos de entrada
    def adicionar_questao(self):
        for widget in self.master.winfo_children():
            widget.destroy()

        # Frame principal
        main_frame = ctk.CTkFrame(self.master, fg_color="#2b2b2b")
        main_frame.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.8, relheight=0.8)

        # Título
        label_adicionar_questao = ctk.CTkLabel(main_frame, text="Adicionar Questão", 
                                              font=("Arial", 24, "bold"))
        label_adicionar_questao.place(relx=0.5, rely=0.05, anchor="center")

        # Frame para os campos
        campos_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        campos_frame.place(relx=0.5, rely=0.5, anchor="center")

        # Configuração dos campos
        campos = [
            ("Enunciado:", "entrada_enunciado"),
            ("Alternativa A:", "entrada_alternativa_a"),
            ("Alternativa B:", "entrada_alternativa_b"),
            ("Alternativa C:", "entrada_alternativa_c"),
            ("Alternativa D:", "entrada_alternativa_d"),
            ("Alternativa E:", "entrada_alternativa_e"),
            ("Resposta Certa:", "entrada_resposta_certa"),
        ]

        for i, (label_text, _) in enumerate(campos):
            label = ctk.CTkLabel(campos_frame, text=label_text)
            label.grid(row=i, column=0, padx=(20, 10), pady=10, sticky="e")
            
            entrada = ctk.CTkEntry(campos_frame, width=600)
            entrada.grid(row=i, column=1, padx=(10, 20), pady=10)
            setattr(self, f"entrada_{i}", entrada)  # Armazena referência para uso posterior

        # Adicionar frame para os radio buttons
        dificuldade_frame = ctk.CTkFrame(campos_frame, fg_color="transparent")
        dificuldade_frame.grid(row=len(campos), column=0, columnspan=2, pady=20)

        # Label para dificuldade
        label_dificuldade = ctk.CTkLabel(dificuldade_frame, text="Nível de Dificuldade:")
        label_dificuldade.grid(row=0, column=0, padx=(0, 10))

        # Variável para armazenar a seleção
        self.dificuldade_var = ctk.StringVar(value="outro")

        # Dicionário de dificuldades e pontos
        dificuldades = {
            "Fácil (5 pts)": "facil",
            "Médio (10 pts)": "medio",
            "Difícil (20 pts)": "dificil",
            "Especialista (40 pts)": "especialista",
            "Extremo (80 pts)": "extremo"
        }

        # Criar radio buttons horizontalmente
        for i, (texto, valor) in enumerate(dificuldades.items()):
            radio = ctk.CTkRadioButton(dificuldade_frame, 
                                     text=texto, 
                                     variable=self.dificuldade_var, 
                                     value=valor)
            radio.grid(row=0, column=i+1, padx=10)

        # Frame para botões
        botoes_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        botoes_frame.place(relx=0.5, rely=0.9, anchor="center")

        btn_salvar = ctk.CTkButton(botoes_frame, text="Criar Questão", 
                                  command=lambda: self.salvar_questao(
                                      self.entrada_0.get(),  # enunciado
                                      self.entrada_1.get(),  # alternativa A
                                      self.entrada_2.get(),  # alternativa B
                                      self.entrada_3.get(),  # alternativa C
                                      self.entrada_4.get(),  # alternativa D
                                      self.entrada_5.get(),  # alternativa E
                                      self.entrada_6.get()   # resposta certa
                                  ), **self.button_configs)
        btn_salvar.grid(row=0, column=1, padx=10)

        btn_cancelar = ctk.CTkButton(botoes_frame, text="Cancelar", 
                                    command=self.voltar, **self.button_configs)
        btn_cancelar.grid(row=0, column=0, padx=10)

    # A função salvar_questao é implementada para validar e persistir nova questão no banco
    # Simplificada usando dicionário para mapear dificuldade -> pontos
    def salvar_questao(self, enunciado, alternativa_a, alternativa_b, alternativa_c, 
                      alternativa_d, alternativa_e, resposta_certa):
        # Validar a resposta
        if not self.validar_resposta(resposta_certa):
            return
        
        # Converter a letra em número
        resposta_numero = self.letra_para_numero(resposta_certa)
        
        # Obter pontos baseado na dificuldade selecionada
        pontos = self.get_pontos_por_dificuldade(self.dificuldade_var.get())

        try:
            self.cursor.execute("""
                UPDATE perguntas 
                SET pergunta=?, opcao_a=?, opcao_b=?, opcao_c=?, opcao_d=?, opcao_e=?, 
                    resposta_certa=?, pontos=? 
                WHERE id=?""", 
                (enunciado, alternativa_a, alternativa_b, alternativa_c, 
                 alternativa_d, alternativa_e, resposta_numero, pontos)
            )
            self.conexao.commit()
            
            self.cursor.execute("SELECT * FROM perguntas")
            self.questoes = self.cursor.fetchall()
            
            messagebox.showinfo("Sucesso", "Questão criada com sucesso!")
            self.voltar()
            
        except sqlite3.Error as e:
            messagebox.showerror("Erro", f"Erro ao criar questão: {str(e)}")

    # A função editar_questao é implementada para criar interface de edição
    # e carregar dados da questão existente
    def editar_questao(self, numero):
        for widget in self.master.winfo_children():
            widget.destroy()

        # Frame principal
        main_frame = ctk.CTkFrame(self.master, fg_color="#2b2b2b")
        main_frame.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.8, relheight=0.8)

        # Título
        label_editar_questao = ctk.CTkLabel(main_frame, text="Editar Questão", 
                                           font=("Arial", 24, "bold"))
        label_editar_questao.place(relx=0.5, rely=0.05, anchor="center")

        # Frame para os campos
        campos_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        campos_frame.place(relx=0.5, rely=0.5, anchor="center")

        # Dados da questão atual
        questao_atual = self.questoes[numero]
        numero_para_letra = {0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'E'}
        resposta_letra = numero_para_letra.get(questao_atual[7], '')

        # Configuração dos campos
        campos = [
            ("Enunciado:", questao_atual[1]),
            ("Alternativa A:", questao_atual[2]),
            ("Alternativa B:", questao_atual[3]),
            ("Alternativa C:", questao_atual[4]),
            ("Alternativa D:", questao_atual[5]),
            ("Alternativa E:", questao_atual[6]),
            ("Resposta Certa:", resposta_letra),
        ]

        for i, (label_text, valor) in enumerate(campos):
            label = ctk.CTkLabel(campos_frame, text=label_text)
            label.grid(row=i, column=0, padx=(20, 10), pady=10, sticky="e")
            
            entrada = ctk.CTkEntry(campos_frame, width=600)
            entrada.insert(0, str(valor))
            entrada.grid(row=i, column=1, padx=(10, 20), pady=10)
            setattr(self, f"entrada_{i}", entrada)

        # Adicionar frame para os radio buttons
        dificuldade_frame = ctk.CTkFrame(campos_frame, fg_color="transparent")
        dificuldade_frame.grid(row=len(campos), column=0, columnspan=2, pady=20)

        # Label para dificuldade
        label_dificuldade = ctk.CTkLabel(dificuldade_frame, text="Nível de Dificuldade:")
        label_dificuldade.grid(row=0, column=0, padx=(0, 10))

        # Pegar a dificuldade atual da questão baseada nos pontos
        pontos_atuais = questao_atual[8] if len(questao_atual) > 8 else 5
        dificuldade_atual = self.pontos_para_dificuldade(pontos_atuais)
        
        self.dificuldade_var = ctk.StringVar(value=dificuldade_atual)

        # Dicionário de dificuldades e pontos
        dificuldades = {
            "Fácil (5 pts)": "facil",
            "Médio (10 pts)": "medio",
            "Difícil (20 pts)": "dificil",
            "Especialista (40 pts)": "especialista",
            "Extremo (80 pts)": "extremo"
        }

        # Criar radio buttons horizontalmente
        for i, (texto, valor) in enumerate(dificuldades.items()):
            radio = ctk.CTkRadioButton(dificuldade_frame, 
                                     text=texto, 
                                     variable=self.dificuldade_var, 
                                     value=valor)
            radio.grid(row=0, column=i+1, padx=10)

        # Frame para botões
        botoes_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        botoes_frame.place(relx=0.5, rely=0.9, anchor="center")

        btn_deletar = ctk.CTkButton(botoes_frame, text="Deletar", 
                                   command=lambda: self.deletar_questao(numero), 
                                   **self.button_configs)
        btn_deletar.grid(row=0, column=0, padx=10)

        btn_cancelar = ctk.CTkButton(botoes_frame, text="Cancelar", 
                                    command=self.voltar, **self.button_configs)
        btn_cancelar.grid(row=0, column=1, padx=10)

        btn_salvar = ctk.CTkButton(botoes_frame, text="Salvar", 
                                  command=lambda: self.salvar_edicao(
                                      numero, 
                                      self.entrada_0.get(),  # enunciado
                                      self.entrada_1.get(),  # alternativa A
                                      self.entrada_2.get(),  # alternativa B
                                      self.entrada_3.get(),  # alternativa C
                                      self.entrada_4.get(),  # alternativa D
                                      self.entrada_5.get(),  # alternativa E
                                      self.entrada_6.get(),  # resposta certa
                                      self.dificuldade_var.get()  # dificuldade
                                  ), **self.button_configs)
        btn_salvar.grid(row=0, column=2, padx=10)

    # A função deletar_questao é implementada para remover questão do banco de dados
    def deletar_questao(self, numero):
        id_questao = self.questoes[numero][0]
        
        self.cursor.execute("DELETE FROM perguntas WHERE id=?", (id_questao,))
        self.conexao.commit()
        
        self.cursor.execute("SELECT * FROM perguntas")
        self.questoes = self.cursor.fetchall()
        
        messagebox.showinfo("Sucesso", "Questão deletada com sucesso!")
        self.voltar()

    # A função letra_para_numero é implementada para converter resposta em letra para índice
    # Simplificada usando dicionário para mapear letra -> número
    def letra_para_numero(self, letra):
        mapeamento = {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4}
        letra = letra.upper()
        if letra not in mapeamento:
            return None
        return mapeamento[letra]

    # A função validar_resposta é implementada para verificar formato da resposta
    def validar_resposta(self, resposta):
        if not resposta:
            messagebox.showerror("Erro", "Por favor, insira uma resposta.")
            return False
        
        resposta = resposta.upper()
        if resposta not in ['A', 'B', 'C', 'D', 'E']:
            messagebox.showerror("Erro", "A resposta deve ser uma letra entre A e E.")
            return False
        return True
    def salvar_questao(self, enunciado, alternativa_a, alternativa_b, alternativa_c, 
                      alternativa_d, alternativa_e, resposta_certa):
        # Validar a resposta
        if not self.validar_resposta(resposta_certa):
            return
        
        # Converter a letra em número
        resposta_numero = self.letra_para_numero(resposta_certa)
        
        # Obter pontos baseado na dificuldade selecionada
        pontos = self.get_pontos_por_dificuldade(self.dificuldade_var.get())
        
        self.cursor.execute("""
            INSERT INTO perguntas (pergunta, opcao_a, opcao_b, opcao_c, opcao_d, opcao_e, 
                                 resposta_certa, pontos) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)""", 
            (enunciado, alternativa_a, alternativa_b, alternativa_c, 
             alternativa_d, alternativa_e, resposta_numero, pontos)
        )
        self.conexao.commit()

        self.cursor.execute("SELECT * FROM perguntas")
        self.questoes = self.cursor.fetchall()
        
        messagebox.showinfo("Sucesso", "Questão criada com sucesso!")
        self.voltar()
    
    # A função salvar_edicao é implementada para persistir alterações em questão existente
    def salvar_edicao(self, numero, enunciado, alternativa_a, alternativa_b, alternativa_c, 
                      alternativa_d, alternativa_e, resposta_certa, dificuldade):
        # Validar a resposta
        if not self.validar_resposta(resposta_certa):
            return
        
        # Converter a letra em número
        resposta_numero = self.letra_para_numero(resposta_certa)
        
        # Obter pontos baseado na dificuldade selecionada
        pontos = self.get_pontos_por_dificuldade(dificuldade)
        print(pontos)
        
        id_questao = self.questoes[numero][0]
        
        self.cursor.execute("""
            UPDATE perguntas 
            SET pergunta=?, opcao_a=?, opcao_b=?, opcao_c=?, opcao_d=?, opcao_e=?, 
                resposta_certa=?, pontos=? 
            WHERE id=?""", 
            (enunciado, alternativa_a, alternativa_b, alternativa_c, 
             alternativa_d, alternativa_e, resposta_numero, pontos, id_questao)
        )
        self.conexao.commit()
        
        self.cursor.execute("SELECT * FROM perguntas")
        self.questoes = self.cursor.fetchall()
        
        messagebox.showinfo("Sucesso", "Questão atualizada com sucesso!")
        self.voltar()

    # A função voltar é implementada para limpar a tela e retornar à interface de listagem de questões
    def voltar(self):
        for widget in self.master.winfo_children():
            widget.destroy()
        self.pagina_questoes()

    # A função voltar_configuracao é implementada para limpar a tela e retornar à interface principal de configurações
    def voltar_configuracao(self):
        if hasattr(self, 'conexao'):
            self.conexao.close()
        Configuracao(self.master)

    def __del__(self):
        if hasattr(self, 'conexao'):
            self.conexao.close()

    # A função get_pontos_por_dificuldade é implementada para converter nível em pontos
    # Simplificada usando dicionário para mapear dificuldade -> pontos
    def get_pontos_por_dificuldade(self, dificuldade):
        pontos = {
            "facil": 5,
            "medio": 10,
            "dificil": 20,
            "especialista": 40,
            "extremo": 80
        }
        return pontos.get(dificuldade, 5)  # retorna 5 como padrão se a dificuldade não for encontrada
    
    # A função verificar_dificuldade é implementada para validar nível de dificuldade
    def verificar_dificuldade(self, dificuldade):
        return dificuldade if dificuldade in ["facil", "medio", "dificil", "especialista", "extremo"] else "facil"

    # A função pontos_para_dificuldade é implementada para converter pontos em nível
    # Simplificada usando dicionário para mapear pontos -> dificuldade
    def pontos_para_dificuldade(self, pontos):
        mapeamento = {
            5: "facil",
            10: "medio",
            20: "dificil",
            40: "especialista",
            80: "extremo"
        }
        return mapeamento.get(pontos, "facil")

# A classe PaginaConfiguracao é implementada para gerenciar configurações do jogo
# e persistir preferências do usuário
class PaginaConfiguracao:
    # A função __init__ é implementada para inicializar interface de configurações
    # e carregar configurações existentes
    def __init__(self, master):
        self.master = master
        self.conexao = sqlite3.connect("database/quiz_game.db")
        self.cursor = self.conexao.cursor()
        
        # Buscar configuração atual
        self.cursor.execute("SELECT * FROM configuracao")
        self.config = self.cursor.fetchone()
        
        # Se não existir configuração, criar uma padrão
        if not self.config:
            self.cursor.execute("INSERT INTO configuracao (numero_questoes, tempo_questao) VALUES (5, 30)")
            self.conexao.commit()
            self.config = (1, 5, 30)  # id, numero_questoes, tempo_questao
        
        # Configuração dos botões simplificada usando dicionário para centralizar estilos
        self.button_configs = {
            'width': 200,
            'height': 40,
            'fg_color': "#333333",
            'text_color': "white",
            'hover_color': "#444444",
            'font': ("Arial", 14),
            'corner_radius': 10
        }
        
        # Limpar a tela antes de criar a nova interface
        for widget in self.master.winfo_children():
            widget.destroy()
            
        self.pagina_configuracao()

    # A função pagina_configuracao é implementada para criar interface de configurações
    # e campos de entrada
    def pagina_configuracao(self):
        # Frame principal
        frame = ctk.CTkFrame(self.master)
        frame.place(relx=0.5, rely=0.4, anchor="center")

        # Título
        label_titulo = ctk.CTkLabel(frame, text="Configurações do Jogo", font=("Arial", 20, "bold"))
        label_titulo.grid(row=0, column=0, columnspan=2, pady=20, padx=20)

        # Número de questões
        label_num_questoes = ctk.CTkLabel(frame, text="Número de Questões por Rodada:")
        label_num_questoes.grid(row=1, column=0, pady=10, padx=20)

        self.entrada_num_questoes = ctk.CTkEntry(frame, width=200)
        self.entrada_num_questoes.insert(0, str(self.config[1]))
        self.entrada_num_questoes.grid(row=1, column=1, pady=10, padx=20)

        # Tempo por questão
        label_tempo = ctk.CTkLabel(frame, text="Tempo por Questão (segundos):")
        label_tempo.grid(row=2, column=0, pady=10, padx=20)

        self.entrada_tempo = ctk.CTkEntry(frame, width=200)
        self.entrada_tempo.insert(0, str(self.config[2]))
        self.entrada_tempo.grid(row=2, column=1, pady=10, padx=20)

        # Botões
        btn_salvar = ctk.CTkButton(
            self.master, 
            text="Salvar Configurações", 
            command=lambda: self.salvar_configuracao(self.entrada_num_questoes.get(), self.entrada_tempo.get()),
            **self.button_configs
        )
        btn_salvar.place(relx=0.6, rely=0.8, anchor="center")

        btn_voltar = ctk.CTkButton(
            self.master, 
            text="Voltar", 
            command=self.voltar_configuracao,
            **self.button_configs
        )
        btn_voltar.place(relx=0.4, rely=0.8, anchor="center")

    # A função salvar_configuracao é implementada para validar e persistir configurações
    def salvar_configuracao(self, num_questoes, tempo_questao):
        try:
            if int(num_questoes) <= 0 or int(tempo_questao) <= 0:
                messagebox.showerror("Erro", "Os valores devem ser maiores que zero!")
                return
            
            self.cursor.execute("""
                UPDATE configuracao 
                SET numero_questoes = ?, tempo_questao = ? 
                WHERE id = ?""", 
                (num_questoes, tempo_questao, self.config[0])
            )
            self.conexao.commit()

            # Atualiza a configuração
            self.cursor.execute("SELECT * FROM configuracao")
            self.config = self.cursor.fetchone()
            
            messagebox.showinfo("Sucesso", "Configurações salvas com sucesso!")
            
        except ValueError:
            messagebox.showerror("Erro", "Por favor, insira apenas números inteiros!")

    # A função voltar_configuracao é implementada para limpar a tela e retornar à interface principal de configurações
    def voltar_configuracao(self):
        if hasattr(self, 'conexao'):
            self.conexao.close()
        Configuracao(self.master)

    def __del__(self):
        if hasattr(self, 'conexao'):
            self.conexao.close()

# A classe PaginaJogador é implementada para gerenciar cadastro de jogadores
# e suas pontuações
class PaginaJogador:
    # A função __init__ é implementada para inicializar interface de jogadores
    # e carregar lista de jogadores
    def __init__(self, master):
        self.master = master
        self.conexao = sqlite3.connect("database/quiz_game.db")
        self.cursor = self.conexao.cursor()
        
        self.cursor.execute("SELECT * FROM jogadores")
        self.jogadores = self.cursor.fetchall()

        # Configuração dos botões simplificada usando dicionário para centralizar estilos
        self.button_configs = {
            'width': 200,
            'height': 40,
            'fg_color': "#333333",
            'text_color': "white",
            'hover_color': "#444444",
            'font': ("Arial", 14),
            'corner_radius': 10
        }
        
        for widget in self.master.winfo_children():
            widget.destroy()
            
        self.pagina_jogadores()

    # A função pagina_jogadores é implementada para criar interface de listagem
    # e controles de edição
    def pagina_jogadores(self):
        main_frame = ctk.CTkFrame(self.master, fg_color="#2b2b2b")
        main_frame.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.8, relheight=0.8)

        label_jogadores = ctk.CTkLabel(main_frame, text="Gerenciar Jogadores", 
                                     font=("Arial", 24, "bold"))
        label_jogadores.place(relx=0.5, rely=0.05, anchor="center")

        scrollable_frame = ctk.CTkScrollableFrame(main_frame, 
                                                width=900, 
                                                height=400,
                                                fg_color="#333333")
        scrollable_frame.place(relx=0.5, rely=0.45, anchor="center")

        # Cabeçalho
        header_frame = ctk.CTkFrame(scrollable_frame, fg_color="transparent")
        header_frame.grid(row=0, column=0, columnspan=6, sticky="ew", padx=20, pady=(0, 10))

        headers = ["Nº", "Nome", "Pontos", "Acertos", "Erros", "Editar"]
        widths = [60, 200, 100, 100, 100, 100]
        
        for i, (header, width) in enumerate(zip(headers, widths)):
            ctk.CTkLabel(header_frame, text=header, font=("Arial", 14, "bold"), 
                        width=width).grid(row=0, column=i, padx=5)

        separator = ctk.CTkFrame(scrollable_frame, height=2, fg_color="gray50")
        separator.grid(row=1, column=0, columnspan=6, sticky="ew", padx=20, pady=(0, 10))

        # Lista de jogadores
        for i, jogador in enumerate(self.jogadores):
            jogador_frame = ctk.CTkFrame(scrollable_frame, fg_color="transparent")
            jogador_frame.grid(row=i+2, column=0, columnspan=6, sticky="ew", padx=20, pady=5)

            ctk.CTkLabel(jogador_frame, text=f"{i+1}", width=60).grid(row=0, column=0, padx=5)
            ctk.CTkLabel(jogador_frame, text=jogador[1], width=200).grid(row=0, column=1, padx=5)
            ctk.CTkLabel(jogador_frame, text=str(jogador[2]), width=100).grid(row=0, column=2, padx=5)
            ctk.CTkLabel(jogador_frame, text=str(jogador[3]), width=100).grid(row=0, column=3, padx=5)
            ctk.CTkLabel(jogador_frame, text=str(jogador[4]), width=100).grid(row=0, column=4, padx=5)

            imagem_botao = ctk.CTkImage(light_image=Image.open("img/botao-editar.png"),
                                      dark_image=Image.open("img/botao-editar.png"),
                                      size=(20, 20))
            
            btn_editar = ctk.CTkButton(jogador_frame, 
                                     text="", 
                                     image=imagem_botao,
                                     width=30,
                                     height=30,
                                     fg_color="transparent",
                                     hover_color="#444444",
                                     command=lambda n=i: self.editar_jogador(n))
            btn_editar.grid(row=0, column=5, padx=5)

        botoes_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        botoes_frame.place(relx=0.5, rely=0.9, anchor="center")

        btn_adicionar = ctk.CTkButton(botoes_frame, 
                                    text="Adicionar Jogador", 
                                    command=self.adicionar_jogador, 
                                    **self.button_configs)
        btn_adicionar.grid(row=0, column=1, padx=10)

        btn_voltar = ctk.CTkButton(botoes_frame, 
                                  text="Voltar", 
                                  command=self.voltar_configuracao, 
                                  **self.button_configs)
        btn_voltar.grid(row=0, column=0, padx=10)

    # A função adicionar_jogador é implementada para criar interface de novo jogador
    def adicionar_jogador(self):
        for widget in self.master.winfo_children():
            widget.destroy()

        main_frame = ctk.CTkFrame(self.master, fg_color="#2b2b2b")
        main_frame.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.8, relheight=0.8)

        label_adicionar = ctk.CTkLabel(main_frame, text="Adicionar Jogador", 
                                     font=("Arial", 24, "bold"))
        label_adicionar.place(relx=0.5, rely=0.2, anchor="center")

        label_nome = ctk.CTkLabel(main_frame, text="Nome do Jogador:")
        label_nome.place(relx=0.3, rely=0.4, anchor="center")

        self.entrada_nome = ctk.CTkEntry(main_frame, width=300)
        self.entrada_nome.place(relx=0.5, rely=0.4, anchor="center")

        botoes_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        botoes_frame.place(relx=0.5, rely=0.8, anchor="center")

        btn_salvar = ctk.CTkButton(botoes_frame, text="Criar Jogador", 
                                  command=self.salvar_jogador, **self.button_configs)
        btn_salvar.grid(row=0, column=1, padx=10)

        btn_cancelar = ctk.CTkButton(botoes_frame, text="Cancelar", 
                                    command=self.voltar, **self.button_configs)
        btn_cancelar.grid(row=0, column=0, padx=10)

    # A função editar_jogador é implementada para criar interface de edição
    # e carregar dados do jogador
    def editar_jogador(self, numero):
        for widget in self.master.winfo_children():
            widget.destroy()

        main_frame = ctk.CTkFrame(self.master, fg_color="#2b2b2b")
        main_frame.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.8, relheight=0.8)

        label_editar = ctk.CTkLabel(main_frame, text="Editar Jogador", 
                                  font=("Arial", 24, "bold"))
        label_editar.place(relx=0.5, rely=0.2, anchor="center")

        jogador_atual = self.jogadores[numero]

        label_nome = ctk.CTkLabel(main_frame, text="Nome do Jogador:")
        label_nome.place(relx=0.3, rely=0.4, anchor="center")

        self.entrada_nome = ctk.CTkEntry(main_frame, width=300)
        self.entrada_nome.insert(0, jogador_atual[1])
        self.entrada_nome.place(relx=0.5, rely=0.4, anchor="center")

        botoes_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        botoes_frame.place(relx=0.5, rely=0.8, anchor="center")

        btn_deletar = ctk.CTkButton(botoes_frame, text="Deletar", 
                                   command=lambda: self.deletar_jogador(numero), 
                                   **self.button_configs)
        btn_deletar.grid(row=0, column=0, padx=10)

        btn_zerar = ctk.CTkButton(botoes_frame, text="Zerar Pontuação", 
                                 command=lambda: self.zerar_pontuacao(numero), 
                                 **self.button_configs)
        btn_zerar.grid(row=0, column=1, padx=10)

        btn_cancelar = ctk.CTkButton(botoes_frame, text="Cancelar", 
                                    command=self.voltar, **self.button_configs)
        btn_cancelar.grid(row=0, column=2, padx=10)

        btn_salvar = ctk.CTkButton(botoes_frame, text="Salvar", 
                                  command=lambda: self.salvar_edicao(numero), 
                                  **self.button_configs)
        btn_salvar.grid(row=0, column=3, padx=10)

    # A função salvar_jogador é implementada para validar e persistir novo jogador
    def salvar_jogador(self):
        nome = self.entrada_nome.get().strip()
        if not nome:
            messagebox.showerror("Erro", "Por favor, insira um nome.")
            return

        self.cursor.execute("""
            INSERT INTO jogadores (nome, pontos, acertos, erros) 
            VALUES (?, 0, 0, 0)""", (nome,))
        self.conexao.commit()

        self.cursor.execute("SELECT * FROM jogadores")
        self.jogadores = self.cursor.fetchall()
        
        messagebox.showinfo("Sucesso", "Jogador criado com sucesso!")
        self.voltar()

    # A função salvar_edicao é implementada para persistir alterações em jogador
    def salvar_edicao(self, numero):
        nome = self.entrada_nome.get().strip()
        if not nome:
            messagebox.showerror("Erro", "Por favor, insira um nome.")
            return

        id_jogador = self.jogadores[numero][0]
        self.cursor.execute("UPDATE jogadores SET nome=? WHERE id=?", (nome, id_jogador))
        self.conexao.commit()

        self.cursor.execute("SELECT * FROM jogadores")
        self.jogadores = self.cursor.fetchall()
        
        messagebox.showinfo("Sucesso", "Jogador atualizado com sucesso!")
        self.voltar()

    # A função zerar_pontuacao é implementada para resetar estatísticas do jogador
    def zerar_pontuacao(self, numero):
        id_jogador = self.jogadores[numero][0]
        self.cursor.execute("""
            UPDATE jogadores 
            SET pontos=0, acertos=0, erros=0 
            WHERE id=?""", (id_jogador,))
        self.conexao.commit()

        self.cursor.execute("SELECT * FROM jogadores")
        self.jogadores = self.cursor.fetchall()
        
        messagebox.showinfo("Sucesso", "Pontuação zerada com sucesso!")
        self.voltar()

    # A função deletar_jogador é implementada para remover jogador do banco de dados
    def deletar_jogador(self, numero):
        id_jogador = self.jogadores[numero][0]
        self.cursor.execute("DELETE FROM jogadores WHERE id=?", (id_jogador,))
        self.conexao.commit()

        self.cursor.execute("SELECT * FROM jogadores")
        self.jogadores = self.cursor.fetchall()
        
        messagebox.showinfo("Sucesso", "Jogador deletado com sucesso!")
        self.voltar()

    # A função voltar é implementada para limpar a tela e retornar à interface de listagem de jogadores
    def voltar(self):
        for widget in self.master.winfo_children():
            widget.destroy()
        self.pagina_jogadores()

    # A função voltar_configuracao é implementada para limpar a tela e retornar à interface principal de configurações
    def voltar_configuracao(self):
        if hasattr(self, 'conexao'):
            self.conexao.close()
        Configuracao(self.master)

    def __del__(self):
        if hasattr(self, 'conexao'):
            self.conexao.close()

if __name__ == "__main__":
    app = ctk.CTk()
    app.geometry("1280x720")
    app.title("Configuração")
    
    configuracao = Configuracao(app)
    app.mainloop()