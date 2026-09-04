import sqlite3
from datetime import datetime, timedelta
import random

# Conectar ao banco de dados
conexao = sqlite3.connect('escola.db')
cursor = conexao.cursor()

# Funções para gerar dados
def gerar_data_admissao():
    dias_atras = random.randint(365, 365 * 10)
    return (datetime.now() - timedelta(days=dias_atras)).strftime('%Y-%m-%d')

def gerar_nota():
    return round(random.uniform(5.0, 10.0), 1)

estados = ['SP', 'RJ', 'MG', 'RS', 'BA']
cidades = ['São Paulo', 'Rio de Janeiro', 'Belo Horizonte', 'Porto Alegre', 'Salvador']

# Inserir dados na tabela Alunos
alunos = [
    (i, f'Aluno {i}', f'aluno{i}@email.com', f'Rua {i}, {i*10}', random.choice(estados), gerar_nota())
    for i in range(1, 21)
]
cursor.executemany('''
    INSERT INTO Alunos (ID_Aluno, Nome, Email, Rua_Numero, Estado, Nota_Final)
    VALUES (?, ?, ?, ?, ?, ?)
''', alunos)

# Inserir dados na tabela Professores
professores = [
    (
        i,
        f'Professor {i}',
        random.choice(['Matemática', 'História', 'Física', 'Português', 'Química']),
        gerar_data_admissao(),
        f'1199999{i:04}',
        f'prof{i}@escola.com',
        f'Rua {i}',
        f'Bairro {i}',
        random.choice(cidades)
    )
    for i in range(1, 21)
]
cursor.executemany('''
    INSERT INTO Professores (ID_Professor, Nome, Especialidade, Data_Admissao, Telefone, Email, Rua, Bairro, Cidade)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
''', professores)

# Inserir dados na tabela Disciplinas
disciplinas = [
    (
        i,
        f'Disciplina {i}',
        f'Descrição da Disciplina {i}',
        random.choice([30, 45, 60, 90]),
        random.randint(1, 20)  # ID_Professor
    )
    for i in range(1, 21)
]
cursor.executemany('''
    INSERT INTO Disciplinas (ID_Disciplina, Nome, Descricao, Carga_Horaria, ID_Professor)
    VALUES (?, ?, ?, ?, ?)
''', disciplinas)

# Commit e fechamento
conexao.commit()
conexao.close()

print("20 registros inseridos em cada tabela com sucesso.")
