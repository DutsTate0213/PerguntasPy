import sqlite3
import customtkinter as ctk

conexao = sqlite3.connect("database/banco.db")

cursor = conexao.cursor()

cursor.execute("CREATE TABLE IF NOT EXISTS perguntas (id INTEGER PRIMARY KEY AUTOINCREMENT, pergunta TEXT, opcao_a TEXT, opcao_b TEXT, opcao_c TEXT, opcao_d TEXT, resposta_certa INTEGER, pontos INTEGER)")
cursor.execute("CREATE TABLE IF NOT EXISTS configuracao (id INTEGER PRIMARY KEY AUTOINCREMENT, numero_questoes INTEGER, tempo_questao INTEGER)")
cursor.execute("CREATE TABLE IF NOT EXISTS jogadores (id INTEGER PRIMARY KEY AUTOINCREMENT, nome TEXT, pontos INTEGER, acertos INTEGER, erros INTEGER)")


app = ctk.CTk()
app.geometry("300x200")
app.title("Configuração")

class Configuracao:
    def __init__(self, master):
        self.master = master





if __name__ == "__main__":
    app.mainloop()






conexao.commit()
conexao.close()