from __future__ import annotations
import datetime
from typing import TypedDict, Callable
from abc import ABC, abstractmethod

TransacaoTipo = TypedDict("TransacaoTipo", {"tipo": str, "valor": float})


class Transacao(ABC):
    @classmethod
    @abstractmethod
    def registrar(cls, conta: Conta) -> None:
        pass

    @property
    @abstractmethod
    def valor(self) -> float:
        pass


class Deposito(Transacao):
    _valor: float

    def __init__(self, valor: float) -> None:
        self._valor = valor

    @property
    def valor(self) -> float:
        return self._valor

    def registrar(self, conta: Conta) -> None:
        res: bool = conta.depositar(self.valor)

        if res:
            conta.historico.adicionar_transacao(self)


class Historico:
    _transacoes: list[TransacaoTipo] = []

    def adicionar_transacao(self, transacao: Transacao) -> None:
        self._transacoes.append(
            {"tipo": transacao.__class__.__name__, "valor": transacao.valor}
        )

    @property
    def transacoes(self) -> list[TransacaoTipo]:
        return self._transacoes


class Saque(Transacao):
    _valor: float

    def __init__(self, valor: float) -> None:
        self._valor = valor

    @property
    def valor(self) -> float:
        return self._valor

    def registrar(self, conta: Conta) -> None:
        res: bool = conta.sacar(self.valor)

        if res:
            conta.historico.adicionar_transacao(self)


class Cliente:
    endereço: str
    contas: list[Conta] = []

    def __init__(self, endereco: str) -> None:
        self.endereço = endereco

    def realizar_transação(self, conta: Conta, transacao: Transacao) -> None:
        transacao.registrar(conta)

    def adicionar_conta(self, conta: Conta) -> None:
        self.contas.append(conta)


class Conta(Historico):
    _saldo: float = 0
    _numero: int
    _agencia: str = "0001"
    _cliente: PessoaFisica
    _historico: Historico

    def __init__(self, cliente: PessoaFisica, numero: int) -> None:
        self._cliente = cliente
        self._numero = numero
        self._historico = Historico()

    @property
    def saldo(self) -> float:
        return self._saldo

    @property
    def numero(self) -> int:
        return self._numero

    @property
    def agencia(self) -> str:
        return self._agencia

    @property
    def cliente(self) -> PessoaFisica:
        return self._cliente

    @property
    def historico(self) -> Historico:
        return self._historico

    @classmethod
    def nova_conta(cls, cliente: PessoaFisica, numero: int) -> Conta:
        return cls(cliente, numero)

    def sacar(self, valor: float) -> bool:

        saldo = self.saldo

        excedeu_saldo = valor > saldo

        if excedeu_saldo:
            print("Operação falhou! Você não tem saldo suficiente.")
        elif valor > 0:
            self._saldo -= valor
            return True
        else:
            print("Operação falhou! O valor informado é inválido.")
        return False

    def depositar(self, valor: float) -> bool:
        if valor > 0:
            self._saldo += valor
            # extrato += f"Depósito: R$ {valor:.2f}\n"
            return True
        else:
            print("Operação falhou! O valor informado é inválido.")
            return False


class ContaCorrente(Conta):
    limite: float = 500
    limite_saques: int = 3

    def __init__(self, cliente: PessoaFisica, numero: int) -> None:
        super().__init__(cliente, numero)
        self.limite = 500
        self.limite_saques = 3

    def sacar(self, valor: float) -> bool:
        numero_saques: int = 0

        for transacao in self.historico.transacoes:
            if transacao["tipo"] == Saque.__name__:
                numero_saques += 1

        excedeu_limite = valor > self.limite

        excedeu_saques = numero_saques >= self.limite_saques

        if excedeu_limite:
            print("Operação falhou! O valor do saque excede o limite.")

        elif excedeu_saques:
            print("Operação falhou! Número máximo de saques excedido.")
        else:
            return super().sacar(valor)
        return False

    def __str__(self) -> str:
        return f"Agencia: {self.agencia}\nNumero: {self.numero}\nCliente: {self.cliente.nome}"


class PessoaFisica(Cliente):
    nome: str
    data_nascimento: datetime.date
    cpf: str

    def __init__(
        self, nome: str, endereco: str, data_nascimento: datetime.date, cpf: str
    ) -> None:
        super().__init__(endereco)
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf


def achar_contas(cliente: PessoaFisica) -> Conta | None:
    if cliente.contas:
        contaTamanho = len(cliente.contas)
        if contaTamanho < 2:
            return cliente.contas[0]
        else:
            contaIndex: int = int(input(f"Escolha a conta entre 1-{contaTamanho}"))
            return cliente.contas[contaIndex - 1]
    else:
        print("Cliente não tem contas.")
        return None


