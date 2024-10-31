from typing import TypedDict
import datetime
from typing import Literal

Usuario = TypedDict(
    "Usuario",
    {"nome": str, "cpf": int, "data_de_nascimento": datetime.date, "endereço": str},
)

Conta = TypedDict(
    "Conta",
    {"agencia": Literal["0001"], "numero_da_conta": int, "usuario": Usuario},
)


def achar_cpf(usuarios: list[Usuario], cpf: int) -> Literal[False] | int:
    """
    Verifica se o CPF já existe.
    Args:
        usuarios (list[Usuario]): Lista de usuários.
        cpf (int): CPF à ser procurado.

    Returns:
        bool | int: Se for achado, retorna a índice do usuário, caso não for achado retorna False.
    """
    for idx, u in enumerate(usuarios):
        if u["cpf"] == cpf:
            return idx
    return False


def receber_cpf(usuarios: list[Usuario]) -> int:
    cpf: int = int(input("Digite o CPF:\n"))
    if achar_cpf(usuarios, cpf) != False:
        print("Já existe uma conta com esse CPF.")
        receber_cpf(usuarios)
    return cpf


def novo_usuario(usuarios: list[Usuario]) -> None:
    cpf: int = receber_cpf(usuarios)
    res = achar_cpf(usuarios, cpf)
    nome: str = input("Digite o nome: \n")
    while True:
        try:
            data: str = input(
                "Digite a data de nascimento (Formato Ano-Mes-Dia (2000-10-20))\n"
            )
            data_de_nascimento: datetime.date = datetime.datetime.strptime(
                data, "%Y-%m-%d"
            )
        except ValueError:
            print("Data de nascimento está no formato incorreto.")
        else:
            break

    endereco: str = input(
        "Digite o endereço (logradouro, bairro - cidade/sigla estado): \n"
    )

    usuarios.append(
        {
            "cpf": cpf,
            "data_de_nascimento": data_de_nascimento,
            "endereço": f"{endereco}",
            "nome": nome,
        }
    )
    print("Usuário foi criado!")


def nova_conta(
    agencia: Literal["0001"], numero_conta: int, usuarios: list[Usuario]
) -> Conta | None:
    cpf: int = int(input("Digite o CPF:\n"))
    usuario: Literal[False] | int = achar_cpf(usuarios, cpf)

    print(usuarios, cpf, cpf == 30)

    if usuario != False:
        print("Conta foi criada!")
        usu: Usuario = usuarios[usuario]
        return {"agencia": agencia, "numero_da_conta": numero_conta, "usuario": usu}

    print("Conta não foi criada.")
    return


def sacar(
    *,
    valor: float,
    saldo: float,
    extrato: str,
    limite: int,
    numero_saques: int,
    limite_saques: int,
) -> tuple[float, str]:

    excedeu_saldo = valor > saldo

    excedeu_limite = valor > limite

    excedeu_saques = numero_saques >= limite_saques

    if excedeu_saldo:
        print("Operação falhou! Você não tem saldo suficiente.")
    elif excedeu_limite:
        print("Operação falhou! O valor do saque excede o limite.")

    elif excedeu_saques:
        print("Operação falhou! Número máximo de saques excedido.")

    elif valor > 0:
        saldo -= valor
        extrato += f"Saque: R$ {valor:.2f}\n"
        numero_saques += 1

    else:
        print("Operação falhou! O valor informado é inválido.")
    return saldo, extrato


def depositar(saldo: float, valor: float, extrato: str, /) -> tuple[float, str]:

    if valor > 0:
        saldo += valor
        extrato += f"Depósito: R$ {valor:.2f}\n"

    else:
        print("Operação falhou! O valor informado é inválido.")
    return saldo, extrato


def vizualizar_histórico(saldo: float, /, *, extrato: str) -> None:
    print("\n================ EXTRATO ================")
    print("Não foram realizadas movimentações." if not extrato else extrato)
    print(f"\nSaldo: R$ {saldo:.2f}")
    print("==========================================")


def listar_contas(contas: list[Conta]):
    for conta in contas:
        print(conta)


def main():

    menu = """

    [d] Depositar
    [s] Sacar
    [e] Extrato
    [q] Sair
    [nc] Criar conta
    [nu] Criar usuário
    [ls] Listar contas
    => """

    saldo: float = 0
    limite: int = 500
    extrato: str = ""
    numero_saques: int = 0

    LIMITE_SAQUES: int = 3
    AGENCIA: Literal["0001"] = "0001"

    usuarios: list[Usuario] = []
    contas: list[Conta] = []

    while True:

        opcao = input(menu)

        if opcao == "d":
            valor = float(input("Informe o valor do depósito: "))
            saldo, extrato = depositar(saldo, valor, extrato)

        elif opcao == "s":
            valor = float(input("Informe o valor do saque: "))
            saldo, extrato = sacar(
                valor=valor,
                saldo=saldo,
                extrato=extrato,
                limite=limite,
                numero_saques=numero_saques,
                limite_saques=LIMITE_SAQUES,
            )

        elif opcao == "e":
            vizualizar_histórico(saldo, extrato=extrato)
        elif opcao == "nc":
            numero_conta = len(contas) - 1

            conta = nova_conta(AGENCIA, numero_conta, usuarios)
            if conta:
                contas.append(conta)

        elif opcao == "nu":
            novo_usuario(usuarios)
        elif opcao == "ls":
            listar_contas(contas)
        elif opcao == "q":
            break

        else:
            print(
                "Operação inválida, por favor selecione novamente a operação desejada."
            )


main()
