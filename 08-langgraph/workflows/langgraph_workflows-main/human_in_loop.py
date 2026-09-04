from typing import Annotated, TypedDict
from typing_extensions import TypedDict
from operator import or_
import random

from langgraph.graph import START, END, StateGraph
from langchain_core.messages import HumanMessage, SystemMessage

from models import models

# Estados
class State(TypedDict):
    story: Annotated[dict[str, str], or_]
    human_feedback: str
    needs_revision: bool
    revision_count: int

# Nodes
def generate_story_part(state: State):
    """Gera uma parte da história"""
    
    if "story" not in state:
        state["story"] = {}
    
    msg = f"""Você é um escritor criativo. Escreva uma parte interessante de uma história.
              Se já existir conteúdo anterior, continue a partir dele:
              {state.get('story', {}).get('current_part', '')}
              
              A história deve ser envolvente e ter elementos de fantasia.
              Limite a resposta a 2-3 parágrafos."""
    
    messages = [
        SystemMessage(content="Você é um escritor criativo especializado em histórias de fantasia."),
        HumanMessage(content=msg)
    ]
    
    response = models["deepseek_r1"].invoke(messages)
    
    return {
        "story": {"current_part": response.content},
        "needs_revision": False,
        "revision_count": 0
    }

def get_human_feedback(state: State):
    """Solicita feedback do humano"""
    
    print("\n=== PARTE ATUAL DA HISTÓRIA ===")
    print(state["story"]["current_part"])
    print("\n=== FEEDBACK SOLICITADO ===")
    print("Por favor, avalie esta parte da história:")
    print("1. Aprovar e continuar")
    print("2. Solicitar revisão")
    print("3. Fazer sugestão específica")
    
    choice = input("\nSua escolha (1-3): ")
    
    if choice == "1":
        return {
            "human_feedback": "approved",
            "needs_revision": False
        }
    elif choice == "2":
        return {
            "human_feedback": "needs_revision",
            "needs_revision": True
        }
    else:
        suggestion = input("\nDigite sua sugestão: ")
        return {
            "human_feedback": suggestion,
            "needs_revision": True
        }

def revise_story(state: State):
    """Revisa a história com base no feedback"""
    
    msg = f"""Você é um escritor criativo. Revise a seguinte parte da história com base no feedback:
              História atual:
              {state['story']['current_part']}
              
              Feedback recebido:
              {state['human_feedback']}
              
              Por favor, revise a história mantendo o contexto geral, mas incorporando o feedback.
              Limite a resposta a 2-3 parágrafos."""
    
    messages = [
        SystemMessage(content="Você é um escritor criativo especializado em revisão de histórias."),
        HumanMessage(content=msg)
    ]
    
    response = models["deepseek_r1"].invoke(messages)
    
    return {
        "story": {"current_part": response.content},
        "needs_revision": False,
        "revision_count": state.get("revision_count", 0) + 1
    }

def should_continue(state: State):
    """Decide se deve continuar ou terminar"""
    if state.get("revision_count", 0) >= 3:
        return "end"
    return "continue"

# Construindo o workflow
workflow = StateGraph(State)

# Adicionando nós
workflow.add_node("generate", generate_story_part)
workflow.add_node("feedback", get_human_feedback)
workflow.add_node("revise", revise_story)

# Adicionando arestas
workflow.add_edge(START, "generate")
workflow.add_edge("generate", "feedback")
workflow.add_edge("feedback", "revise", condition=lambda x: x["needs_revision"])
workflow.add_edge("revise", "feedback")
workflow.add_edge("feedback", END, condition=lambda x: not x["needs_revision"])

# Compilando o workflow
story_human_workflow = workflow.compile()

# Função para executar o workflow
def run_story_workflow():
    """Executa o workflow de geração de história com feedback humano"""
    result = story_human_workflow.invoke({})
    print("\n=== HISTÓRIA FINAL ===")
    print(result["story"]["current_part"])
    print(f"\nNúmero de revisões: {result.get('revision_count', 0)}")

if __name__ == "__main__":
    run_story_workflow() 