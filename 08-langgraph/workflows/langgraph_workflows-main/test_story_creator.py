import pytest
from story_creator import story_workflow, StoryState

def test_story_workflow():
    # Estado inicial
    initial_state = {
        "prompt": "Uma história sobre um cientista que descobre uma forma de viajar no tempo, mas algo dá errado.",
        "story": "",
        "feedback": "",
        "act": 1
    }
    
    # Simulando feedback do usuário
    def mock_interrupt(state):
        return {"Feedback": "aprovado"}
    
    # Executando o workflow
    result = story_workflow.invoke(
        initial_state,
        config={"interrupt": mock_interrupt}
    )
    
    # Verificações básicas
    assert "story" in result
    assert len(result["story"]) > 0
    assert result["act"] == 4  # Deve ter passado por todos os atos

def test_story_revision():
    # Estado inicial
    initial_state = {
        "prompt": "Uma história sobre um gato que aprende a falar.",
        "story": "Era uma vez um gato chamado Whiskers.",
        "feedback": "",
        "act": 1
    }
    
    # Simulando feedback negativo seguido de positivo
    feedback_count = 0
    def mock_interrupt(state):
        nonlocal feedback_count
        feedback_count += 1
        return {"Feedback": "revisar" if feedback_count == 1 else "aprovado"}
    
    # Executando o workflow
    result = story_workflow.invoke(
        initial_state,
        config={"interrupt": mock_interrupt}
    )
    
    # Verificações
    assert "story" in result
    assert len(result["story"]) > len(initial_state["story"])
    assert feedback_count == 2  # Deve ter recebido feedback duas vezes

if __name__ == "__main__":
    # Exemplo de uso interativo
    initial_state = {
        "prompt": "Uma história sobre um jardim mágico que muda de acordo com as emoções de quem o visita.",
        "story": "",
        "feedback": "",
        "act": 1
    }
    
    def get_user_feedback(state):
        print("\nHistória atual:")
        print(state["story"])
        print(f"\nAto {state['act']}")
        feedback = input("\nDigite 'aprovado' para continuar ou 'revisar' para pedir uma nova versão: ")
        return {"Feedback": feedback}
    
    result = story_workflow.invoke(
        initial_state,
        config={"interrupt": get_user_feedback}
    )
    
    print("\nHistória final:")
    print(result["story"]) 