### Essa versão implementa o padrão de workflow chain.
### Criando história de ficção em 4 atos.
from typing import Annotated
from typing_extensions import TypedDict
from operator import or_
import random

from langgraph.graph import START, END, StateGraph
from langchain_core.messages import HumanMessage

from models import models




# Estados(Importante)
class State(TypedDict):
    character: str
    action: str
    place: str
    complement: str
    story: Annotated[dict[str, str], or_]

# Nodes

def act_one(state: State):
    """Escreve o Ato 1"""
    
    character = random.choice(["Um mágico e seu coelho da cartola", "Um detetive", "uma professora e uma aluna"])
    action = random.choice(["Perder-se", "Ganhar na loteria", "Escutar barulho estranho no meio da noite"])
    place = random.choice(["Um elevador muito apertado", "Uma pastelaria", "Um estádio de futebol"])
    complement = random.choice(["Uma planta ressecada", "Pode gritar à vontade. Não há ninguém por perto", "Remédios para dormir"])
    
    msg = f"""Você é um roteirista experiente encarregado de escrever o Ato 1 de uma nova história de ficção.

            **Instruções:**

            Baseado nas seguintes informações iniciais:
            *   **Personagem:** {character}
            *   **Ação Inicial Desejada/Circunstância:** {action}
            *   **Lugar Inicial:** {place}
            *   **Complemento Relevante:** {complement}

            Escreva o **Ato 1** desta história. Este ato deve:
            1.  **Apresentar o Protagonista:** Mostre quem é o `[Personagem]` em seu mundo (`[Lugar]`). Revele um pouco de sua personalidade, seus desejos, e talvez uma falha ou algo que o incomoda em sua vida cotidiana.
            2.  **Estabelecer o Status Quo:** Descreva a vida normal do protagonista antes que o conflito principal comece.
            3.  **Introduzir o Incidente Incitante:** Um evento (relacionado à `[Ação]` e/ou `[Complemento]`) que perturba o status quo do protagonista e dá início ao conflito principal da história. Este evento deve ser claro e impactante.
            4.  **Terminar com o Primeiro Ponto de Virada (Quebra para o Ato Dois):** O protagonista deve tomar uma decisão crucial ou ser forçado a uma situação que o comprometa com a jornada ou o conflito principal. Ele não pode mais voltar à sua vida normal como era antes. Este é o momento em que ele cruza um limiar.

            O Ato 1 deve ter entre 1 e 2 parágrafos.
            Ao final, sinalize claramente:
            --- FIM DO ATO 1 ---
            --- PRIMEIRO PONTO DE VIRADA: [Descreva brevemente o ponto de virada] --
            """
    
    messages = [
    HumanMessage(
        content=msg
    )
    ]
    response = models["deepseek_r1"].invoke(messages)
   
    return {"story": {"act_1": response.content}, 
            "character": character, 
            "action": action, 
            "place": place, 
            "complement": complement}

def act_two(state: State):
    """Escreve o Ato 2"""
    
    msg = f"""Você é um roteirista experiente continuando uma história de ficção.
              Abaixo está o Ato 1 da história:
             --- INÍCIO DO ATO 1 (CONTEXTO) ---
             {state["story"]["act_1"]}
            --- FIM DO ATO 1 (CONTEXTO) ---

            **Instruções:**

            Agora, escreva o **Ato 2 (Parte 1)** desta história, continuando diretamente de onde o Ato 1 parou. Este ato deve:
            1.  **Reação ao Primeiro Ponto de Virada:** Mostrar o protagonista lidando com as consequências imediatas da decisão ou evento do Primeiro Ponto de Virada.
            2.  **Novos Desafios e Obstáculos:** O protagonista começa a enfrentar os primeiros obstáculos em sua jornada para alcançar seu objetivo ou resolver o conflito introduzido. Esses desafios devem testá-lo.
            3.  **Aprendizado e Adaptação:** O protagonista pode aprender novas habilidades, cometer erros, encontrar aliados e/ou inimigos.
            4.  **Aumento Gradual da Tensão:** As apostas começam a subir. O protagonista pode ter alguns sucessos iniciais, mas os desafios se tornam mais complexos.
            5.  **Terminar com o Ponto Médio (Midpoint):** O Ato 2 (Parte 1) deve culminar em um evento significativo no meio da história. Este "Ponto Médio" pode ser:
                *   Uma falsa vitória (o protagonista acha que está no caminho certo, mas algo maior está por vir).
                *   Uma falsa derrota (parece que tudo está perdido, mas uma nova percepção surge).
                *   Uma grande revelação que muda a perspectiva do protagonista ou a natureza do conflito.
                *   Um momento em que o protagonista passa de reativo para proativo em relação ao conflito.
                Este Ponto Médio deve elevar as apostas drasticamente e mudar a dinâmica da história.

            O Ato 2 (Parte 1) deve ter entre 1 e 2 parágrafos.
            Ao final, sinalize claramente:
            --- FIM DO ATO 2 (PARTE 1) ---
            --- PONTO MÉDIO (MIDPOINT): [Descreva brevemente o Ponto Médio] ---
            """
    
    messages = [
    HumanMessage(
        content=msg
    )
    ]
    response = models["deepseek_r1"].invoke(messages)
   
    return {"story": {"act_2": response.content}}

