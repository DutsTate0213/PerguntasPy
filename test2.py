import sqlite3
import customtkinter as ctk
import pandas as pd
from tkinter import messagebox
from PIL import Image

conexao = sqlite3.connect("database/quiz_game.db")
cursor = conexao.cursor()

# cursor.execute("DROP TABLE IF EXISTS perguntas")
# cursor.execute("DROP TABLE IF EXISTS configuracao")
# cursor.execute("DROP TABLE IF EXISTS jogadores")
# conexao.commit()

cursor.execute("CREATE TABLE IF NOT EXISTS perguntas (id INTEGER PRIMARY KEY AUTOINCREMENT, pergunta TEXT, opcao_a TEXT, opcao_b TEXT, opcao_c TEXT, opcao_d TEXT, opcao_e TEXT, resposta_certa INTEGER, pontos INTEGER)")
cursor.execute("CREATE TABLE IF NOT EXISTS configuracao (id INTEGER PRIMARY KEY AUTOINCREMENT, numero_questoes INTEGER, tempo_questao INTEGER)")
cursor.execute("CREATE TABLE IF NOT EXISTS jogadores (id INTEGER PRIMARY KEY AUTOINCREMENT, nome TEXT, pontos INTEGER, acertos INTEGER, erros INTEGER)")
conexao.commit()

# cursor.execute("DELETE FROM perguntas")
# conexao.commit()

cursor.execute("""INSERT INTO perguntas (pergunta, opcao_a, opcao_b, opcao_c, opcao_d, opcao_e, resposta_certa, pontos) 
VALUES
('Qual é a capital da França?', 'Londres', 'Paris', 'Berlim', 'Madrid', 'Roma', 1, 10),
('Quanto é 5 + 3?', '5', '8', '10', '7', '6', 1, 5),
('Qual é o maior planeta do sistema solar?', 'Terra', 'Marte', 'Júpiter', 'Saturno', 'Vênus', 2, 15),
('Quem escreveu "Dom Quixote"?', 'Shakespeare', 'Cervantes', 'Tolstói', 'Dante', 'Kafka', 1, 20),
('Qual é o elemento químico representado pelo símbolo O?', 'Ouro', 'Oxigênio', 'Prata', 'Ósmio', 'Óxido', 1, 10)
""")
conexao.commit()


cursor.close()
conexao.close()
