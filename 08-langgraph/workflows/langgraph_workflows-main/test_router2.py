from router2 import workflow

def test_workflow():
    # Teste com consulta técnica
    resultado_tecnico = workflow.invoke({
        "query": "Como posso aprender Python?",
        "categoria": "",
        "answer": ""
    })
    print("\n=== Consulta Técnica ===")
    print(f"Pergunta: Como posso aprender Python?")
    print(f"Resposta: {resultado_tecnico['answer']}")

    # Teste com consulta de saúde
    resultado_saude = workflow.invoke({
        "query": "Quais são os benefícios de uma alimentação saudável?",
        "categoria": "",
        "answer": ""
    })
    print("\n=== Consulta de Saúde ===")
    print(f"Pergunta: Quais são os benefícios de uma 
          alimentação saudável?")
    print(f"Resposta: {resultado_saude['answer']}")

    # Teste com consulta geral
    resultado_geral = workflow.invoke({
        "query": "Qual é a capital do Brasil?",
        "categoria": "",
        "answer": ""
    })
    print("\n=== Consulta Geral ===")
    print(f"Pergunta: Qual é a capital do Brasil?")
    print(f"Resposta: {resultado_geral['answer']}")

if __name__ == "__main__":
    test_workflow() 