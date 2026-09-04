# Projeto de Workflows com LangGraph

Este projeto serve como um repositório de diversos padrões de workflows construídos com LangGraph. O objetivo é fornecer uma base de exemplos (cookbook) que podem ser adaptados e utilizados em soluções futuras.

## Estrutura do Projeto

A ideia é que cada arquivo Python principal na raiz do projeto represente um workflow ou um padrão de workflow específico.

## Soluções Implementadas

### 1. Paralelização e Julgamento (`parallelization.py`)

Este workflow demonstra como executar duas chamadas a Modelos de Linguagem (LLMs) de forma paralela e, em seguida, utilizar um terceiro LLM para julgar qual das respostas é a melhor. Esta abordagem de usar um LLM para avaliar a saída de outros LLMs é conhecida como a técnica "LLM as a Judge".

Esse workflow pode ser adaptado para que diferentes LLMs resolvam um pedaço de um problema geral e o agregador junte as peças.

Esse é um padrão poderoso e pode ser usado em muitas soluções.

**Funcionamento:**

1.  O workflow recebe uma query (pergunta/instrução) do usuário.
2.  A query é enviada simultaneamente para dois LLMs diferentes:
    *   `gemini_2.5_flash`
    *   `deepseek_v3`
3.  Ambos os LLMs são instruídos (via System Message) a atuar como cozinheiros especialistas, gerando receitas saudáveis com base nos ingredientes fornecidos pelo usuário.
4.  As respostas de ambos os LLMs são então enviadas para um terceiro LLM (`gpt_4o`).
5.  Este terceiro LLM atua como um juiz, avaliando as duas receitas geradas e determinando qual delas é a melhor, considerando critérios como utilidade, relevância, precisão, etc.
6.  O resultado final é a avaliação do juiz.

**Arquivos Relevantes:**

*   `parallelization.py`: Contém a definição do grafo e a lógica do workflow de paralelização e julgamento.
*   `models.py`: Responsável por carregar e configurar os diferentes LLMs utilizados no projeto (OpenAI, Google Gemini, DeepSeek). Ele lê as chaves de API de variáveis de ambiente (arquivo `.env`) e instancia os modelos com configurações específicas.

## Requisitos

*   Python 3.10 ou superior.

## Como Executar

1.  **Instale as dependências:**

    Antes de executar o projeto, certifique-se de instalar todas as bibliotecas necessárias. Execute o seguinte comando no seu terminal, na raiz do projeto:

    ```bash
    pip install -r requirements.txt
    ```

2.  **Execute o ambiente de desenvolvimento LangGraph:**

    Para executar os workflows e interagir com a API do LangGraph localmente, utilize o seguinte comando no terminal, na raiz do projeto:

    ```bash
    langgraph dev
    ```

Certifique-se de ter um arquivo `.env` com as chaves