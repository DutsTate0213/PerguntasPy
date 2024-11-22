import sqlite3

conexao = sqlite3.connect("database/quiz_game.db")
cursor = conexao.cursor()

# cursor.execute("DELETE FROM perguntas")

cursor.execute("""
INSERT INTO perguntas (pergunta, opcao_a, opcao_b, opcao_c, opcao_d, opcao_e, resposta_certa, pontos) 
VALUES
('Qual é o protocolo principal usado para envio de e-mails?', 'HTTP', 'FTP', 'SMTP', 'TCP', 'UDP', 2, 20),
('O que significa a sigla SQL?', 'Standard Query Language', 'Structured Question Language', 'System Quality Language', 'Structured Query Language', 'Standard Quality Language', 3, 20),
('Qual destes não é um tipo de linguagem de programação?', 'Compilada', 'Interpretada', 'Marcação', 'Transpilada', 'Executada', 4, 20),
('O que significa a sigla API?', 'Application Programming Interface', 'Advanced Programming Interface', 'Application Process Integration', 'Advanced Process Integration', 'Automated Programming Interface', 0, 20),
('Qual destes não é um princípio da programação orientada a objetos?', 'Encapsulamento', 'Herança', 'Polimorfismo', 'Abstração', 'Concatenação', 4, 20),
('O que é um algoritmo de busca binária?', 'Busca em árvores', 'Busca em listas ordenadas', 'Busca em grafos', 'Busca em tabelas hash', 'Busca em matrizes', 1, 20),
('Qual é a complexidade de tempo média do algoritmo QuickSort?', 'O(n)', 'O(n log n)', 'O(n²)', 'O(log n)', 'O(2^n)', 1, 20),
('O que significa a sigla HTML?', 'Hyper Text Markup Language', 'High Tech Modern Language', 'Hyper Transfer Markup Language', 'High Text Machine Language', 'Hyper Tech Micro Language', 0, 20),
('Qual destes não é um tipo de banco de dados?', 'Relacional', 'NoSQL', 'Orientado a objetos', 'Hierárquico', 'Binário', 4, 20),
('O que é um deadlock em sistemas operacionais?', 'Erro de compilação', 'Conflito de recursos', 'Falha de hardware', 'Vírus de computador', 'Sobrecarga de memória', 1, 20),
('Qual é a função principal de um compilador?', 'Executar código', 'Depurar código', 'Traduzir código-fonte para código de máquina', 'Otimizar código', 'Gerenciar memória', 2, 20),
('O que é um firewall em segurança de redes?', 'Antivírus', 'Sistema de backup', 'Barreira de segurança', 'Gerenciador de senhas', 'Criptografia de dados', 2, 20),
('Qual destes não é um paradigma de programação?', 'Imperativo', 'Declarativo', 'Funcional', 'Orientado a objetos', 'Sequencial', 4, 20),
('O que é um ponteiro em linguagens de programação?', 'Variável que armazena endereços de memória', 'Função que retorna valores', 'Estrutura de controle de fluxo', 'Tipo de dado primitivo', 'Operador lógico', 0, 20),
('Qual é o propósito principal do protocolo HTTPS?', 'Transferência de arquivos', 'Comunicação segura', 'Gerenciamento de redes', 'Streaming de vídeo', 'Compartilhamento de arquivos', 1, 20),
('O que é um buffer overflow?', 'Sobrecarga de CPU', 'Falha de segurança', 'Erro de compilação', 'Otimização de código', 'Tipo de algoritmo', 1, 40),
('Qual é a diferença principal entre threads e processos?', 'Velocidade de execução', 'Compartilhamento de memória', 'Prioridade no sistema', 'Consumo de energia', 'Tamanho do código', 1, 40),
('O que é um ataque de negação de serviço (DoS)?', 'Roubo de dados', 'Sobrecarga intencional de sistemas', 'Invasão de sistemas', 'Criptografia maliciosa', 'Falsificação de identidade', 1, 40),
('Qual é o princípio fundamental do algoritmo MapReduce?', 'Busca em profundidade', 'Divisão e conquista', 'Programação dinâmica', 'Backtracking', 'Força bruta', 1, 40),
('O que é um design pattern em desenvolvimento de software?', 'Ferramenta de design gráfico', 'Solução reutilizável para problemas comuns', 'Linguagem de programação', 'Framework de teste', 'Sistema de controle de versão', 1, 40),
('O que é o problema do caixeiro viajante em teoria da computação?', 'Problema de roteamento', 'Problema de ordenação', 'Problema de criptografia', 'Problema de compressão', 'Problema de otimização de banco de dados', 0, 40),
('Qual é o princípio do algoritmo de criptografia RSA?', 'Substituição simples', 'Chave simétrica', 'Fatoração de números primos', 'Compressão de dados', 'Hash criptográfico', 2, 40),
('O que é um ataque de injeção SQL?', 'Sobrecarga de banco de dados', 'Exploração de vulnerabilidades em consultas', 'Criptografia de dados', 'Otimização de consultas', 'Backup de banco de dados', 1, 40),
('Qual é a diferença entre Big O, Big Theta e Big Omega na análise de algoritmos?', 'Precisão da medição', 'Limites de complexidade', 'Tipos de algoritmos', 'Métodos de ordenação', 'Estruturas de dados', 1, 40),
('O que é um blockchain em tecnologia da informação?', 'Tipo de firewall', 'Estrutura de dados distribuída', 'Protocolo de rede', 'Linguagem de programação', 'Sistema operacional', 1, 40),
('Qual é o princípio do algoritmo de compressão Huffman?', 'Codificação run-length', 'Codificação baseada em frequência', 'Transformada de Fourier', 'Compressão fractal', 'Codificação delta', 1, 40),
('O que é um ataque de força bruta em segurança da informação?', 'Exploração de vulnerabilidades de software', 'Tentativa sistemática de todas as possibilidades', 'Engenharia social', 'Interceptação de tráfego de rede', 'Exploração de buffer overflow', 1, 40),
('Qual é o propósito principal de um garbage collector em linguagens de programação?', 'Otimização de código', 'Gerenciamento automático de memória', 'Depuração de código', 'Compilação just-in-time', 'Verificação de tipos', 1, 40),
('O que é um sistema distribuído em computação?', 'Sistema com múltiplos processadores', 'Sistema com componentes em diferentes locais', 'Sistema operacional multiusuário', 'Sistema de arquivos em rede', 'Sistema de virtualização', 1, 40),
('Qual é o princípio do algoritmo de consenso Proof of Work usado em criptomoedas?', 'Votação distribuída', 'Resolução de problemas computacionais', 'Assinatura digital', 'Criptografia simétrica', 'Roteamento de pacotes', 1, 40),
('O que é um ataque de man-in-the-middle?', 'Interceptação de comunicação', 'Sobrecarga de servidor', 'Exploração de buffer overflow', 'Injeção de código', 'Negação de serviço', 0, 40),
('Qual é a diferença principal entre machine learning e deep learning?', 'Velocidade de processamento', 'Complexidade das redes neurais', 'Tipo de dados utilizados', 'Aplicações práticas', 'Necessidade de supervisão humana', 1, 40),
('O que é um sistema de arquivos distribuído?', 'Sistema de backup em nuvem', 'Sistema de armazenamento em múltiplos dispositivos', 'Sistema de compressão de arquivos', 'Sistema de criptografia de dados', 'Sistema de indexação de arquivos', 1, 40),
('Qual é o princípio do algoritmo de roteamento OSPF?', 'Roteamento baseado em distância', 'Roteamento baseado em estado de enlace', 'Roteamento estático', 'Roteamento por vetor de distância', 'Roteamento hierárquico', 1, 40),
('O que é um ataque de phishing?', 'Sobrecarga de servidor', 'Engenharia social para obter informações', 'Exploração de vulnerabilidades de software', 'Interceptação de tráfego de rede', 'Negação de serviço distribuído', 1, 40),
('Qual é a diferença entre compilação e interpretação em linguagens de programação?', 'Velocidade de execução', 'Portabilidade do código', 'Uso de memória', 'Complexidade do código', 'Paradigma de programação', 1, 40),
('O que é um sistema de detecção de intrusão (IDS)?', 'Firewall avançado', 'Sistema de monitoramento de rede', 'Antivírus em tempo real', 'Sistema de backup automático', 'Gerenciador de senhas', 1, 40),
('Qual é o princípio do algoritmo de criptografia AES?', 'Criptografia de chave pública', 'Criptografia de bloco simétrica', 'Criptografia de fluxo', 'Hash criptográfico', 'Criptografia quântica', 1, 40),
('O que é um ataque de cross-site scripting (XSS)?', 'Injeção de código malicioso em websites', 'Exploração de vulnerabilidades de servidor', 'Interceptação de cookies', 'Negação de serviço distribuído', 'Falsificação de identidade', 0, 40),
('Qual é a diferença entre virtualização e containerização?', 'Consumo de recursos', 'Isolamento de processos', 'Portabilidade', 'Velocidade de inicialização', 'Segurança', 1, 40),
('O que é um sistema de arquivos journaling?', 'Sistema de backup incremental', 'Sistema de registro de transações', 'Sistema de compressão em tempo real', 'Sistema de criptografia de disco', 'Sistema de indexação de arquivos', 1, 40),
('Qual é o princípio do algoritmo de consenso Proof of Stake?', 'Resolução de problemas computacionais', 'Posse de moedas como garantia', 'Votação distribuída', 'Assinatura digital múltipla', 'Mineração de dados', 1, 40),
('O que é um ataque de buffer overflow?', 'Sobrecarga de memória', 'Injeção de SQL', 'Negação de serviço', 'Interceptação de pacotes', 'Engenharia social', 0, 40),
('Qual é a diferença entre um array e uma lista encadeada?', 'Velocidade de acesso', 'Uso de memória', 'Flexibilidade de tamanho', 'Complexidade de implementação', 'Ordenação dos elementos', 2, 40),
('O que é um sistema de gerenciamento de banco de dados (SGBD)?', 'Software para criar backups', 'Interface para consultas SQL', 'Sistema para administrar dados', 'Ferramenta de modelagem de dados', 'Protocolo de comunicação de rede', 2, 40),
('Qual é o princípio do algoritmo de hash SHA-256?', 'Compressão de dados', 'Criptografia simétrica', 'Função de resumo criptográfico', 'Codificação de caracteres', 'Compactação sem perdas', 2, 40),
('O que é um ataque de dia zero (zero-day)?', 'Ataque em massa', 'Exploração de vulnerabilidade desconhecida', 'Negação de serviço prolongada', 'Sequestro de dados em larga escala', 'Invasão de múltiplos sistemas', 1, 40),
('Qual é a diferença entre IPv4 e IPv6?', 'Velocidade de transmissão', 'Tamanho do endereço IP', 'Protocolo de segurança', 'Método de roteamento', 'Compatibilidade com dispositivos', 1, 40)        
""")
conexao.commit()



conexao.commit()
conexao.close()
