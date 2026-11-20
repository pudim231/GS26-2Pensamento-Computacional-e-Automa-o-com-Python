from base_conhecimento import BaseConhecimento
from assistente import Assistente


def solicitar_nota_facilidade() -> int:
    """Solicita uma nota de 1 a 5 ao sair, tratando entradas inválidas."""
    while True:
        entrada = input("\nAntes de sair, avalie a facilidade de uso do assistente (1 a 5): ").strip()
        if entrada.isdigit() and 1 <= int(entrada) <= 5:
            return int(entrada)
        print("Nota inválida. Digite um número inteiro entre 1 e 5.")


def main() -> None:
    base = BaseConhecimento("data/base_conhecimento.json")
    carregou = base.carregar()

    if not carregou:
        print("Aviso: o programa continuará em execução, mas sem orientações carregadas.")

    assistente = Assistente("Citizen Assist AI", base)

    while True:
        print("\n" + "=" * 65)
        print(f"  {assistente.nome} - Orientação ao Jovem e Estudante")
        print("  Aviso: este assistente NÃO é um canal oficial.")
        print("=" * 65)
        print("1. Fazer uma pergunta (busca inteligente)")
        print("2. Navegar por categorias")
        print("3. Ver indicadores de atendimento")
        print("4. Exportar atendimentos para CSV")
        print("0. Sair")

        opcao = input("\nEscolha uma opção: ").strip()

        if opcao == "1":
            assistente.perguntar()
        elif opcao == "2":
            assistente.navegar()
        elif opcao == "3":
            assistente.indicadores()
        elif opcao == "4":
            assistente.exportar_csv()
        elif opcao == "0":
            nota = solicitar_nota_facilidade()
            assistente.indicadores(nota_facilidade=nota)
            assistente.exportar_csv()
            print("\nObrigado por utilizar o Citizen Assist AI. Até logo!")
            break
        else:
            print("Opção inválida. Digite 1, 2, 3, 4 ou 0.")


if __name__ == "__main__":
    main()