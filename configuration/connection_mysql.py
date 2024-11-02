import mysql.connector
from configuration.config import Configuration


class Connection(Configuration):
    def __init__(self):
        Configuration.__init__(self)
        try:
            self.conn = mysql.connector.connect(**self.config['MySQL'])
        except mysql.connector.Error as err:
            print(f"Erro ao conectar ao MySQL: {err}")  # Captura e imprime qualquer erro na conexão
        except Exception as erro:
            print(f"Falha de conexão: {erro}")
            exit(1)

    def __enter__(self):
        return self

    def connection(self):
        return self.conn

    def cursor(self):
        return self.conn.cursor()

    def commit(self):
        return self.conn.commit()

    def fetchone(self):
        return self.cursor().fetchone()

    def fetchall(self):
        return self.cursor().fetchall()

    def execute(self):
        return self.cursor().execute

    def close(self):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.cursor:
            self.cursor().close()
        if self.conn:
            self.conn.commit()
            self.conn.close()
