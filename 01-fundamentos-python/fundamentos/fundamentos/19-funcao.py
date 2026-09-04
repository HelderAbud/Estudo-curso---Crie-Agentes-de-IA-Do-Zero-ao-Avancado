# 1 - Função para imprimir uma mensagem
def welcome():
    print("Bem vindo ao sistema de filmes!")
    
# for i in range(10):
#     welcome()
# 2 - Função para calcular a média de notas
def calculate_average():
    num_ratings = int(input("Digite quantas avaliações deseja fazer pro filme:\n"))
    total = 0 
    for i in range(num_ratings):
        note = float(input("Digite a nota para o filme:\n"))
        total += note
    
    if num_ratings > 0:
        average = total / num_ratings
    else:
        average = 0
        
    return average

print(f"A média de avaliações é: {calculate_average():.2f}")

# 3 - Função para cadastrar um filme:
def create_movie():
    name = input("Digite o nome do filme:\n")
    yearLaunch = int(input("Digite o ano de lançamento do filme:\n"))
    moviePrice = float(input("Digite o preço do filme:\n"))
    rating = float(input("Digite a nota do filme:\n"))
    print(f"{name} ({yearLaunch}) - R$ {moviePrice:.2f}")
    
create_movie()
create_movie()
