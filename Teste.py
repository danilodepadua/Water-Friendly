import sqlite3

def IniciarBanco():
    con = sqlite3.connect('banco.db')
    cursor = con.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS Usuarios (Login TEXT PRIMARY KEY, Nome TEXT, Sobrenome TEXT, Senha TEXT)")
    cursor.execute("CREATE TABLE IF NOT EXISTS Plantacoes (Id Integer PRIMARY KEY, User TEXT, Planta Text, Tamanho INTEGER, FOREIGN KEY(User) REFERENCES Usuarios(Login))")
    con.close()
def AdicionarUsuario(login, nome, sobrenome, senha):
    con = sqlite3.connect('banco.db')
    cursor = con.cursor()
    try:
        cursor.execute("INSERT INTO Usuarios VALUES(?,?,?,?)", (login, nome, sobrenome, senha))
        con.commit()
    except:
        print("Erro ao adicionar usuario")
    con.close()
def AdicionarPlantacao(user, planta, tamanho):
    con = sqlite3.connect('banco.db')
    cursor = con.cursor()
    cursor.execute("PRAGMA foreign_keys = ON")
    try:
        cursor.execute(f"INSERT INTO Plantacoes(User, Planta, Tamanho) VALUES('{user}', '{planta}', '{tamanho}')")
        con.commit()
    except:
        print("Erro ao adicionar plantacao")
    con.close()
def DeletarUsuario(Login):
    con = sqlite3.connect('banco.db')
    cursor = con.cursor()
    try:
        cursor.execute(f"DELETE FROM Plantacoes WHERE User = '{Login}'")
        cursor.execute(f"DELETE FROM Usuarios WHERE Login = '{Login}'")
        con.commit()
    except:
        print("Erro ao deletar usuario")
    con.close()
def DeletarPlantacao(id):
    con = sqlite3.connect('banco.db')
    cursor = con.cursor()
    try:
        cursor.execute(f"DELETE FROM Plantacoes WHERE Id = '{id}'")
        con.commit()
    except:
        print("Erro ao deletar plantacao")
    con.close()
def AtualizarPlantacao(id, planta, tamanho):
    con = sqlite3.connect('banco.db')
    cursor = con.cursor()
    try:
        cursor.execute(f"UPDATE Plantacoes SET Planta = '{planta}', Tamanho = '{tamanho}' WHERE Id = '{id}'")
        con.commit()
    except:
        print("Erro ao atualizar plantacao")
    con.close()
def ListarPlantacoes(User):
    con = sqlite3.connect('banco.db')
    cursor = con.cursor()
    try:
        cursor.execute(f"SELECT * FROM Plantacoes WHERE User = '{User}'")
        for linha in cursor.fetchall():
            print(linha)
    except:
        print("Erro ao listar plantacoes")
    con.close()