### Essa versão implementa o padrão de workflow chain.
### Criando história de ficção em 4 atos.
from typing import Annotated
from typing_extensions import TypedDict
from operator import add

from langgraph.graph import START, END, StateGraph
from langchain_core.messages import HumanMessage
from langgraph.types import interrupt, Command
from typing import Literal

from models import models
import logging




# Estados(Importante)
class State(TypedDict):
    email: str
    response: str
    feedback: str

# Nodes

def generate_response(state: State):
    """Escreve o email"""
    
    feedback = state.get("feedback", "")
    response = state.get("response", "")
    
    

              
    
    msg = f"""Você é um assistente responsável por responder emails de clientes.
              Você trabalha para o Ronnald Hawk da Simplework.ai
              Ronnald pode atender apenas às terças feiras entre as 10h e as 12h.
            
            **Instruções:**
            
            Baseado no email abaixo, responda de forma educada e profissional.  
            
            Só exiba o email final, sem explicação.
            
            **Instruções:**
            
            Baseado no email abaixo, responda de forma educada e profissional.  
            
            Email:
            {state["email"]}
            
            Caso a existam feedbacks anteriores, lembre-se deles.
            
            Feedbacks anteriores:
            {feedback}
            
            Também leve em consideração o esboço anterior, caso exista.
            
            Esboço anterior:
            {response}
            
            
            
            """
    
    messages = [
    HumanMessage(
        content=msg
    )
    ]
    response = models["gemini-2.0-flash"].invoke(messages)
   
    return {"response": response.content}

def evaluate_response(state: State):
    """Pede feedback sobre o email"""
    feedback = interrupt( 
        {
            "email": state["email"],
            "response": state["response"]
        }
    )
    logging.info(feedback)
    return {"feedback": feedback}

def route_email(state: State):
    """Roteia para o próximo nó"""
    f = state.get("feedback")
    if f['Feedback'] == 'aprovado':
        return True
    else:
        return False
    
def final_response(state: State):
    """Finaliza o workflow"""
    return {"response": state["response"]}
   




# Construindo o workflow
builder = StateGraph(State)

# Adicionando nós
builder.add_node("generate_response", generate_response)
builder.add_node("evaluate_response", evaluate_response)
builder.add_node("final_response", final_response)

builder.add_edge(START, "generate_response")
builder.add_edge("generate_response", "evaluate_response")
builder.add_conditional_edges("evaluate_response",
                              route_email,
                              {
                                  False: "generate_response", 
                                  True: "final_response"
                              })
builder.add_edge("final_response", END)




# Compilando o workflow
optimizer_workflow = builder.compile()