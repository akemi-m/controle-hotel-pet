# Controle Hotel Pet

## Descrição do Projeto

O "Controle Hotel Pet" é um sistema desenvolvido para gerenciar as atividades de um hotel para pets, incluindo cadastro, edição, consulta, listagem e hospedagem de animais.

Este projeto tem como objetivo proporcionar uma interface amigável e funcional para o gerenciamento eficiente de informações relacionadas aos pets e seus tutores.

## Funcionalidades

- **Adicionar Pet**: Registra um novo pet no sistema.
- **Editar Pet**: Permite alterar informações de um pet cadastrado.
- **Consultar Pet**: Exibe os dados de um pet específico.
- **Listar Pets**: Mostra todos os pets cadastrados.
- **Excluir Pet**: Remove um pet do sistema.
- **Entrada no Hotel Pet**: Registra a entrada de um pet no hotel para hospedagem.
- **Saída do Hotel Pet**: Finaliza a hospedagem e calcula o custo total.
- **Listagem do Hotel Pet**: Exibe os pets atualmente hospedados e o histórico de hospedagens.
- **Consultar Preços**: Mostra os preços de hospedagem por porte do pet.

## Detalhes de Configuração

Para configurar o projeto, siga as instruções abaixo:

### Instalação de Dependências

1. Instale o SQLAlchemy:

```bash
python -m pip install SQLAlchemy
```

2. Instale o driver MySQL-Connector:

```bash
python -m pip install mysql-connector-python
```

### Configuração do Banco de Dados

1. Crie o banco de dados utilizando o arquivo `script.sql` fornecido com o projeto. Ele contém as instruções para criar o banco de dados e a tabela necessária para o funcionamento do sistema.

2. No arquivo `util.py`, substitua a linha 10 com os dados do seu MySQL:

```python
engine = create_engine('mysql+mysqlconnector://<user>:<password>@<host>[:<port>]/<dbname>')
```

## Estrutura do Projeto

O projeto está organizado nos seguintes módulos:

- **`app.py`**: Arquivo principal para execução do sistema.
- **`util.py`**: Funções principais para gerenciar pets e hospedagens.
- **`tipo.py`**: Enumeração para tipos de pets.
- **`resposta.py`**: Enumeração para respostas de confirmação.
- **`porte.py`**: Enumeração para portes dos pets.
- **`pets.py`**: Classe que representa um pet e suas propriedades.
- **`hospedado.py`**: Enumeração para status de hospedagem.

## Executando o Projeto

1. Certifique-se de que todas as dependências estão instaladas e o banco de dados está configurado.
2. Execute o comando:

```bash
python py/app.py
```

3. Siga as instruções do menu para interagir com o sistema.
