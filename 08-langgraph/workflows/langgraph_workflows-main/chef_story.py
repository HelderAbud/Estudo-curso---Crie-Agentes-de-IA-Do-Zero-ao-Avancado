from typing import Annotated
from typing_extensions import TypedDict
from operator import or_
import random

from langgraph.graph import START, END, StateGraph
from langchain_core.messages import HumanMessage

from models import models

# Estados
class State(TypedDict):
    chef: str
    dish: str
    ingredient: str
    challenge: str
    story: Annotated[dict[str, str], or_]

# Nodes
def first_act(state: State):
    """Escreve o Primeiro Ato"""
    
    chef = random.choice([
        "Um chef italiano apaixonado por massas",
        "Uma chef francesa especialista em sobremesas",
        "Um chef brasileiro que ama comida de boteco"
    ])
    dish = random.choice([
        "Um risoto de frutos do mar",
        "Uma torta de maçã tradicional",
        "Um feijão tropeiro especial"
    ])
    ingredient = random.choice([
        "Um tempero secreto da família",
        "Um vinho raro de 50 anos",
        "Um queijo artesanal único"
    ])
    challenge = random.choice([
        "O forno quebrou no meio do preparo",
        "Um crítico gastronômico famoso chegou inesperadamente",
        "Faltou um ingrediente essencial"
    ])
    
    msg = f"""Você é um escritor culinário experiente encarregado de escrever o Primeiro Ato de uma história sobre um chef.

            **Instruções:**

            Baseado nas seguintes informações iniciais:
            *   **Chef:** {chef}
            *   **Prato:** {dish}
            *   **Ingrediente Especial:** {ingredient}
            *   **Desafio:** {challenge}

            Escreva o **Primeiro Ato** desta história. Este ato deve:
            1.  **Apresentar o Chef:** Mostre quem é o chef e sua paixão pela culinária.
            2.  **Estabelecer o Contexto:** Descreva o restaurante e a situação normal antes do desafio.
            3.  **Introduzir o Desafio:** O momento em que o chef descobre que terá que lidar com {challenge}.
            4.  **Terminar com o Primeiro Ponto de Virada:** O chef toma a decisão de enfrentar o desafio.

            O Primeiro Ato deve ter entre 1 e 2 parágrafos.
            Ao final, sinalize claramente:
            --- FIM DO PRIMEIRO ATO ---
            --- PRIMEIRO PONTO DE VIRADA: [Descreva brevemente o ponto de virada] ---
            """
    
    messages = [HumanMessage(content=msg)]
    response = models["deepseek_r1"].invoke(messages)
   
    return {
        "story": {"act_1": response.content},
        "chef": chef,
        "dish": dish,
        "ingredient": ingredient,
        "challenge": challenge
    }

def second_act(state: State):
    """Escreve o Segundo Ato"""
    
    msg = f"""Você é um escritor culinário continuando uma história sobre um chef.
              Abaixo está o Primeiro Ato da história:
             --- INÍCIO DO PRIMEIRO ATO ---
             {state["story"]["act_1"]}
            --- FIM DO PRIMEIRO ATO ---

            **Instruções:**

            Agora, escreva o **Segundo Ato** desta história, continuando diretamente de onde o Primeiro Ato parou. Este ato deve:
            1.  **Reação ao Desafio:** Mostrar como o chef começa a lidar com o problema.
            2.  **Tentativas Iniciais:** As primeiras tentativas de resolver a situação.
            3.  **Complicações:** Como as coisas começam a ficar mais difíceis.
            4.  **Ponto Médio:** Um momento de revelação ou mudança de estratégia.

            O Segundo Ato deve ter entre 1 e 2 parágrafos.
            Ao final, sinalize claramente:
            --- FIM DO SEGUNDO ATO ---
            --- PONTO MÉDIO: [Descreva brevemente o ponto médio] ---
            """
    
    messages = [HumanMessage(content=msg)]
    response = models["deepseek_r1"].invoke(messages)
   
    return {"story": {"act_2": response.content}}

def third_act(state: State):
    """Escreve o Terceiro Ato"""
    
    msg = f"""Você é um escritor culinário continuando uma história sobre um chef.
            Abaixo estão o Primeiro e Segundo Atos da história:
            --- INÍCIO DO CONTEXTO PREEXISTENTE ---
            {state["story"]["act_1"]}

            {state["story"]["act_2"]}
            --- FIM DO CONTEXTO PREEXISTENTE ---

            **Instruções:**

            Agora, escreva o **Terceiro Ato** desta história, continuando diretamente de onde o Segundo Ato parou. Este ato deve:
            1.  **Crise:** O momento mais difícil para o chef.
            2.  **Revelação:** Uma descoberta ou ideia que pode mudar tudo.
            3.  **Decisão Final:** A escolha que levará ao clímax.

            O Terceiro Ato deve ter entre 1 e 2 parágrafos.
            Ao final, sinalize claramente:
            --- FIM DO TERCEIRO ATO ---
            --- SEGUNDO PONTO DE VIRADA: [Descreva brevemente o segundo ponto de virada] ---
            """
    
    messages = [HumanMessage(content=msg)]
    response = models["deepseek_r1"].invoke(messages)
   
    return {"story": {"act_3": response.content}}

def fourth_act(state: State):
    """Escreve o Quarto Ato"""
    
    msg = f"""Você é um escritor culinário finalizando uma história sobre um chef.
    Abaixo estão os três primeiros atos da história:
    --- INÍCIO DO CONTEXTO PREEXISTENTE ---
    {state["story"]["act_1"]}

    {state["story"]["act_2"]}

    {state["story"]["act_3"]}
    --- FIM DO CONTEXTO PREEXISTENTE ---

    **Instruções:**

    Agora, escreva o **Quarto Ato (Resolução)** desta história, continuando diretamente de onde o Terceiro Ato parou. Este ato deve:
    1.  **Clímax:** O momento final onde o chef apresenta sua solução.
    2.  **Resultado:** Como o prato foi recebido e o que aconteceu.
    3.  **Conclusão:** O que o chef aprendeu com toda essa experiência.

    O Quarto Ato deve ter entre 1 e 2 parágrafos.
    Ao final, sinalize claramente:
    --- FIM DO QUARTO ATO: CLÍMAX ---
    [Texto do Clímax]
    --- FIM DO QUARTO ATO: RESOLUÇÃO ---
    [Texto da Resolução]
    --- FIM DA HISTÓRIA ---
    """
    
    messages = [HumanMessage(content=msg)]
    response = models["deepseek_r1"].invoke(messages)
   
    return {"story": {"act_4": response.content}}

# Construindo o workflow
chef_builder = StateGraph(State)

# Adicionando nós
chef_builder.add_node("first_act", first_act)
chef_builder.add_node("second_act", second_act)
chef_builder.add_node("third_act", third_act)
chef_builder.add_node("fourth_act", fourth_act)

# Adicionando arestas
chef_builder.add_edge(START, "first_act")
chef_builder.add_edge("first_act", "second_act")
chef_builder.add_edge("second_act", "third_act")
chef_builder.add_edge("third_act", "fourth_act")
chef_builder.add_edge("fourth_act", END)

# Compilando o workflow
chef_workflow = chef_builder.compile() 