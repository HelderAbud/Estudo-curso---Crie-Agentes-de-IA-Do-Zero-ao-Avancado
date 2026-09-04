### Essa versão implementa a versão síncrona do workflow
import os
import random
from typing_extensions import TypedDict

from langgraph.graph import START, END, StateGraph
from langgraph.prebuilt import tools_condition
from langgraph.prebuilt import ToolNode
from langchain_core.messages import SystemMessage, HumanMessage
from langgraph.graph import MessagesState

from models import models



def matrix_quote() -> str:
    """Retorna uma frase do filme Matrix.

    Args:
        Não há argumentos.
    """
    frases = [
        "Neo, sooner or later you're going to realize just as I did that there's a difference between knowing the path and walking the path.",
        "What are you trying to tell me? That I can dodge bullets?",
        "There is no spoon.",
    ]
    return random.choice(frases)

tools = [matrix_quote]
llm = models["gpt_4_1"]

llm_with_tools = llm.bind_tools(tools, parallel_tool_calls=False)

# System message
sys_msg = SystemMessage(content="""Você é um assistente de IA que responde perguntas sobre o filmes. 
                        Quando perguntado sobre o filme Matrix, você deve responder com uma frase usando a ferramenta matrix_quote.""")

# Nós
def assistant(state: MessagesState):
   return {"messages": [llm_with_tools.invoke([sys_msg] + state["messages"])]}


# Grafo
builder = StateGraph(MessagesState)

# Define nós: estes realizam o trabalho
builder.add_node("assistant", assistant)
builder.add_node("tools", ToolNode(tools))

# Define arestas: estas determinam como o fluxo de controle se move
builder.add_edge(START, "assistant")
builder.add_conditional_edges(
    "assistant",
    # Se a última mensagem (resultado) do assistente é uma chamada de ferramenta -> tools_condition roteia para ferramentas
    # Se a última mensagem (resultado) do assistente não é uma chamada de ferramenta -> tools_condition roteia para END
    tools_condition,
)
builder.add_edge("tools", "assistant")
builder.add_edge("assistant", END)
agent = builder.compile()