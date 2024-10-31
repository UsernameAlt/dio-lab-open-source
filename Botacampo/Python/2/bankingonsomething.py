opções = """

"d" - Deposito
"s" - Sacar
"e" - Extrair
"q" - Sair

"""

saldo: float = 0
MAX_SAQUE: int = 500
extrato: str = ""
quantidade_saques: int = 0
MAX_QUANTIDADE_SAQUES: int = 3

while True:
    commando: str = input(f"{opções}")

    if commando == "s":
        val: float = float(input("Valor a sacar: "))

        maior_que_saldo: bool = val > saldo
        maior_que_max: bool = val > MAX_SAQUE
        mais_que_limite: bool = quantidade_saques > MAX_QUANTIDADE_SAQUES

        if maior_que_saldo:
            print(
                f"\nTentou sacar mais do que tem no saldo.\nSaldo: {saldo:.2f}\nTentou remover: R$ {val:.2f}\n"
            )
        elif maior_que_max:
            print(f"Valor deve ser menor que {MAX_SAQUE}")
        elif mais_que_limite:
            print(f"Limite de {MAX_QUANTIDADE_SAQUES} saques já foi alcançado.")
        elif val > 0:

            saldo -= val
            quantidade_saques += 1

            print(
                f"R$ {val:.2f} foram Sacados. {quantidade_saques} de {MAX_QUANTIDADE_SAQUES} diários"
            )

            extrato += f"Sacou R$ {val:.2f}\n"

        else:
            print("Valor invalido.")

    elif commando == "d":
        if quantidade_saques < MAX_QUANTIDADE_SAQUES:
            val = float(input("Valor a depositar: "))
            if val > 0:
                saldo += val
                print(f"Depositado: R$ {val:.2f}")
                extrato += f"Depositado R$ {val:.2f}\n"
            else:
                print("Valor invalido")
        else:
            print("Limite de quantidade de saques alcançado.")

    elif commando == "e":
        print(f"Nenhuma operação foi realizada." if not extrato else extrato)
        print(f"Saldo: R$ {saldo:.2f}\n")

    elif commando == "q":
        print("Saindo")
        break
    else:
        print(
            f'Comando "{commando if not len(commando) > 15 else commando[:15] + '...'}" é Invalido. '
        )
