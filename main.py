from cliente import Cliente
from conta import Conta

cliente = Cliente('caio', '81979056770', 'Recife')

conta = Conta(cliente.nome, '001', cliente.consultar()[0][0])

print(conta.saque(2000))
