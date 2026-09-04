from agno.agent import Agent
from agno.tools.youtube import YouTubeTools

agent = Agent(
    tools=[YouTubeTools()],
    show_tool_calls=True,
    description="""
    Você é um agente do Youtube. Obtenha as legendas de um
    vídeo do Youtube e responda às perguntas.
    """
)

agent.print_response("Sumarize esse vídeo: https://www.youtube.com/watch?v=AHqqzUkjRjw", markdown=True)
    
