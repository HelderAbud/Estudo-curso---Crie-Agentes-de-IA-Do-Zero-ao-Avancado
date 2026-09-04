from detective_story import detective_workflow

def test_detective_story():
    # Executando o workflow
    result = detective_workflow.invoke({})
    
    # Imprimindo a história completa
    print("\n=== HISTÓRIA DO DETETIVE ===\n")
    
    print("=== PRIMEIRO ATO ===")
    print(result["story"]["act_1"])
    print("\n=== SEGUNDO ATO ===")
    print(result["story"]["act_2"])
    print("\n=== TERCEIRO ATO ===")
    print(result["story"]["act_3"])
    print("\n=== QUARTO ATO ===")
    print(result["story"]["act_4"])
    
    # Imprimindo os elementos da história
    print("\n=== ELEMENTOS DA HISTÓRIA ===")
    print(f"Detetive: {result['detective']}")
    print(f"Crime/Mistério: {result['crime']}")
    print(f"Local: {result['location']}")
    print(f"Pista Inicial: {result['clue']}")

if __name__ == "__main__":
    test_detective_story() 