from parallelization2 import code_analysis_workflow

# Código de exemplo para análise
codigo_teste = """
def calcular_media(lista):
    soma = 0
    for i in range(len(lista)):
        soma = soma + lista[i]
    media = soma / len(lista)
    return media

# Testando a função
numeros = [1, 2, 3, 4, 5]
resultado = calcular_media(numeros)
print(f"A média é: {resultado}")
"""

# Executando o workflow
resultado = code_analysis_workflow.invoke({
    "query": codigo_teste
})

# Exibindo os resultados
print("\n=== Análise do Gemini ===")
print(resultado["llm1"])
print("\n=== Análise do O4 ===")
print(resultado["llm2"])
print("\n=== Avaliação Final ===")
print(resultado["best_llm"]) 