def act_three(state: State):
    """Escreve o Ato 3"""
    
    msg = f"""Você é um roteirista experiente continuando uma história de ficção.
            Abaixo estão o Ato 1 e o Ato 2 (Parte 1) da história:
            --- INÍCIO DO CONTEXTO PREEXISTENTE ---
            {state["story"]["act_1"]}

            {state["story"]["act_2"]}
            --- FIM DO CONTEXTO PREEXISTENTE ---

            **Instruções:**

            Agora, escreva o **Ato 3 (ou Ato 2 - Parte 2, aprofundando a Confrontação)** desta história, continuando diretamente de onde o Ato 2 (Parte 1) parou, após o Ponto Médio. Este ato deve:
            1.  **Consequências do Ponto Médio:** O protagonista lida com as ramificações do Ponto Médio. Se foi uma vitória, as coisas podem se complicar inesperadamente. Se foi uma derrota, ele precisa se reerguer.
            2.  **Intensificação do Conflito ("Bad Guys Close In"):** Os obstáculos se tornam mais difíceis e perigosos. As forças antagonistas (sejam elas pessoas, circunstâncias ou internas) ganham força e pressionam o protagonista.
            3.  **"Tudo Parece Perdido" (All is Lost) / "Noite Escura da Alma":** O protagonista enfrenta seu maior revés até agora. Pode ser uma perda significativa, um fracasso esmagador, ou um momento de profunda crise pessoal onde ele questiona sua jornada, suas habilidades ou seus valores. A esperança parece mínima.
            4.  **Terminar com o Segundo Ponto de Virada (Quebra para o Ato Quatro):** Após a crise ("Noite Escura da Alma"), o protagonista encontra uma nova chave, uma nova determinação, uma epifania, ou um último fragmento de esperança. Ele descobre algo (interno ou externo) que o capacita ou o direciona para o confronto final. Este é o momento que o impulsiona para o Clímax.

            O Ato 3 deve ter entre 1 e 2 parágrafos.
            Ao final, sinalize claramente:
            --- FIM DO ATO 3 ---
            --- SEGUNDO PONTO DE VIRADA: [Descreva brevemente o Segundo Ponto de Virada] ---
            """
    
    messages = [
    HumanMessage(
        content=msg
    )
    ]
    response = models["deepseek_r1"].invoke(messages)
   
    return {"story": {"act_3": response.content}}

def act_four(state: State):
    """Escreve o Ato 4"""
    
    msg = f"""Você é um roteirista experiente finalizando uma história de ficção.
    Abaixo estão os Atos 1, 2 (Parte 1) e 3 da história:
    --- INÍCIO DO CONTEXTO PREEXISTENTE ---
    {state["story"]["act_1"]}

    {state["story"]["act_2"]}

    {state["story"]["act_3"]}
    --- FIM DO CONTEXTO PREEXISTENTE ---

    **Instruções:**

    Agora, escreva o **Ato 4 (Resolução)** desta história, continuando diretamente de onde o Ato 3 parou, após o Segundo Ponto de Virada. Este ato deve:
    1.  **Rumo ao Clímax:** O protagonista, energizado ou com um novo plano/entendimento do Segundo Ponto de Virada, avança para o confronto final. A tensão deve ser máxima.
    2.  **Clímax:** Este é o confronto final e decisivo entre o protagonista e a principal força antagonista. É o momento de maior tensão da história, onde o conflito central é enfrentado diretamente. O protagonista deve usar tudo o que aprendeu em sua jornada. O resultado do clímax deve resolver a questão principal da história.
    3.  **Resolução (Denouement):**
        *   **Consequências Imediatas:** Mostre o resultado direto do clímax. Quem venceu, quem perdeu, o que mudou.
        *   **Novo Normal:** Descreva brevemente a nova situação do protagonista e de seu mundo após o conflito.
    *   **Arco do Personagem Concluído:** Mostre como o protagonista mudou como resultado de sua jornada. Ele alcançou seu desejo inicial? Ele superou sua falha?
    *   **Sensação de Conclusão:** A história deve terminar de forma satisfatória, amarrando as pontas soltas mais importantes.

    O Ato 4 deve ter entre 1 e 2 parágrafos.
    Separe claramente o Clímax da Resolução.
    Ao final, sinalize claramente:
    --- FIM DO ATO 4: CLÍMAX ---
    [Texto do Clímax]
    --- FIM DO ATO 4: RESOLUÇÃO ---
    [Texto da Resolução]
    --- FIM DA HISTÓRIA ---
    """
    
    messages = [
    HumanMessage(
        content=msg
    )
    ]
    response = models["deepseek_r1"].invoke(messages)
   
    return {"story": {"act_4": response.content}}







# Construindo o workflow
chain_builder = StateGraph(State)

# Adicionando nós
chain_builder.add_node("act_one", act_one)
chain_builder.add_node("act_two", act_two)
chain_builder.add_node("act_three", act_three)
chain_builder.add_node("act_four", act_four)

# Adicionando arestas
chain_builder.add_edge(START, "act_one")
chain_builder.add_edge("act_one", "act_two")
chain_builder.add_edge("act_two", "act_three")
chain_builder.add_edge("act_three", "act_four")
chain_builder.add_edge("act_four", END)

# Compilando o workflow
chain_workflow = chain_builder.compile()