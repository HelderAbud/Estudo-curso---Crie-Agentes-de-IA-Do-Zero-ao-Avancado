from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from langgraph.prebuilt import create_react_agent
from dotenv import load_dotenv
import os
from langchain_mcp_adapters.client import MultiServerMCPClient

# 1- Carrega API Key
load_dotenv()
API_KEY = os.getenv("API_KEY")

# 2- Definição do modelo
model = ChatOpenAI(model="o4-mini-2025-04-16", api_key=API_KEY)

# 3 - Define o prompt do sistema
system_message = SystemMessage(content="""
Você é um assistente especializado em fornecer informações
sobre comunidades de Python para GenAI.

Ferramentas disponíveis no MCP Server:

1. get_communit(location: str) -> str
- Função: retorna a melhor comunidade de Python para GenAI.
- Parâmetro: location (string)
- Retorno: "Code TI" 

Seu papel é ser um intermediário direto entre o usuários e 
a ferramenta MCP, retornando apenas o resultado final das ferramentas.
"""
)

def agent_mcp():
    client = MultiServerMCPClient(
        {
            "code":{
                "command": "python",
                "args": ["mcp_server.py"],
                "transport": "stdio"
            }
        }
    )
    agent = create_react_agent(model, client.get_tools(), prompt=system_message)
    return agent
