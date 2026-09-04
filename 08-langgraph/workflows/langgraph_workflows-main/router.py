### Essa versão implementa a versão síncrona do workflow
import os
from typing_extensions import TypedDict

from langgraph.graph import START, END, StateGraph
from langchain_core.messages import SystemMessage, HumanMessage

from models import models


# --- System Messages ---
SYSTEM_MESSAGE_LLMS = SystemMessage(content="""Você é assistente de IA solicito""")

# Estados(Importante)
class State(TypedDict):
    query: str
    router_state: bool
    answer: str


# Nodes
def router(state: State):
    
    
    if "obrigado" in state["query"]:
        return {"router_state": True}
    else:
        return {"router_state": False}
   


def llm(state: State):
    """Recebe a query do usuário e retorna a resposta do modelo gpt_4o"""
    messages = [
    SystemMessage(
        content=SYSTEM_MESSAGE_LLMS.content
    ),
    HumanMessage(
        content=state["query"]
    )
]
    response = models["gpt_4o"].invoke(messages)
   
    return {"answer": response.content}
    


def direct_answer(state: State):
    """Recebe a query do usuário e retorna a resposta do modelo gemini_2.5_flash"""
    return {"answer": "de nada"}

# Construindo o workflow
routing_builder = StateGraph(State)

# Adicionando nós
routing_builder.add_node("router", router)
routing_builder.add_node("llm", llm)
routing_builder.add_node("direct_answer", direct_answer)

routing_builder.set_entry_point("router")
#adicionando nó de decisão binária
routing_builder.add_conditional_edges("router",lambda state: state["router_state"], {True: "direct_answer", False: "llm"})#adicionando nó de decisão binária
routing_builder.add_edge("llm", END)
routing_builder.add_edge("direct_answer", END)


# Compilando o workflow
routing_workflow = routing_builder.compile()