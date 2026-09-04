import sqlite3

# Criação da conexão com o banco de dados
conexao = sqlite3.connect('escola.db')
cursor = conexao.cursor()

# Criação da tabela Alunos
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Alunos (
        ID_Aluno INTEGER PRIMARY KEY,
        Nome TEXT NOT NULL,
        Email TEXT,
        Rua_Numero TEXT,
        Estado TEXT,
        Nota_Final REAL
    )
''')

# Criação da tabela Professores
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Professores (
        ID_Professor INTEGER PRIMARY KEY,
        Nome TEXT NOT NULL,
        Especialidade TEXT,
        Data_Admissao TEXT,
        Telefone TEXT,
        Email TEXT,
        Rua TEXT,
        Bairro TEXT,
        Cidade TEXT
    )
''')

# Criação da tabela Disciplinas
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Disciplinas (
        ID_Disciplina INTEGER PRIMARY KEY,
        Nome TEXT NOT NULL,
        Descricao TEXT,
        Carga_Horaria INTEGER,
        ID_Professor INTEGER,
        FOREIGN KEY (ID_Professor) REFERENCES 
        Professores(ID_Professor)
    )
''')

# Commit e fechamento da conexão
conexao.commit()
conexao.close()

print("Banco de dados e tabelas criados com sucesso.")
