import sqlite3
import customtkinter as ctk
import pandas as pd
from tkinter import messagebox
from PIL import Image

app = ctk.CTk()
app.geometry("1280x720")
app.title("Configuração")

class PaginaQuestoes:
    def __init__(self, master):
        self.master = master
        self.conexao = sqlite3.connect("database/banco.db")
        self.cursor = self.conexao.cursor()
        
        self.cursor.execute("SELECT * FROM perguntas")
        self.questoes = self.cursor.fetchall()
        btn_abrir_questao = ctk.CTkButton(self.master, text="Abrir Questão", command=self.pagina_questoes)
        btn_abrir_questao.grid(row=0, column=0, padx=20, pady=20)

    def pagina_questoes(self):
        for widget in self.master.winfo_children():
            widget.destroy()
        scrollable_frame = ctk.CTkScrollableFrame(self.master, width=1240, height=700)
        scrollable_frame.place(relx=0.5, rely=0.5, anchor="center")

        btn_adicionar_questao = ctk.CTkButton(self.master, text="Adicionar Questão", command=self.adicionar_questao)
        btn_adicionar_questao.place(relx=0.5, rely=0.9, anchor="center")

        for numero, questao in enumerate(self.questoes):
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
                command=lambda n=numero: self.editar_questao(n)
            )      
            btn_questao.grid(row=numero, column=2, padx=30, pady=5)
    
    def adicionar_questao(self):
        for widget in self.master.winfo_children():
            widget.destroy()
        label_adicionar_questao = ctk.CTkLabel(self.master, text="Adicionar Questão")
        label_adicionar_questao.grid(row=0, column=0, padx=20, pady=20)

        label_enunciado = ctk.CTkLabel(self.master, text="Enunciado:")
        label_enunciado.grid(row=1, column=0, padx=20, pady=20)

        entrada_enunciado = ctk.CTkEntry(self.master, width=720)
        entrada_enunciado.grid(row=1, column=1, padx=20, pady=20)

        label_alternativa_a = ctk.CTkLabel(self.master, text="Alternativa A:")
        label_alternativa_a.grid(row=2, column=0, padx=20, pady=20)

        entrada_alternativa_a = ctk.CTkEntry(self.master, width=720)
        entrada_alternativa_a.grid(row=2, column=1, padx=20, pady=20)

        label_alternativa_b = ctk.CTkLabel(self.master, text="Alternativa B:")
        label_alternativa_b.grid(row=3, column=0, padx=20, pady=20)

        entrada_alternativa_b = ctk.CTkEntry(self.master, width=720)
        entrada_alternativa_b.grid(row=3, column=1, padx=20, pady=20)

        label_alternativa_c = ctk.CTkLabel(self.master, text="Alternativa C:")
        label_alternativa_c.grid(row=4, column=0, padx=20, pady=20)

        entrada_alternativa_c = ctk.CTkEntry(self.master, width=720)
        entrada_alternativa_c.grid(row=4, column=1, padx=20, pady=20)

        label_alternativa_d = ctk.CTkLabel(self.master, text="Alternativa D:")
        label_alternativa_d.grid(row=5, column=0, padx=20, pady=20)

        entrada_alternativa_d = ctk.CTkEntry(self.master, width=720)
        entrada_alternativa_d.grid(row=5, column=1, padx=20, pady=20)

        label_alternativa_e = ctk.CTkLabel(self.master, text="Alternativa E:")
        label_alternativa_e.grid(row=6, column=0, padx=20, pady=20)

        entrada_alternativa_e = ctk.CTkEntry(self.master, width=720)
        entrada_alternativa_e.grid(row=6, column=1, padx=20, pady=20)

        label_resposta_certa = ctk.CTkLabel(self.master, text="Resposta Certa:")
        label_resposta_certa.grid(row=7, column=0, padx=20, pady=20)

        entrada_resposta_certa = ctk.CTkEntry(self.master, width=720)
        entrada_resposta_certa.grid(row=7, column=1, padx=20, pady=20)

        label_pontos = ctk.CTkLabel(self.master, text="Pontos:")
        label_pontos.grid(row=8, column=0, padx=20, pady=20)

        entrada_pontos = ctk.CTkEntry(self.master, width=720)
        entrada_pontos.grid(row=8, column=1, padx=20, pady=20)

        btn_cancelar = ctk.CTkButton(self.master, text="Cancelar", command=self.voltar)
        btn_cancelar.place(relx=0.05, rely=0.9) 
        
        btn_salvar = ctk.CTkButton(self.master, text="Criar Questão", command=lambda: self.salvar_questao(entrada_enunciado.get(), entrada_alternativa_a.get(), entrada_alternativa_b.get(), entrada_alternativa_c.get(), entrada_alternativa_d.get(), entrada_alternativa_e.get(), entrada_resposta_certa.get(), entrada_pontos.get()))
        btn_salvar.place(relx=0.3, rely=0.9)

    def editar_questao(self, numero):
        for widget in self.master.winfo_children():
            widget.destroy()
        
        # Criar as entradas e depois inserir os valores
        label_enunciado = ctk.CTkLabel(self.master, text="Enunciado:")
        label_enunciado.grid(row=0, column=0, padx=20, pady=20)
        
        entrada_enunciado = ctk.CTkEntry(self.master, width=720)
        entrada_enunciado.insert(0, self.questoes[numero][1])
        entrada_enunciado.grid(row=0, column=1, padx=20, pady=20)

        label_alternativa_a = ctk.CTkLabel(self.master, text="Alternativa A:")
        label_alternativa_a.grid(row=1, column=0, padx=20, pady=20)

        entrada_alternativa_a = ctk.CTkEntry(self.master, width=720)
        entrada_alternativa_a.insert(0, self.questoes[numero][2])
        entrada_alternativa_a.grid(row=1, column=1, padx=20, pady=20)

        label_alternativa_b = ctk.CTkLabel(self.master, text="Alternativa B:")
        label_alternativa_b.grid(row=2, column=0, padx=20, pady=20)

        entrada_alternativa_b = ctk.CTkEntry(self.master, width=720)
        entrada_alternativa_b.insert(0, self.questoes[numero][3])
        entrada_alternativa_b.grid(row=2, column=1, padx=20, pady=20)

        label_alternativa_c = ctk.CTkLabel(self.master, text="Alternativa C:")
        label_alternativa_c.grid(row=3, column=0, padx=20, pady=20)

        entrada_alternativa_c = ctk.CTkEntry(self.master, width=720)
        entrada_alternativa_c.insert(0, self.questoes[numero][4])
        entrada_alternativa_c.grid(row=3, column=1, padx=20, pady=20)

        label_alternativa_d = ctk.CTkLabel(self.master, text="Alternativa D:")
        label_alternativa_d.grid(row=4, column=0, padx=20, pady=20)

        entrada_alternativa_d = ctk.CTkEntry(self.master, width=720)
        entrada_alternativa_d.insert(0, self.questoes[numero][5])
        entrada_alternativa_d.grid(row=4, column=1, padx=20, pady=20)

        label_alternativa_e = ctk.CTkLabel(self.master, text="Alternativa E:")
        label_alternativa_e.grid(row=5, column=0, padx=20, pady=20)

        entrada_alternativa_e = ctk.CTkEntry(self.master, width=720)
        entrada_alternativa_e.insert(0, self.questoes[numero][6])
        entrada_alternativa_e.grid(row=5, column=1, padx=20, pady=20)

        label_resposta = ctk.CTkLabel(self.master, text="Resposta Certa:")
        label_resposta.grid(row=6, column=0, padx=20, pady=20)

        entrada_resposta = ctk.CTkEntry(self.master, width=720)
        entrada_resposta.insert(0, self.questoes[numero][7])
        entrada_resposta.grid(row=6, column=1, padx=20, pady=20)

        label_pontos = ctk.CTkLabel(self.master, text="Pontos:")
        label_pontos.grid(row=7, column=0, padx=20, pady=20)

        entrada_pontos = ctk.CTkEntry(self.master, width=720)
        entrada_pontos.insert(0, self.questoes[numero][8])
        entrada_pontos.grid(row=7, column=1, padx=20, pady=20)

        # O resto do código permanece igual
        btn_cancelar = ctk.CTkButton(self.master, text="Cancelar", command=self.voltar)
        btn_cancelar.place(relx=0.05, rely=0.9) 
        
        btn_salvar = ctk.CTkButton(self.master, text="Salvar", command=lambda: self.salvar_questao(numero, entrada_enunciado.get(), entrada_alternativa_a.get(), entrada_alternativa_b.get(), entrada_alternativa_c.get(), entrada_alternativa_d.get(), entrada_alternativa_e.get(), entrada_resposta.get(), entrada_pontos.get()))
        btn_salvar.place(relx=0.3, rely=0.9)

    def voltar(self):
        for widget in self.master.winfo_children():
            widget.destroy()
        self.pagina_questoes()

    def salvar_questao(self, numero, enunciado, alternativa_a, alternativa_b, alternativa_c, alternativa_d, alternativa_e, resposta_certa, pontos):
        # Pegar o ID real da questão usando o índice
        id_questao = self.questoes[numero][0]  # Assumindo que o ID está na primeira coluna
        
        self.cursor.execute("""
            UPDATE perguntas 
            SET pergunta=?, 
                opcao_a=?, 
                opcao_b=?, 
                opcao_c=?, 
                opcao_d=?, 
                opcao_e=?, 
                resposta_certa=?, 
                pontos=? 
            WHERE id=?""", 
            (enunciado, alternativa_a, alternativa_b, alternativa_c, 
             alternativa_d, alternativa_e, resposta_certa, pontos, id_questao)
        )
        self.conexao.commit()
        
        # Atualizar a lista de questões após salvar
        self.cursor.execute("SELECT * FROM perguntas")
        self.questoes = self.cursor.fetchall()
        
        print("Questão salva com sucesso!")
        self.cancelar_edicao()

    def salvar_questao(self, enunciado, alternativa_a, alternativa_b, alternativa_c, alternativa_d, alternativa_e, resposta_certa, pontos):
        self.cursor.execute("""INSERT INTO perguntas (pergunta, opcao_a, opcao_b, opcao_c, opcao_d, opcao_e, resposta_certa, pontos) 
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?)""", 
                            (enunciado, alternativa_a, alternativa_b, alternativa_c, alternativa_d, alternativa_e, resposta_certa, pontos))
        self.conexao.commit()
        print("Questão criada com sucesso!")
        self.voltar()

    def __del__(self):
        if hasattr(self, 'conexao'):
            self.conexao.close()

if __name__ == "__main__":
    PaginaQuestoes(app)
    app.mainloop()