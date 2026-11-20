import csv
import json
import os
import time
from datetime import datetime
from base_conhecimento import BaseConhecimento
from orientacao import Orientacao


class Assistente:
    """Controla a interação com o cidadão, histórico, indicadores e exportação CSV."""

    def __init__(
        self,
        nome: str,
        base: BaseConhecimento,
        caminho_historico: str = "data/historico.json",
        caminho_csv: str = "data/atendimentos.csv",
    ):
        self.nome = nome
        self.base = base
        self.caminho_historico = caminho_historico
        self.caminho_csv = caminho_csv
        self.historico: list[dict] = self._carregar_historico()

    def _carregar_historico(self) -> list[dict]:
        """Carrega o histórico existente de forma segura, sem falhar se ausente/corrompido."""
        if not os.path.exists(self.caminho_historico):
            return []
        try:
            with open(self.caminho_historico, "r", encoding="utf-8") as arquivo:
                dados = json.load(arquivo)
                return dados if isinstance(dados, list) else []
        except (json.JSONDecodeError, OSError):
            print("[AVISO] Histórico anterior corrompido ou ilegível. Iniciando histórico limpo.")
            return []

    def _salvar_historico(self) -> None:
        """Persiste a lista de atendimentos no arquivo data/historico.json."""
        pasta = os.path.dirname(self.caminho_historico)
        if pasta:
            os.makedirs(pasta, exist_ok=True)
        with open(self.caminho_historico, "w", encoding="utf-8") as arquivo:
            json.dump(self.historico, arquivo, ensure_ascii=False, indent=2)

    @staticmethod
    def contem_dado_pessoal(texto: str) -> bool:
        """
        Verifica se o texto contém '@' (e-mail) ou 8 ou mais dígitos
        numéricos (CPF, RG, telefone, etc.).
        """
        if "@" in texto:
            return True
        qtd_digitos = sum(1 for c in texto if c.isdigit())
        return qtd_digitos >= 8

    @staticmethod
    def classificar_confianca(pontos: int) -> str:
        """Classifica o nível de confiança com base na pontuação obtida."""
        if pontos >= 6:
            return "ALTA"
        if pontos >= 3:
            return "MÉDIA"
        return "BAIXA"

    @staticmethod
    def _perguntar_sim_nao(mensagem: str) -> bool:
        """Lê apenas 's' ou 'n' sem encerrar o programa em entradas inválidas."""
        while True:
            resp = input(mensagem).strip().lower()
            if resp == "s":
                return True
            if resp == "n":
                return False
            print("Entrada inválida. Digite apenas 's' para sim ou 'n' para não.")

    def registrar(
        self,
        origem: str,
        pergunta: str,
        orientacao_id: int | None,
        encontrou: bool,
        ajudou: bool,
        tentativas: int,
        tempo_segundos: float,
    ) -> None:
        """Registra um atendimento no histórico em memória e salva no JSON."""
        registro = {
            "data": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "origem": origem,
            "pergunta": pergunta,
            "id_orientacao": orientacao_id,
            "encontrou": encontrou,
            "ajudou": ajudou,
            "tentativas": tentativas,
            "tempo_segundos": tempo_segundos,
        }
        self.historico.append(registro)
        self._salvar_historico()

    def perguntar(self) -> None:
        """Executa o fluxo de atendimento por pergunta em texto livre."""
        if not self.base.orientacoes:
            print("\nBase de conhecimento vazia. Não é possível responder perguntas agora.")
            return

        tentativas = 0
        inicio = time.time()

        while True:
            pergunta = input("\nDigite sua dúvida (0 para voltar): ").strip()

            if pergunta == "0":
                return

            if not pergunta:
                print("Entrada vazia. Por favor, digite sua dúvida ou 0 para voltar.")
                continue

            if self.contem_dado_pessoal(pergunta):
                print("Atenção: não digite CPF, telefone ou e-mail. Reescreva.")
                continue

            tentativas += 1
            resultados = self.base.buscar(pergunta)

            # Melhor orientação precisa ter pelo menos 3 pontos
            if not resultados or resultados[0][0] < 3:
                print("\nNão encontrei uma orientação com confiança suficiente para essa dúvida.")
                print("Dica: tente usar palavras-chave mais diretas (ex: 'cpf', 'ctps', 'titulo de eleitor', 'cadunico', 'cartao sus').")
                print(f"Categorias disponíveis: {', '.join(self.base.categorias())}")

                if self._perguntar_sim_nao("Deseja reformular a pergunta agora? (s/n): "):
                    continue

                tempo_total = round(time.time() - inicio, 1)
                self.registrar(
                    origem="pergunta",
                    pergunta=pergunta,
                    orientacao_id=None,
                    encontrou=False,
                    ajudou=False,
                    tentativas=tentativas,
                    tempo_segundos=tempo_total,
                )
                return

            melhor_pontos, melhor_orientacao = resultados[0]
            nivel_confianca = self.classificar_confianca(melhor_pontos)

            print(f"\nConfiança da resposta: {nivel_confianca} ({melhor_pontos} pontos)")
            melhor_orientacao.exibir()

            # Exibe até duas alternativas caso também tenham atingido pontuação mínima
            alternativas = [item for item in resultados[1:3] if item[0] >= 3]
            if alternativas:
                print("\nOutras orientações relacionadas:")
                for pts_alt, ori_alt in alternativas:
                    print(f"  * [{ori_alt.id}] {ori_alt.titulo} ({pts_alt} pontos)")

            ajudou = self._perguntar_sim_nao("\nEssa orientação respondeu sua dúvida? (s/n): ")
            tempo_total = round(time.time() - inicio, 1)

            self.registrar(
                origem="pergunta",
                pergunta=pergunta,
                orientacao_id=melhor_orientacao.id,
                encontrou=True,
                ajudou=ajudou,
                tentativas=tentativas,
                tempo_segundos=tempo_total,
            )
            return

    def navegar(self) -> None:
        """Permite navegar pelas categorias e orientações numeradas com opção 0 para voltar."""
        if not self.base.orientacoes:
            print("\nBase de conhecimento vazia.")
            return

        categorias = self.base.categorias()

        while True:
            print("\n--- Categorias Disponíveis ---")
            for idx, cat in enumerate(categorias, start=1):
                print(f"{idx}. {cat}")
            print("0. Voltar ao menu principal")

            escolha_cat = input("Escolha o número da categoria: ").strip()
            if escolha_cat == "0":
                return

            if not escolha_cat.isdigit() or not (1 <= int(escolha_cat) <= len(categorias)):
                print("Opção inválida. Escolha um número da lista ou 0 para voltar.")
                continue

            categoria_selecionada = categorias[int(escolha_cat) - 1]
            itens_categoria = self.base.por_categoria(categoria_selecionada)

            while True:
                print(f"\n--- Orientações em: {categoria_selecionada} ---")
                for idx, ori in enumerate(itens_categoria, start=1):
                    print(f"{idx}. {ori.titulo}")
                print("0. Voltar às categorias")

                inicio = time.time()
                escolha_ori = input("Escolha o número da orientação: ").strip()

                if escolha_ori == "0":
                    break

                if not escolha_ori.isdigit() or not (1 <= int(escolha_ori) <= len(itens_categoria)):
                    print("Opção inválida. Escolha um número válido ou 0 para voltar.")
                    continue

                orientacao_escolhida: Orientacao = itens_categoria[int(escolha_ori) - 1]
                orientacao_escolhida.exibir()

                ajudou = self._perguntar_sim_nao("\nEssa orientação respondeu sua dúvida? (s/n): ")
                tempo_total = round(time.time() - inicio, 1)

                self.registrar(
                    origem="categoria",
                    pergunta=f"[Categoria: {categoria_selecionada}] {orientacao_escolhida.titulo}",
                    orientacao_id=orientacao_escolhida.id,
                    encontrou=True,
                    ajudou=ajudou,
                    tentativas=1,
                    tempo_segundos=tempo_total,
                )
                return

    def indicadores(self, nota_facilidade: int | None = None) -> None:
        """Calcula e exibe todos os indicadores exigidos pelo edital."""
        total = len(self.historico)
        print("\n" + "=" * 65)
        print(f"INDICADORES DE DESEMPENHO - {self.nome}")
        print("=" * 65)

        if total == 0:
            print("Nenhum atendimento registrado até o momento.")
            if nota_facilidade is not None:
                print(f"Facilidade de uso informada: {nota_facilidade} / 5")
            print("=" * 65)
            return

        encontrados = [r for r in self.historico if r.get("encontrou")]
        ajudaram = [r for r in self.historico if r.get("ajudou")]
        sem_solucao = [r["pergunta"] for r in self.historico if not r.get("encontrou") or not r.get("ajudou")]

        pct_encontrada = (len(encontrados) / total) * 100
        pct_ajudou = (len(ajudaram) / total) * 100
        media_tentativas = sum(r.get("tentativas", 1) for r in self.historico) / total

        if encontrados:
            tempo_medio_encontrar = sum(r.get("tempo_segundos", 0.0) for r in encontrados) / len(encontrados)
        else:
            tempo_medio_encontrar = 0.0

        print(f"Total de atendimentos registrados : {total}")
        print(f"Resposta encontrada (%)           : {pct_encontrada:.1f}%")
        print(f"Tempo médio para encontrar        : {tempo_medio_encontrar:.1f} s")
        if nota_facilidade is not None:
            print(f"Facilidade de uso (1 a 5)         : {nota_facilidade} / 5")
        else:
            print("Facilidade de uso (1 a 5)         : Avaliada ao encerrar o sistema")
        print(f"Taxa de acerto: ajudou (%)        : {pct_ajudou:.1f}%")
        print(f"Tentativas por atendimento        : {media_tentativas:.2f}")

        print("\nLista de dúvidas sem solução:")
        if sem_solucao:
            for duvida in sem_solucao:
                print(f"  - {duvida}")
        else:
            print("  (Nenhuma dúvida sem solução registrada)")
        print("=" * 65)

    def exportar_csv(self) -> None:
        """Exporta todos os registros do histórico para data/atendimentos.csv usando csv.DictWriter."""
        pasta = os.path.dirname(self.caminho_csv)
        if pasta:
            os.makedirs(pasta, exist_ok=True)

        campos = [
            "data",
            "origem",
            "pergunta",
            "id_orientacao",
            "encontrou",
            "ajudou",
            "tentativas",
            "tempo_segundos",
        ]

        try:
            with open(self.caminho_csv, "w", newline="", encoding="utf-8-sig") as arquivo_csv:
                writer = csv.DictWriter(arquivo_csv, fieldnames=campos, delimiter=";")
                writer.writeheader()
                for registro in self.historico:
                    writer.writerow({campo: registro.get(campo, "") for campo in campos})
            print(f"\n[OK] Histórico exportado com sucesso para '{self.caminho_csv}'.")
        except OSError as erro:
            print(f"\n[ERRO] Não foi possível exportar o CSV: {erro}")