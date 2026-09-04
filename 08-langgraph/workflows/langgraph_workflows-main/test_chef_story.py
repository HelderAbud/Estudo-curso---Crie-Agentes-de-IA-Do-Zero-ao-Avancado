from chef_story import chef_workflow

def test_chef_story():
    # Executando o workflow
    result = chef_workflow.invoke({})
    
    # Imprimindo a história completa
    print("\n=== HISTÓRIA DO CHEF ===\n")
    
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
    print(f"Chef: {result['chef']}")
    print(f"Prato: {result['dish']}")
    print(f"Ingrediente Especial: {result['ingredient']}")
    print(f"Desafio: {result['challenge']}")

if __name__ == "__main__":
    test_chef_story() 