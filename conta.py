from configuration.connection_mysql import Connection


class Conta:
    def __init__(self, titular: str, numero: str, id_cliente: int):
        self.__titular = titular
        self.__numero = numero
        self.criar_tabela()
        self.__saldo = 2500.00
        self.inserir_dados(id_cliente)

    @property
    def saldo(self):
        return self.__saldo

    @saldo.setter
    def saldo(self, saldo: float):
        if saldo < 0:
            raise ValueError("O saldo não pode ficar negativo")
        self.__saldo = saldo

    def saque(self, valor) -> str | ValueError:
        if valor > 0:
            with Connection() as conn:
                if conn.cursor():
                    cursor = conn.cursor()
                    cursor.execute("USE banco;")
                    cursor.execute(f"UPDATE conta SET saldo = {self.saldo - valor};")
            self.saldo -= valor
            return f"Saque de {valor} realizado. Saldo atual: {self.__saldo}"
        else:
            raise ValueError("Informe um valor válido")

    def deposito(self, valor) -> str | ValueError:
        if valor >= 0:
            with Connection() as conn:
                if conn.cursor():
                    cursor = conn.cursor()
                    cursor.execute("USE banco;")
                    cursor.execute(f"UPDATE conta SET saldo = {self.saldo + valor};")
            self.saldo += valor
            return "Depósito de " + str(valor) + " realizado. Saldo atual: " + str(self.__saldo)
        else:
            raise ValueError("Informe um valor válido")

    def extrato(self):
        print("Nome Do Cliente:", self.__titular, "\nSaldo Atual Da Conta:%.2f" % self.saldo)

    @staticmethod
    def criar_tabela():
        with Connection() as conn:
            if conn.cursor():
                cursor = conn.cursor()
                cursor.execute("USE banco;")
                cursor.execute("CREATE TABLE IF NOT EXISTS conta("
                               "ID INT PRIMARY KEY AUTO_INCREMENT,"
                               "nome VARCHAR(255) NOT NULL,"
                               "Numero_conta VARCHAR(255) NOT NULL,"
                               "Saldo DECIMAL(10,2) NOT NULL,"
                               "ID_CLIENTE INT NOT NULL, FOREIGN KEY (ID_CLIENTE) REFERENCES clientes(ID));")

    def inserir_dados(self, id_cliente: int):
        with Connection() as conn:
            if conn.cursor():
                cursor = conn.cursor()
                cursor.execute("USE banco;")
                cursor.execute(f"SELECT * FROM conta WHERE nome='{self.__titular}' AND Numero_conta='{self.__numero}' "
                               f" AND ID_CLIENTE={id_cliente};")
                if len(cursor.fetchall()) > 0:
                    raise ValueError("A conta com este dados já existe.")
                cursor.execute("INSERT INTO conta(nome,numero_conta,saldo,id_cliente)"
                               f"VALUES ('{self.__titular}','{self.__numero}',{self.__saldo},{id_cliente});")
