import os
from typing_extensions import TypedDict

from langgraph.graph import START, END, StateGraph
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_deepseek import ChatDeepSeek

from models import models
from dotenv import load_dotenv

load_dotenv()

# Obtém as chaves de API das variáveis de ambiente
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")

# Configuração dos modelos com as chaves de API
models = {
    "gemini_2.5_flash": ChatGoogleGenerativeAI(
        model="gemini-2.5-flash-preview-04-17",
        google_api_key=GOOGLE_API_KEY,
        temperature=1.0
    ),
    "o4": ChatOpenAI(
        model="o4-mini-2025-04-16",
        openai_api_key=OPENAI_API_KEY
    ),
    "gpt_4o": ChatOpenAI(
        model="gpt-4o-2024-08-06",
        openai_api_key=OPENAI_API_KEY
    )
}

# --- System Messages ---
SYSTEM_MESSAGE_LLMS = SystemMessage(content="""
    Você é um cozinheiro especialista, gerando receitas saudáveis para usuários com base nos ingredientes deles.
    Você receberá uma lista de ingredientes e precisará gerar uma receita com base neles,
    juntamente com ingredientes básicos adicionais comumente encontrados em casa 
    (como temperos, manteiga, óleo, alho, etc.).
    A receita deve ser uma lista de etapas, juntamente com uma lista de ingredientes 
    necessários para cada etapa.""")


# Estados(Importante)
class State(TypedDict):
    query: str
    llm1: str
    llm2: str
    best_llm: str


# Nodes
def call_llm_1(state: State):
    """Recebe a query do usuário e retorna a resposta do modelo gemini_2.5_flash"""

    messages = [
        SystemMessage(
            content=SYSTEM_MESSAGE_LLMS.content
        ),
        HumanMessage(
            content=state["query"]
        )
    ]
    response = models["gemini_2.5_flash"].invoke(messages)
   
    return {"llm1": response.content}


def call_llm_2(state: State):
    """Recebe a query do usuário e retorna a resposta do modelo o4"""
    messages = [
        SystemMessage(
            content=SYSTEM_MESSAGE_LLMS.content
        ),
        HumanMessage(
            content=state["query"]
        )
    ]
    response = models["o4"].invoke(messages)
   
    return {"llm2": response.content}


def judge(state: State):
    """Recebe as respostas dos modelos e retorna a melhor resposta. Usa uma técnica chamada LLMS as a judge"""
    
    msg = f"""Aja como um juiz imparcial e avalie a qualidade das respostas fornecidas por dois assistentes de
            assistentes de IA à pergunta do usuário exibida abaixo. 

            Você deve escolher o assistente que
            segue as instruções do usuário e responde melhor à pergunta do usuário. Sua avaliação
            deve considerar fatores como a utilidade, a relevância, a precisão, a profundidade, a criatividade
            e o nível de detalhes de suas respostas. Comece sua avaliação comparando as duas
            respostas e forneça uma breve explicação. Evite qualquer preconceito de posição e certifique-se de que a ordem em que as respostas foram
            ordem em que as respostas foram apresentadas não influencie sua decisão. Não permita que
            Não permita que a extensão das respostas influencie sua avaliação. Não dê preferência a determinados nomes de
            assistentes. Seja o mais objetivo possível. Depois de fornecer sua explicação, dê seu
            veredicto final seguindo rigorosamente este formato: "[[A]]" se o assistente A for melhor, "[[B]]"
            se o assistente B for melhor, e "[[C]]" em caso de empate.

            [Pergunta do usuário]
            {state["query"]}

            [Início da resposta do assistente A]
            {state["llm1"]}
            [Fim da resposta do assistente A]

            [Início da resposta do assistente B]
            {state["llm2"]}
            [Fim da resposta do assistente B]
            """
    
    messages = [
        SystemMessage(
            content=msg
        )
    ]
    response = models["gpt_4o"].invoke(messages)
   
    return {"best_llm": response.content}


# Construindo o workflow
parallel_builder = StateGraph(State)

# Adicionando nós
parallel_builder.add_node("call_llm_1", call_llm_1)
parallel_builder.add_node("call_llm_2", call_llm_2)
parallel_builder.add_node("judge", judge)

# Adicionando arestas
parallel_builder.add_edge(START, "call_llm_1")
parallel_builder.add_edge(START, "call_llm_2")
parallel_builder.add_edge("call_llm_1", "judge")
parallel_builder.add_edge("call_llm_2", "judge")
parallel_builder.add_edge("judge", END)

# Compilando o workflow
parallel_workflow = parallel_builder.compile()
