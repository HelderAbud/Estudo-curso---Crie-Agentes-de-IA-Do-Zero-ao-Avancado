# Lista de Filmes
moviesList = ["Titanic", "The Godfather", "Inception", "Jurassic Park"]

# 1 - Iterando valores de uma lista
for movie in moviesList:
    print(movie)

# 2 - Quando a condição for atendida, o loop será encerrado
for movie in moviesList:
    if movie == "Inception":
        break
    print(movie)
    
# 3 - Quando a condição for atendida, o loop vai para próxima iteração
for movie in moviesList:
    if movie == "Inception":
        continue
    print(movie)
    
# 4 - Avaliação do filme:
movieName = input("Digite o nome do filme:\n")
movieRating = int(input("Digite quantas avaliações deseja fazer:\n"))

total = 0
for i in range(movieRating):
    note = float(input("Digite a nota para o filme:\n"))
    total += note
    
if movieRating > 0:
    average = total / movieRating
else: 
    average = 0
    
print(f"Média de avaliação do filme {movieName} é: {average:.2f}")