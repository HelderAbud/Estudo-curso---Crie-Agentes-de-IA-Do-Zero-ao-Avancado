# Crie Rápido Agentes de IA — Do Zero ao Avançado

Repositório de **estudos e exercícios práticos** do curso *Crie Rápido Agentes de IA Do Zero ao Avançado - AI Agents* (Udemy).

Documenta minha trilha com agentes de IA em Python. **Não substitui o curso pago** nem republica slides, apostilas ou vídeos do instrutor.

## Sobre o curso

Formação para dominar ferramentas de criação de agentes de IA: **CrewAI**, **LangGraph**, **LangChain**, **LlamaIndex** e automação de workflows (inclui **N8N** no currículo do curso).

**O que se aprende**

- Configuração de ambientes para desenvolvimento de agentes
- Criação e execução de agentes multi-tarefas
- Integração de ferramentas e processamento de dados (LangChain, LlamaIndex)
- Automação de workflows (LangGraph; N8N no curso)
- Análise e geração de insights a partir de dados
- Exportação e apresentação de resultados

**Pré-requisitos**

- Python básico
- Noções de IA e modelos de linguagem
- Computador com internet

**Público-alvo:** desenvolvedores, cientistas de dados, entusiastas de IA e especialistas em automação.

## Ferramentas neste repositório

| Ferramenta | Uso no material local |
|------------|------------------------|
| LangChain | Chatbots, chains, RAG, agents |
| LangGraph | Grafos e workflows de agentes |
| LlamaIndex | Indexação e consulta de dados |
| CrewAI | Crews multi-agente |
| Agno | Agentes com tools e reasoning |
| Jupyter / VS Code | Notebooks e scripts Python |

> **N8N:** faz parte do currículo do curso; **não há módulo N8N** neste repositório (low-code / instalação local).

## Estrutura

```text
01-fundamentos-python/     Python básico
02-python-intermediario/   Iteradores, geradores, regex, async
03-engenharia-de-prompt/   Prompting, evals, Anthropic
04-provedores-llm/         OpenAI, Groq, Gemini, Mistral, Cohere
05-langchain-fundamentos/  Models, prompts, chains, memory
06-langchain-rag/          Embeddings, vector store, retrieval
07-langchain-agents/       Tools, agents, LCEL
08-langgraph/              Básico, colaboração, workflows
09-llamaindex/             Indexação, agents, RAG, banco
10-crewai/                 Deploy, PDF, tools, imobiliária
11-agno/                   Agentes Agno
```

## Como rodar

1. Clone o repositório.
2. Crie e ative um venv: `python -m venv .venv`
3. Copie variáveis: `copy .env.example .env` (Windows) ou `cp .env.example .env`
4. Preencha as chaves **somente no `.env` local**.
5. Instale deps do módulo: `pip install -r <pasta>/requirements.txt`
6. Abra o notebook ou script do módulo.

Nunca commite `.env`, `.venv/` ou saídas de notebook com API keys.

## Destaques para portfólio

- `06-langchain-rag` — pipeline RAG
- `08-langgraph/workflows` — padrões de workflow (router, paralelização, HITL)
- `10-crewai/imobiliaria` — crew + recomendação
- `11-agno` — agentes com tools

## Segurança

Secrets via `.env` (no `.gitignore`). Material sensível ou de copyright fica em `_local-nao-publicar/` (também ignorado).

## Autor

Helder Abud — portfólio de estudos (Python / IA aplicada / agentes).
