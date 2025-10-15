# Sistema de Monitoramento de Perdas na Colheita de Cana-de-Açúcar

## 👨‍🎓 Integrantes:
- Jorge Augusto Rodrigues Macedo / RM567175
- Lucca de Almeida Benigno / RM566930
- Thiago Costa Sales / RM567889

## 👩‍🏫 Professores:
### Tutora) 
- Ana Cristina dos Santos
### Coordenador(a)
- André Godoi Chiovato

## 📜 Descrição

Este projeto é uma AgroTech, uma solução digital desenvolvida em Python para enfrentar um problema crítico no agronegócio: as perdas na colheita mecanizada de cana-de-açúcar. Apesar de o Brasil ser o maior produtor global, as perdas chegam a 15% da produção, causando grandes prejuízos financeiros aos produtores.

Nossa aplicação atua como um sistema de bordo, permitindo que o produtor rural monitore e gerencie a eficiência de suas colheitadeiras. O objetivo é fornecer dados claros sobre a produtividade e as perdas, possibilitando a tomada de decisões mais precisas para otimizar o processo de colheita.

A solução foi desenvolvida com base nos seguintes conceitos fundamentais de programação:

- Subalgoritmos: O código é modularizado em funções e procedimentos para tornar a lógica mais limpa e organizada.

- Estruturas de Dados: Utilizamos listas e dicionários para criar uma representação de tabela em memória, facilitando a manipulação e o armazenamento temporário de dados.

- Manipulação de Arquivos: Os registros de colheita são salvos e carregados em um formato JSON, garantindo portabilidade e persistência dos dados.

- Conexão com Banco de Dados: A aplicação estabelece uma conexão com um banco de dados Oracle para realizar as operações de CRUD (Create, Read, Update, Delete) de forma segura e duradoura.

- Tratamento de Erros: O sistema é robusto, utilizando blocos try-except para validar as entradas do usuário e tratar possíveis falhas na conexão com o banco de dados.

A interface do programa, embora seja via prompt de comando, é projetada para ser intuitiva e fácil de usar, com um menu claro e dados exibidos de forma organizada para uma melhor usabilidade.

## 🔧 Como executar o código
Para executar a aplicação, siga o passo a passo abaixo:

1- Pré-requisitos: Certifique-se de que o Python está instalado em seu sistema. É necessário também instalar as bibliotecas `oracledb` e `pandas`, que podem ser instaladas via `pip`:

`pip install oracledb pandas`

2 - Configuração do Banco de Dados: Antes de rodar o código, execute o script SQL abaixo no seu ambiente Oracle para criar a tabela TBL_COLHEITA.

`CREATE TABLE TBL_COLHEITA (
    ID NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    ID_COLHEITADEIRA VARCHAR2(30) NOT NULL,
    HECTARES_COLHIDOS FLOAT NOT NULL,
    PERDAS_POR_HA FLOAT NOT NULL,
    PREJUIZO_ESTIMADO FLOAT NOT NULL
);`

3 - Configuração do Código: No arquivo principal, localize a seção de conexão do banco de dados e insira suas credenciais de usuário e senha do Oracle.

Exemplo:
`conn = oracledb.connect(user='[SEU_USUARIO]', password='[SUA_SENHA]', dsn='oracle.fiap.com.br:1521/ORCL')`

4 - Execução: Execute o arquivo Python no terminal.

`python app.py`

A aplicação será iniciada e o menu de opções será exibido.
