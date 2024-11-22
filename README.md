# 🎮 Sistema de Quiz Game

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8+-blue.svg" alt="Python Version">
  <img src="https://img.shields.io/badge/License-MIT-green.svg" alt="License">
  <img src="https://img.shields.io/badge/Status-Em%20Desenvolvimento-yellow.svg" alt="Status">
  <img src="https://img.shields.io/badge/CustomTkinter-5.1.2-purple.svg" alt="CustomTkinter">
  <img src="https://img.shields.io/badge/SQLite-3.0+-orange.svg" alt="SQLite">
</p>

## 📑 Índice
1. [Descrição](#-descrição)
2. [Objetivos](#-objetivos-do-projeto)
3. [Características](#-principais-características)
4. [Começando](#-começando)
5. [Estrutura do Projeto](#-estrutura-do-projeto)
6. [Metodologia de Desenvolvimento](#-metodologia-de-desenvolvimento)
   - [Fase 1: Análise](#fase-1-análise-)
   - [Fase 2: Planejamento](#fase-2-planejamento-)
   - [Fase 3: Desenho](#fase-3-desenho-)
   - [Fase 4: Programação e Teste](#fase-4-programação-e-teste-)
   - [Documentação e Avaliação](#documentação-e-avaliação-)
   - [Apresentação e Conclusão](#apresentação-e-conclusão-)
7. [Documentação Técnica](#-documentação-técnica)
8. [Desenvolvimento](#-desenvolvimento)
9. [Contribuindo](#-contribuindo)
10. [Licença](#-licença)
11. [Autores](#-autores)

## 📝 Descrição
Sistema de quiz interativo desenvolvido em Python utilizando CustomTkinter para interface gráfica e SQLite para persistência de dados. O sistema permite gerenciar perguntas, jogadores e configurações do jogo, oferecendo uma experiência educativa e divertida.

### 🎯 Objetivos do Projeto
- 📚 Criar um sistema de quiz interativo e educativo
  - Sistema de perguntas e respostas múltipla escolha
  - Feedback imediato de acertos e erros
  - Diferentes níveis de dificuldade
  - Sistema de pontuação dinâmico

- 🎨 Implementar interface gráfica moderna e intuitiva
  - Design moderno com CustomTkinter
  - Navegação fluida entre telas
  - Feedback visual das ações
  - Temporizador visual para questões

- 💾 Gerenciar dados de forma eficiente com SQLite
  - Armazenamento de perguntas e respostas
  - Sistema de pontuação por jogador
  - Histórico de partidas
  - Configurações personalizáveis do jogo

- 🔄 Sistema de Gerenciamento Completo
  - Gerenciamento de jogadores (criar, editar, deletar)
  - Controle de questões (adicionar, editar, remover)
  - Configurações ajustáveis (tempo, número de questões)
  - Sistema de ranking e pontuação

## �� Principais Características

### 🎮 Sistema de Jogo
- Interface gráfica moderna com CustomTkinter
- Sistema de pontuação baseado em tempo e dificuldade
- Gerenciamento de múltiplos jogadores
- Configurações personalizáveis

### 📊 Estrutura de Dados
```sql
-- Tabela de Jogadores
CREATE TABLE jogadores (
    id INTEGER PRIMARY KEY,
    nome TEXT NOT NULL,
    pontos INTEGER DEFAULT 0,
    acertos INTEGER DEFAULT 0,
    erros INTEGER DEFAULT 0
);

-- Tabela de Perguntas
CREATE TABLE perguntas (
    id INTEGER PRIMARY KEY,
    pergunta TEXT NOT NULL,
    opcao_a TEXT,
    opcao_b TEXT,
    opcao_c TEXT,
    opcao_d TEXT,
    opcao_e TEXT,
    resposta_certa INTEGER,
    pontos INTEGER
);

-- Tabela de Configuração
CREATE TABLE configuracao (
    id INTEGER PRIMARY KEY,
    numero_questoes INTEGER DEFAULT 5,
    tempo_questao INTEGER DEFAULT 30,
    jogador_atual INTEGER,
    FOREIGN KEY(jogador_atual) REFERENCES jogadores(id)
);
```

### 🎮 Sistema de Pontuação

O sistema utiliza uma pontuação baseada na dificuldade das questões, conforme definido no campo `dificuldade` da tabela `perguntas`. A pontuação é acumulada por jogador e armazenada na tabela `jogadores`.

#### Distribuição por Nível
```python
# Sistema de pesos para dificuldade
pesos = {
    "facil": [50, 30, 15, 4, 1],     # Maior chance de questões fáceis
    "medio": [15, 40, 30, 10, 5],    # Distribuição equilibrada
    "dificil": [5, 15, 30, 30, 20]   # Maior chance de questões difíceis
}
```

## 🚀 Começando

### 📋 Pré-requisitos

#### 💻 Sistema
- [Python 3.8+](https://www.python.org/downloads/)
- [SQLite3](https://www.sqlite.org/download.html)
- Bibliotecas Python necessárias:
  - [CustomTkinter](https://customtkinter.tomschimansky.com/)
  - [Pillow (PIL)](https://pillow.readthedocs.io/en/stable/)
  - [Pandas](https://pandas.pydata.org/docs/)
  - [Tkinter](https://docs.python.org/3/library/tkinter.html) (incluído no Python)

### 📦 Instalação

1. **Clone o Repositório**
```bash
git clone https://github.com/seu-usuario/quiz-game.git
cd quiz-game
```

2. **Instale as Dependências**
```bash
pip install customtkinter
pip install pillow
pip install pandas
```

3. **Configure o SQLite**
- Para Windows: Baixe o [Precompiled Binaries for Windows](https://www.sqlite.org/download.html)
- Para Linux: `sudo apt-get install sqlite3`
- Para macOS: SQLite já vem instalado

4. **Configure o Python**
- Baixe a versão mais recente do [Python](https://www.python.org/downloads/)
- Durante a instalação, marque a opção "Add Python to PATH"
- Verifique a instalação com `python --version`

## 🧮 Estrutura do Projeto

### 📁 Arquivos Principais
- `game_quiz.py`: Interface principal e lógica do jogo
- `configuracao.py`: Sistema de configurações
- `config_global.py`: Constantes e configurações globais
- `database/quiz_game.db`: Banco de dados SQLite

### 🔄 Fluxo do Sistema
```mermaid
graph TD
    A[Menu Principal] --> B[Iniciar Jogo]
    A --> C[Configurações]
    A --> D[Pontuação dos Jogadores]
    A --> E[Sair]
    
    B --> F[Seleção de Dificuldade]
    F --> G[Fácil]
    F --> H[Médio]
    F --> I[Difícil]
    
    G & H & I --> J[Questionário]
    J --> K[Página de Resposta]
    K --> A
    
    C --> L[Gerenciar Questões]
    C --> M[Configurar Jogo]
    C --> N[Gerenciar Jogador]
    
    L --> O[Adicionar Questão]
    L --> P[Editar Questão]
    L --> Q[Deletar Questão]
    
    M --> R[Número de Questões]
    M --> S[Tempo por Questão]
    
    N --> X[Gerenciar Jogador]
    X --> Y[Adicionar Jogador]
    X --> Z[Editar Jogador]
    X --> AA[Deletar Jogador]
    X --> BB[Zerar Pontuação]
```

### ⚙️ Classes Principais

#### MenuPrincipal
- Gerencia a interface principal
- Controla navegação entre telas
- Mantém conexão com banco de dados

#### Questionario
- Implementa lógica do quiz
- Gerencia tempo e pontuação
- Controla fluxo de perguntas
- Distribui questões por dificuldade
- Calcula pontuação dinâmica

#### PaginaResposta
- Mostra resultados
- Calcula pontuação final
- Atualiza estatísticas do jogador
- Permite reiniciar ou sair

#### PaginaJogador
- Gerencia cadastro de jogadores
- Controla pontuações e estatísticas
- Permite zerar pontuação
- Mantém histórico de partidas

#### PaginaQuestoes
- Gerencia banco de questões
- Permite CRUD de questões
- Configura níveis de dificuldade
- Define pontuação por questão

#### PaginaConfiguracao
- Ajusta número de questões por partida
- Define tempo por questão
- Configura jogador atual
- Gerencia configurações globais

## 📚 Metodologia de Desenvolvimento

### Fase 1: Análise ✓
- [x] Problema definido: Sistema de quiz interativo com múltiplas dificuldades
- [x] Análise dos desafios: Interface gráfica, persistência de dados, sistema de pontuação
- [x] Modelo teórico: Sistema de pesos para distribuição de questões e cálculo de pontuação

### Fase 2: Planejamento ✓
- [x] Objetivos definidos: Sistema educativo, interativo e escalável
- [x] Métricas estabelecidas: Tempo de resposta, precisão do usuário, distribuição de dificuldade
- [x] Estratégia de resolução: Arquitetura MVC (Model-View-Controller) com CustomTkinter e SQLite
- [x] Subproblemas identificados:
  - Interface gráfica responsiva
  - Sistema de pontuação dinâmico
  - Gerenciamento de estado
  - Persistência de dados

### Fase 3: Desenho ✓
- [x] Análise de complexidade:
  - Acesso a questões: O(1)
  - Distribuição por dificuldade: O(n)
  - Cálculo de pontuação: O(1)
- [x] Pontos críticos otimizados:
  - Cache de questões
  - Índices de banco de dados

### Fase 4: Programação e Teste ✓
- [x] Implementação:
  - Código modular e orientado a objetos
  - Padrões de projeto aplicados
  - Documentação inline
- [x] Testes realizados:
  - Testes unitários
  - Testes de integração
  - Testes de interface
- [x] Correções implementadas:
  - Tratamento de exceções
  - Validação de entrada
  - Recuperação de erros

### Documentação e Avaliação ✓
- [x] Documentação técnica completa
- [x] Análise de desempenho realizada

### Apresentação e Conclusão ✓
- [x] Melhorias futuras identificadas

## 📚 Melhorias Futuras

### 💯 Sistema de Pontuação Avançado
- **Penalização por Erros**
  - Fácil: -5 pontos
  - Médio: -15 pontos
  - Difícil: -30 pontos
- **Justificativa**: Adicionar risco/recompensa ao selecionar dificuldades maiores

### 🌐 Migração para API REST
- **Benefícios**:
  - Melhor escalabilidade
  - Separação clara entre frontend e backend
  - Cache mais eficiente

### 🎮 Modos de Jogo Adicionais
- **Modo Contra o Tempo**: Pontuação baseada no tempo de resposta
- **Modo Torneio**: Eliminatórias com múltiplas rodadas

### 📊 Analytics e Estatísticas
- Gráficos de progresso do jogador
- Análise de questões mais erradas/acertadas
- Tempo médio por tipo de questão
- Padrões de resposta por dificuldade

### 🎨 Melhorias de Interface
- Temas personalizáveis- Modo escuro/claro

## 📚 Documentação Técnica

### 🔍 Algoritmos Principais

#### Distribuição de Questões
O algoritmo de distribuição de questões utiliza um sistema de pesos para selecionar questões baseado na dificuldade escolhida:

```python
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
```

#### Sistema de Pontuação
```python
# Cálculo de pontuação baseado na dificuldade da questão
pontos_totais = 0
for indice_questao, resposta in respostas:
    if resposta != -1:  
        questao = questoes[indice_questao]
        resposta_correta = int(questao[7])
        if resposta == resposta_correta:
            self.corretas += 1
            pontos_totais += int(questao[8])
```

### 📊 Estruturas de Dados


**Complexidade**:
- Acesso: O(1)
- Inserção: O(1)
- Espaço: O(n), onde n é tamanho_max


### 🔍 Análise de Complexidade

#### Conceitos Básicos

**Complexidade Temporal**
- Mede o tempo de execução do algoritmo em relação ao tamanho da entrada
- Expressa em notação Big O: O(n), O(1), O(log n), etc.
- Exemplos:
  - O(1): tempo constante, independente do tamanho da entrada
  - O(n): tempo linear, cresce proporcionalmente com a entrada
  - O(log n): tempo logarítmico, cresce mais lentamente que linear

**Complexidade Espacial**
- Mede o uso de memória adicional necessária pelo algoritmo
- Também expressa em notação Big O
- Exemplos:
  - O(1): espaço constante, independente da entrada
  - O(n): espaço linear, cresce proporcionalmente com a entrada
  - O(m): espaço proporcional a um subconjunto da entrada

#### Operações Principais

| Operação | Complexidade Temporal | Complexidade Espacial | Descrição |
|----------|---------------------|---------------------|------------|
| Carregar Quiz | O(n) | O(m) | Carrega questões do banco e aplica distribuição por dificuldade |
| Selecionar Questão | O(1) | O(1) | Acesso direto via cache LRU |
| Calcular Pontuação | O(1) | O(1) | Cálculo baseado em fórmula constante |
| Atualizar Ranking | O(log n) | O(1) | Atualização via índice B-tree |
| Salvar Progresso | O(1) | O(1) | Operação única de update no banco |


#### Fatores de Complexidade

- **n**: número total de questões no banco
  - Impacta carregamento inicial
  - Afeta distribuição por dificuldade

- **m**: número de questões selecionadas
  - Determina tamanho do cache
  - Influencia memória utilizada


### 🔄 Gerenciamento de Estado

1. **Padrão Observer**
   - Atualização reativa da interface
   - Propagação de eventos

2. **Máquina de Estados**
   - Controle de fluxo do quiz
   - Transições validadas

## 🛠️ Desenvolvimento

### 🔧 Configuração do Ambiente de Desenvolvimento
1. Configure seu editor (VS Code recomendado)
2. Instale as extensões Python necessárias
3. Configure o linter e formatter

## 🤝 Contribuindo

1. Fork o projeto
2. Crie sua Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add: nova funcionalidade'`)
4. Push para a Branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request


## 👥 Autores

* **Anderson Gabriel da Silva Campos** - *Desenvolvedor Principal* - [DutsTate0213](https://github.com/DutsTate0213)
* **João Pedro Marques Boa Sorte Soares** - *Produção de Questões* 
* **Eduardo Moura e Silva** - *Produção de Questões* 


---
⌨️ com ❤️ por [DutsTate0213](https://github.com/DutsTate0213) 😊