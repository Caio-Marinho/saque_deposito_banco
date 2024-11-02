from configuration.connection_mysql import Connection


class Cliente:
    def __init__(self, nome: str, telefone: str, cidade: str):
        self.__nome = nome
        self.__telefone = telefone
        self.__cidade = cidade
        self.criar_tabela()
        self.inserir_dados()

    @property
    def nome(self):
        return self.__nome

    @nome.setter
    def nome(self, nome: str):
        if not nome:
            raise ValueError("O nome não pode ser vazio")
        with Connection() as conn:
            if conn.cursor():
                cursor = conn.cursor()
                cursor.execute("USE banco;")
                cursor.execute(f"UPDATE clientes SET nome='{nome}' WHERE nome = '{self.__nome}';")
                cursor.execute(f"SELECT nome FROM clientes WHERE nome='{nome}';")
                self.__nome = cursor.fetchall()[0][0]

    @property
    def telefone(self):
        return self.__telefone

    @telefone.setter
    def telefone(self, telefone: str):
        if len(str(telefone)) != 11 or not telefone.isdigit():
            raise ValueError("O telefone deve conter 11 dígitos numéricos.")
        with Connection() as conn:
            if conn.cursor():
                cursor = conn.cursor()
                cursor.execute("USE banco;")
                cursor.execute(f"UPDATE clientes SET telefone='{telefone}' WHERE telefone = '{self.__telefone}';")
                cursor.execute(f"SELECT telefone FROM clientes WHERE telefone='{telefone}';")
                self.__telefone = cursor.fetchall()[0][0]  # Telefone atualizado somente se válido

    @property
    def cidade(self):
        return self.__cidade

    @cidade.setter
    def cidade(self, cidade: str):
        if not cidade:
            raise ValueError("A cidade deve ser uma string não vazia.")
        with Connection() as conn:
            if conn.cursor():
                cursor = conn.cursor()
                cursor.execute("USE banco;")
                cursor.execute(f"UPDATE clientes SET cidade='{cidade}' WHERE cidade = '{self.__cidade}';")
                cursor.execute(f"SELECT cidade FROM clientes WHERE cidade='{cidade}';")
                self.__cidade = cursor.fetchall()[0][0]

    @staticmethod
    def criar_tabela():
        with Connection() as conn:
            if conn.cursor():
                cursor = conn.cursor()
                cursor.execute("CREATE DATABASE IF NOT EXISTS banco;")
                cursor.execute("USE banco;")
                cursor.execute("CREATE TABLE IF NOT EXISTS clientes(ID INT PRIMARY KEY AUTO_INCREMENT,"
                               "nome VARCHAR(255) NOT NULL,"
                               "telefone CHAR(11) NOT NULL,"
                               "cidade VARCHAR(255) NOT NULL);")

    def inserir_dados(self):
        with Connection() as conn:
            if conn.cursor():
                cursor = conn.cursor()
                cursor.execute("USE banco;")
                cursor.execute(f"SELECT * FROM clientes WHERE nome='{self.__nome}' AND telefone='{self.__telefone}' "
                               f"AND cidade='{self.__cidade}';")
                if len(cursor.fetchall()) > 0:
                    raise ValueError("O cliente com este dados já existe.")
                cursor.execute("INSERT INTO clientes(nome,telefone,cidade) VALUES"
                               f"('{self.__nome}','{self.__telefone}','{self.__cidade}');")

    def consultar(self):
        with Connection() as conn:
            if conn.cursor():
                cursor = conn.cursor()
                cursor.execute("USE banco;")
                cursor.execute(f"SELECT * FROM clientes WHERE nome='{self.__nome}' AND telefone='{self.__telefone}' "
                               f"AND cidade='{self.__cidade}';")
                return cursor.fetchall()
