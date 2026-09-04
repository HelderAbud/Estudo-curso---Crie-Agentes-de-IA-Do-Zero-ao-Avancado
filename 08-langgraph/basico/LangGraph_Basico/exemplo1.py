from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from langgraph.graph import StateGraph
from pydantic import BaseModel
from dotenv import load_dotenv
import os

# 1- Carrega API Key
load_dotenv()
API_KEY = os.getenv("API_KEY")

# 2- Definição do modelo
llm_model = ChatOpenAI(model="gpt-3.5-turbo", api_key=API_KEY)

# 3 - Definição do StateGraph
class GraphState(BaseModel):
    input: str
    output: str
    
# 4 - Função de resposta
def responder(state):
    input_message = state.input
    response = llm_model.invoke([HumanMessage(content=input_message)])
    return GraphState(input=state.input, 
                      output=response.content
                     )
# 5 - Criando o Graph
graph = StateGraph(GraphState)
graph.add_node("responder", responder)
graph.set_entry_point("responder")
graph.set_finish_point("responder")

# 6 - Compilando o Grafo
export_graph = graph.compile()

# 7 - Testando o Agente
if __name__ == "__main__":
    result = export_graph.invoke(GraphState(input="Quem descobriu a América", output=""))
    print(result)
    
    # Visualizar o grafo
    print(export_graph.get_graph().draw_mermaid())