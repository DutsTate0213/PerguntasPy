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

# cursor.execute("CREATE TABLE IF NOT EXISTS perguntas (id INTEGER PRIMARY KEY AUTOINCREMENT, pergunta TEXT, opcao_a TEXT, opcao_b TEXT, opcao_c TEXT, opcao_d TEXT, opcao_e TEXT, resposta_certa INTEGER, pontos INTEGER)")
# cursor.execute("CREATE TABLE IF NOT EXISTS configuracao (id INTEGER PRIMARY KEY AUTOINCREMENT, numero_questoes INTEGER, tempo_questao INTEGER, jogador_atual INTEGER)")
# cursor.execute("CREATE TABLE IF NOT EXISTS jogadores (id INTEGER PRIMARY KEY AUTOINCREMENT, nome TEXT, pontos INTEGER, acertos INTEGER, erros INTEGER)")
# conexao.commit()

# cursor.execute("DELETE FROM perguntas")
# conexao.commit()

cursor.execute("""
INSERT INTO perguntas (pergunta, opcao_a, opcao_b, opcao_c, opcao_d, opcao_e, resposta_certa, pontos) 
VALUES
('Qual é a cor do tomate maduro?', 'Amarelo', 'Vermelho', 'Verde', 'Azul', 'Preto', 1, 5),
('Quantos lados tem um triângulo?', '2', '3', '4', '5', '6', 1, 5),
('Qual é o número da metade de 10?', '2', '3', '4', '5', '6', 3, 5),
('Quantos dedos temos nas mãos?', '8', '9', '10', '11', '12', 2, 5),
('Qual é o animal conhecido como o melhor amigo do homem?', 'Gato', 'Cavalo', 'Cachorro', 'Coelho', 'Peixe', 2, 5),
('Quanto é 1 + 1?', '1', '2', '3', '4', '5', 1, 5),
('Qual é a bebida mais consumida no mundo depois da água?', 'Café', 'Chá', 'Suco', 'Refrigerante', 'Leite', 1, 5),
('Qual é o país do samba e do futebol?', 'Argentina', 'Brasil', 'Portugal', 'Espanha', 'México', 1, 5),
('Qual é o nome do nosso planeta?', 'Lua', 'Terra', 'Marte', 'Sol', 'Júpiter', 1, 5),
('Quantos olhos tem uma pessoa comum?', '1', '2', '3', '4', '5', 1, 5),
('Qual é o nome do rio que atravessa o Egito?', 'Nilo', 'Amazonas', 'Ganges', 'Yangtzé', 'Mississippi', 0, 10),
('Qual é o maior país do mundo em território?', 'Canadá', 'Rússia', 'China', 'Estados Unidos', 'Brasil', 1, 10),
('Quantos meses tem um ano?', '10', '11', '12', '13', '14', 2, 10),
('Qual é o maior estado do Brasil?', 'Amazonas', 'Pará', 'São Paulo', 'Minas Gerais', 'Bahia', 0, 10),
('Em que continente fica a Austrália?', 'África', 'Europa', 'América', 'Oceania', 'Ásia', 3, 10),
('Qual é o nome do animal que tem o pescoço mais longo?', 'Cavalo', 'Girafa', 'Elefante', 'Jacaré', 'Rinoceronte', 1, 10),
('Qual é o maior oceano do mundo?', 'Atlântico', 'Pacífico', 'Índico', 'Ártico', 'Antártico', 1, 10),
('Qual é a moeda oficial do Brasil?', 'Dólar', 'Euro', 'Real', 'Peso', 'Iene', 2, 10),
('Qual é o planeta mais próximo do Sol?', 'Mercúrio', 'Vênus', 'Terra', 'Marte', 'Júpiter', 0, 10),
('Qual esporte é conhecido como "o esporte das multidões"?', 'Basquete', 'Vôlei', 'Futebol', 'Tênis', 'Atletismo', 2, 10),
('Quem foi o primeiro presidente do Brasil?', 'Juscelino Kubitschek', 'Dom Pedro II', 'Getúlio Vargas', 'Deodoro da Fonseca', 'Floriano Peixoto', 3, 20),
('Quantos continentes existem no planeta Terra?', '5', '6', '7', '8', '9', 2, 20),
('Qual é o idioma oficial da China?', 'Chinês', 'Mandarim', 'Cantonês', 'Coreano', 'Japonês', 1, 20),
('Quem é conhecido como o Rei do Rock?', 'Elvis Presley', 'Michael Jackson', 'Freddie Mercury', 'Frank Sinatra', 'John Lennon', 0, 20),
('Qual é a capital da Espanha?', 'Lisboa', 'Barcelona', 'Madri', 'Sevilha', 'Valência', 2, 20),
('Quem descobriu o Brasil?', 'Pedro Álvares Cabral', 'Cristóvão Colombo', 'Américo Vespúcio', 'Fernão de Magalhães', 'Bartolomeu Dias', 0, 20),
('Qual é a unidade básica da vida?', 'Célula', 'Átomo', 'Molécula', 'Gene', 'Tecido', 0, 20),
('Quantos planetas existem no sistema solar?', '7', '8', '9', '10', '11', 1, 20),
('Qual é o maior animal do mundo?', 'Elefante', 'Baleia Azul', 'Rinoceronte', 'Urso Polar', 'Cavalo', 1, 20),
('Quem escreveu "Hamlet"?', 'Victor Hugo', 'Shakespeare', 'Machado de Assis', 'Charles Dickens', 'Kafka', 1, 20),
('Quem pintou "Guernica"?', 'Van Gogh', 'Picasso', 'Dalí', 'Monet', 'Cézanne', 1, 40),
('Em que ano terminou a Primeira Guerra Mundial?', '1917', '1918', '1919', '1920', '1921', 1, 40),
('Qual é a maior cadeia de montanhas do mundo?', 'Himalaia', 'Andes', 'Rochosas', 'Alpes', 'Pirineus', 0, 40),
('Qual cientista descobriu a penicilina?', 'Newton', 'Einstein', 'Fleming', 'Darwin', 'Bohr', 2, 40),
('Quantos elementos há na tabela periódica?', '112', '118', '120', '125', '130', 1, 40),
('Qual é o nome do líder da Revolução Russa de 1917?', 'Lênin', 'Trotsky', 'Stalin', 'Gorbachev', 'Khrushchev', 0, 40),
('Em que país está localizada a Grande Muralha?', 'Coreia do Sul', 'China', 'Japão', 'Mongólia', 'Vietnã', 1, 40),
('Qual era o nome do barco de Cristóvão Colombo?', 'Pinta', 'Santa Maria', 'Nina', 'Mayflower', 'Endeavour', 1, 40),
('Qual gás é essencial para a respiração?', 'Hidrogênio', 'Oxigênio', 'Nitrogênio', 'Dióxido de Carbono', 'Metano', 1, 40),
('Qual foi o primeiro satélite lançado ao espaço?', 'Apollo 11', 'Sputnik', 'Hubble', 'Voyager', 'Luna', 1, 40),
('Qual é a distância aproximada entre a Terra e a Lua em km?', '384.400', '300.000', '450.000', '500.000', '600.000', 0, 80),
('Quem formulou as três leis do movimento?', 'Galileu Galilei', 'Isaac Newton', 'Einstein', 'Kepler', 'Copérnico', 1, 80),
('Qual é a capital da Mongólia?', 'Pequim', 'Ulã Bator', 'Hanoi', 'Seul', 'Bangkok', 1, 80),
('Qual é a maior floresta tropical do mundo?', 'Floresta Amazônica', 'Floresta Negra', 'Floresta do Congo', 'Floresta Boreal', 'Floresta Australiana', 0, 80),
('Qual é o nome do primeiro computador eletrônico?', 'UNIVAC', 'ENIAC', 'IBM 701', 'Z3', 'Mark I', 1, 80),
('Quem foi o faraó que ordenou a construção da Grande Pirâmide de Gizé?', 'Tutancâmon', 'Ramsés II', 'Quéops', 'Amenófis', 'Cleópatra', 2, 80),
('Qual é a fórmula da velocidade da luz no vácuo?', '2.99 x 10^8 m/s', '3.00 x 10^8 m/s', '3.01 x 10^8 m/s', '2.98 x 10^8 m/s', '3.02 x 10^8 m/s', 1, 80),
('Qual cientista propôs a teoria do Big Bang?', 'Hubble', 'Lemaître', 'Einstein', 'Bohr', 'Newton', 1, 80),
('Quem escreveu "A Divina Comédia"?', 'Dante Alighieri', 'Shakespeare', 'Goethe', 'Petrarca', 'Victor Hugo', 0, 80),
('Em que ano foi fundada a cidade de Roma?', '753 a.C.', '1000 a.C.', '500 a.C.', '300 a.C.', '600 a.C.', 0, 80)
""")
conexao.commit()

cursor.close()
conexao.close()