def pedir_cliente_buffer(
    clientes: list[PessoaFisica], callback: Callable[[PessoaFisica, Conta], None]
) -> None:
    """Pedi e verifica cliente e conta antes de chamar a callback.

    Args:
        clientes (list[PessoaFisica]): Lista de clientes.
        callback (Callable[[PessoaFisica, Conta], None]): Função a ser chamada ao final.
    """
    cpf: str = input("Digite o CPF de um cliente: \n")
    clienteIndex = achar_cpf(clientes, cpf)

    if clienteIndex == None:
        print("Cliente não foi achado.")
        return

    cliente = clientes[clienteIndex]
    conta = achar_contas(cliente)
    if conta == None:
        print("Não achou conta")
        return

    callback(cliente, conta)


def depositar(cliente: PessoaFisica, conta: Conta) -> None:
    valor = float(input("Informe o valor do depósito: "))
    cliente.realizar_transação(conta, Deposito(valor))


def sacar(cliente: PessoaFisica, conta: Conta) -> None:
    valor = float(input("Informe o valor do saque: "))
    cliente.realizar_transação(conta, Saque(valor))


def extrato(cliente: PessoaFisica, conta: Conta) -> None:
    transacoes = conta.historico.transacoes

    print("\n================ EXTRATO ================")
    if not transacoes:
        print("Não foram realizadas movimentações.")
        print(f"\nSaldo: R$ {conta.saldo:.2f}")
    else:
        for t in transacoes:
            print(f'Tipo: {t["tipo"]}\nValor: {t["valor"]}')
            print(f"\nSaldo: R$ {conta.saldo:.2f}")
    print("==========================================")


def achar_cpf(clientes: list[PessoaFisica], cpf: str) -> int | None:
    """
    Verifica se o CPF já existe.
    Args:
        usuarios (list[Usuario]): Lista de usuários.
        cpf (int): CPF à ser procurado.

    Returns:
        int | None: Se for achado, retorna a índice do usuário.
    """
    for idx, c in enumerate(clientes):
        if c.cpf == cpf:
            return idx
    return None


def nova_conta(
    clientes: list[PessoaFisica], contas: list[Conta], numero_conta: int
) -> None:
    cpf: str = input("Digite o CPF de um cliente: \n")
    clienteIndex = achar_cpf(clientes, cpf)

    if clienteIndex == None:
        print("Cliente não foi achado.")
        return

    cliente: PessoaFisica = clientes[clienteIndex]
    conta: Conta = ContaCorrente.nova_conta(cliente, numero_conta)
    contas.append(conta)
    cliente.contas.append(conta)

    print("Conta foi Criada")


def novo_cliente(clientes: list[PessoaFisica]) -> None:
    cpf: str = input("Digite um CPF:\n")
    if achar_cpf(clientes, cpf) != None:
        print("Já existe um cliente com esse CPF.")
        return
    nome: str = input("Digite o nome: \n")

    while True:
        try:
            data: str = input(
                "Digite a data de nascimento (Formato Ano-Mes-Dia (2000-10-20))\n"
            )
            data_nascimento: datetime.date = datetime.datetime.strptime(
                data, "%Y-%m-%d"
            )
        except ValueError:
            print("Data de nascimento está no formato incorreto.")
        else:
            break

    endereco: str = input(
        "Digite o endereço (logradouro, bairro - cidade/sigla estado): \n"
    )

    cliente: PessoaFisica = PessoaFisica(nome, endereco, data_nascimento, cpf)
    clientes.append(cliente)
    print("Cliente foi criado!")


def listar_contas(contas: list[Conta]):
    for conta in contas:
        print(conta)


def main() -> None:

    menu = """

[d] Depositar
[s] Sacar
[e] Extrato
[q] Sair
[nco] Criar conta
[ncl] Criar cliente
[ls] Listar 

=> """

    clientes: list[PessoaFisica] = []
    contas: list[Conta] = []

    while True:

        opcao = input(menu)

        if opcao == "d":
            pedir_cliente_buffer(clientes, depositar)
        elif opcao == "s":
            pedir_cliente_buffer(clientes, sacar)
        elif opcao == "e":
            pedir_cliente_buffer(clientes, extrato)
        elif opcao == "nco":
            nova_conta(clientes, contas, len(contas))
        elif opcao == "ncl":
            novo_cliente(clientes)
        elif opcao == "ls":
            listar_contas(contas)
        elif opcao == "q":
            break

        else:
            print(
                "Operação inválida, por favor selecione novamente a operação desejada."
            )


main()
