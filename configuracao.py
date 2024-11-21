import sqlite3
import customtkinter as ctk
from tkinter import messagebox
from PIL import Image

conexao = sqlite3.connect("database/banco.db")

cursor = conexao.cursor()

cursor.execute("CREATE or ALTER TABLE IF NOT EXISTS perguntas (id INTEGER PRIMARY KEY AUTOINCREMENT, pergunta TEXT, opcao_a TEXT, opcao_b TEXT, opcao_c TEXT, opcao_d TEXT, opcao_e TEXT, resposta_certa INTEGER, pontos INTEGER)")
cursor.execute("CREATE or ALTER TABLE IF NOT EXISTS configuracao (id INTEGER PRIMARY KEY AUTOINCREMENT, numero_questoes INTEGER, tempo_questao INTEGER)")
cursor.execute("CREATE or ALTER TABLE IF NOT EXISTS jogadores (id INTEGER PRIMARY KEY AUTOINCREMENT, nome TEXT, pontos INTEGER, acertos INTEGER, erros INTEGER)")



app = ctk.CTk()
app.geometry("1280x720")
app.title("Configuração")

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

class Configuracao:
    def __init__(self, master):
        self.master = master
        self.master.configure(fg_color=COR_FUNDO)
        self.criar_interface()

    def criar_interface(self):
        # Título da página
        self.lb_titulo = ctk.CTkLabel(self.master, text="Configuração", 
                                    font=(FONTE_PADRAO, TAMANHO_FONTE_TITULO), text_color=COR_TEXTO)
        self.lb_titulo.place(relx=0.5, rely=0.2, anchor='center')

        # Configuração dos botões usando dicionário
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
        self.btn_questoes = ctk.CTkButton(self.master, text="Gerenciar Questões", 
                                        command=self.abrir_questoes, **button_configs)
        self.btn_questoes.place(relx=0.5, rely=0.4, anchor='center')

        self.btn_config_jogo = ctk.CTkButton(self.master, text="Configurar Jogo", 
                                           command=self.abrir_config_jogo, **button_configs)
        self.btn_config_jogo.place(relx=0.5, rely=0.5, anchor='center')

        self.btn_voltar = ctk.CTkButton(self.master, text="Voltar", 
                                      command=self.voltar_menu, **button_configs)
        self.btn_voltar.place(relx=0.5, rely=0.6, anchor='center')

    def abrir_questoes(self):
        # Limpar interface atual
        for widget in self.master.winfo_children():
            widget.destroy()
        
        # Criar interface de gerenciamento de questões
        self.criar_interface_questoes()

    def criar_interface_questoes(self):
        # Título
        self.lb_titulo = ctk.CTkLabel(self.master, text="Gerenciar Questões", 
                                    font=(FONTE_PADRAO, TAMANHO_FONTE_TITULO), text_color=COR_TEXTO)
        self.lb_titulo.place(relx=0.5, rely=0.1, anchor='center')

        # Campos para nova questão
        campos = ['Pergunta:', 'Opção A:', 'Opção B:', 'Opção C:', 'Opção D:', 'Resposta Certa (1-4):', 'Pontos:']
        self.entries = {}
        
        for i, campo in enumerate(campos):
            label = ctk.CTkLabel(self.master, text=campo, 
                               font=(FONTE_PADRAO, TAMANHO_FONTE_NORMAL), text_color=COR_TEXTO)
            label.place(relx=0.3, rely=0.2 + i*0.08, anchor='e')
            
            entry = ctk.CTkEntry(self.master, width=400, height=30, 
                               font=(FONTE_PADRAO, TAMANHO_FONTE_NORMAL))
            entry.place(relx=0.35, rely=0.2 + i*0.08, anchor='w')
            self.entries[campo] = entry

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

        self.btn_adicionar = ctk.CTkButton(self.master, text="Adicionar Questão", 
                                         command=self.adicionar_questao, **button_configs)
        self.btn_adicionar.place(relx=0.3, rely=0.8, anchor='center')
        self.btn_listar = ctk.CTkButton(self.master, text="Listar Questões", 
                                        command=self.listar_questoes, **button_configs)
        self.btn_listar.place(relx=0.7, rely=0.8, anchor='center')

        self.btn_voltar = ctk.CTkButton(self.master, text="Voltar", 
                                      command=self.criar_interface, **button_configs)
        self.btn_voltar.place(relx=0.7, rely=0.8, anchor='center')

    def adicionar_questao(self):
        try:
            # Validar campos vazios
            campos = {
                'Pergunta': self.entries['Pergunta:'].get(),
                'Opção A': self.entries['Opção A:'].get(),
                'Opção B': self.entries['Opção B:'].get(),
                'Opção C': self.entries['Opção C:'].get(),
                'Opção D': self.entries['Opção D:'].get(),
                'Resposta': self.entries['Resposta Certa (1-4):'].get(),
                'Pontos': self.entries['Pontos:'].get()
            }
            
            # Verificar campos vazios
            campos_vazios = [campo for campo, valor in campos.items() if not valor.strip()]
            if campos_vazios:
                messagebox.showerror("Erro", f"Os seguintes campos estão vazios: {', '.join(campos_vazios)}")
                return

            # Validar resposta e pontos
            resposta_certa = int(campos['Resposta'])
            pontos = int(campos['Pontos'])

            if not (1 <= resposta_certa <= 4):
                messagebox.showerror("Erro", "A resposta certa deve ser um número entre 1 e 4")
                return

            if pontos <= 0:
                messagebox.showerror("Erro", "Os pontos devem ser maiores que zero")
                return

            # Confirmar adição
            if messagebox.askyesno("Confirmar", "Deseja adicionar esta questão?"):
                cursor.execute("""
                    INSERT INTO perguntas (pergunta, opcao_a, opcao_b, opcao_c, opcao_d, resposta_certa, pontos)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (campos['Pergunta'], campos['Opção A'], campos['Opção B'], 
                     campos['Opção C'], campos['Opção D'], resposta_certa, pontos))
                conexao.commit()

                # Limpar campos
                for entry in self.entries.values():
                    entry.delete(0, 'end')

                messagebox.showinfo("Sucesso", "Questão adicionada com sucesso!")

        except ValueError:
            messagebox.showerror("Erro", "Por favor, insira números válidos para resposta certa e pontos")
        except sqlite3.Error as e:
            messagebox.showerror("Erro", f"Erro ao salvar no banco de dados: {str(e)}")

    def listar_questoes(self):
        # Limpar interface atual
        for widget in self.master.winfo_children():
            widget.destroy()
        
        # Criar interface de listagem
        scrollable_frame = ctk.CTkScrollableFrame(self.master, width=1240, height=700)
        scrollable_frame.place(relx=0.5, rely=0.5, anchor="center")

        # Buscar questões do banco
        cursor.execute("SELECT * FROM perguntas")
        questoes = cursor.fetchall()

        for numero, questao in enumerate(questoes):
            label_numero = ctk.CTkLabel(scrollable_frame, text=f"Questão {numero + 1}.")
            label_numero.grid(row=numero, column=0, pady=20) 

            label_questao = ctk.CTkLabel(scrollable_frame, text=questao[1])
            label_questao.grid(row=numero, column=1, padx=10, pady=20)  

            imagem_botao = ctk.CTkImage(light_image=Image.open("img/botao-editar.png"),
                               dark_image=Image.open("img/botao-editar.png"),
                               size=(20, 20))

            btn_questao = ctk.CTkButton(
                scrollable_frame, 
                text="", 
                image=imagem_botao, 
                width=20, 
                height=20, 
                command=lambda n=numero, q=questao: self.editar_questao(n, q)
            )      
            btn_questao.grid(row=numero, column=2, padx=30, pady=5)

        btn_voltar = ctk.CTkButton(self.master, text="Voltar", 
                                  command=self.criar_interface, **button_configs)
        btn_voltar.place(relx=0.5, rely=0.9, anchor='center')

    def editar_questao(self, numero, questao):
        # Similar implementation to test.py's edit_questao, but with validations
        # ... (implement the edit interface) ...
        
        def salvar_edicao():
            try:
                # Validações similares ao adicionar_questao
                if messagebox.askyesno("Confirmar", "Deseja salvar as alterações?"):
                    # Executar update
                    cursor.execute("""
                        UPDATE perguntas 
                        SET pergunta=?, opcao_a=?, opcao_b=?, opcao_c=?, opcao_d=?, 
                            resposta_certa=?, pontos=? 
                        WHERE id=?
                    """, (nova_pergunta, nova_opcao_a, nova_opcao_b, nova_opcao_c, 
                         nova_opcao_d, nova_resposta, novos_pontos, questao[0]))
                    conexao.commit()
                    messagebox.showinfo("Sucesso", "Questão atualizada com sucesso!")
                    self.listar_questoes()
            except ValueError:
                messagebox.showerror("Erro", "Por favor, verifique os valores numéricos")
            except sqlite3.Error as e:
                messagebox.showerror("Erro", f"Erro ao atualizar: {str(e)}")


if __name__ == "__main__":
    configuracao = Configuracao(app)
    app.mainloop()






conexao.commit()
conexao.close()