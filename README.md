# Projeto: Sistema de Monitoramento de Perdas na Colheita de Cana-de-Açúcar
# Visão Geral do Projeto
Este projeto consiste no desenvolvimento de um sistema em Python para monitorar e gerir as perdas de cana-de-açúcar durante a colheita mecanizada. A solução atua como uma AgroTech, oferecendo uma ferramenta digital para auxiliar produtores rurais na otimização de seus processos e na redução de prejuízos financeiros significativos.

# O Problema no Agronegócio
Apesar de o Brasil ser um líder global na produção de cana-de-açúcar, as perdas na colheita mecanizada são um desafio constante. Essas perdas podem atingir até 15% da produção, resultando em um prejuízo anual de milhões de reais para o setor. A falta de dados precisos e de um sistema de monitoramento em tempo real dificulta a identificação e correção das falhas operacionais, comprometendo a produtividade do negócio.

# A Solução Proposta
A nossa solução é um aplicativo de console em Python que simula um sistema de bordo para colheitadeiras. Ele permite ao usuário (o produtor rural) registrar, visualizar, atualizar e excluir dados de colheitas, oferecendo uma visão clara do desempenho e das perdas.

A aplicação busca inovar ao transformar dados de campo em informações valiosas, permitindo que o produtor tome decisões mais assertivas para reduzir o desperdício e maximizar o lucro.

# Tecnologias e Conceitos de Python Utilizados
O desenvolvimento desta aplicação integra diversos conceitos abordados nos capítulos 3, 4, 5 e 6 do nosso material de estudo:

Subalgoritmos: O código é modularizado em funções e procedimentos, `como exibe_menu()`, `valida_float()` e `registrar_colheita()`, para promover a reutilização de código e uma lógica clara.

Estruturas de Dados: Para armazenar e manipular os dados, foram utilizadas:

Listas: Para criar uma tabela de memória dinâmica, armazenando múltiplos registros.

Dicionários: Cada registro de colheita é estruturado como um dicionário, usando chaves (keys) como `id_colheitadeira` e `perdas_por_ha` para organizar os dados de forma legível.

Manipulação de Arquivos: O sistema salva e lê dados em formato `.json`, garantindo a persistência dos registros de forma estruturada e portátil. Isso foi feito utilizando a biblioteca json para codificar e decodificar os dados.

Conexão com Banco de Dados: A solução se conecta a um banco de dados Oracle para armazenar o histórico de colheitas de forma permanente. As operações de CRUD (Create, Read, Update, Delete) são executadas usando a biblioteca oracledb.

Tratamento de Erros: Foram implementados blocos try-except para prever e lidar com erros de entrada do usuário (como digitar texto em vez de números) e problemas na conexão com o banco de dados, evitando que a aplicação seja encerrada de forma inesperada.

# Como Executar o Projeto
Pré-requisitos: Certifique-se de que o Python e as bibliotecas necessárias (`oracledb`, `pandas`, `json`) estejam instaladas. Você pode instalá-las com o comando:

`pip install oracledb pandas`

Configuração do Banco de Dados: Antes de rodar o código, execute o script SQL abaixo no seu ambiente Oracle para criar a tabela TBL_COLHEITA.

# SQL

`CREATE TABLE TBL_COLHEITA (
    ID NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    ID_COLHEITADEIRA VARCHAR2(30) NOT NULL,
    HECTARES_COLHIDOS FLOAT NOT NULL,
    PERDAS_POR_HA FLOAT NOT NULL,
    PREJUIZO_ESTIMADO FLOAT NOT NULL
);`

Configuração do Código: No arquivo principal, localize a seção de conexão do banco de dados e insira suas credenciais de usuário e senha do Oracle.

# Python

Exemplo:
`conn = oracledb.connect(user='[SEU_USUARIO]', password='[SUA_SENHA]', dsn='oracle.fiap.com.br:1521/ORCL')`

Execução: Execute o arquivo Python no terminal.

`python seu_arquivo.py`

A aplicação será iniciada e o menu de opções será exibido.
