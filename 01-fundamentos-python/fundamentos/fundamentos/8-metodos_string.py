movieName = "Top Gun"
movieDescription = """
    Top Gun Maverick, é um filme de aviação e aventura,
muito consagrado na indústria
"""
print(movieName.upper()) # tudo maiúsculo
print(movieName.lower()) # tudo minúsculo
print(movieName.capitalize()) # Primeira Letra maiúscula
print(movieName.title()) # Primeira Letra maiúscula
print(movieName.center(10, '-')) # Retorna string centralizada com caractere de preenchimento
print(movieName.find("u")) # Retorna a posição de um determinado caractere
print(movieName.find("o")) # Conta caracteres
print(movieName.replace("Top", "Matrix")) # ALtera elemento por outro
print(movieDescription.split(','))