import json
import os
from orientacao import Orientacao

ACENTOS = {
    "á": "a",
    "à": "a",
    "ã": "a",
    "â": "a",
    "é": "e",
    "ê": "e",
    "í": "i",
    "ó": "o",
    "õ": "o",
    "ô": "o",
    "ú": "u",
    "ç": "c",
}


def normalizar(texto: str) -> str:
    """Remove acentos, pontuação e converte o texto para minúsculas."""
    texto = texto.lower().strip()
    for letra, troca in ACENTOS.items():
        texto = texto.replace(letra, troca)
    for sinal in "?!.,;:()[]{}-_/\\\"'":
        texto = texto.replace(sinal, " ")
    return " ".join(texto.split())


class BaseConhecimento:
    """Gerencia o conjunto de orientações carregadas do arquivo JSON."""

    def __init__(self, caminho: str):
        self.caminho = caminho
        self.orientacoes: list[Orientacao] = []

    def carregar(self) -> bool:
        """Lê o arquivo JSON de forma segura e instancia os objetos Orientacao."""
        self.orientacoes = []

        if not os.path.exists(self.caminho):
            print(f"\n[ERRO] Arquivo '{self.caminho}' não encontrado.")
            print("Verifique se a pasta 'data' e o arquivo 'base_conhecimento.json' existem.")
            return False

        try:
            with open(self.caminho, "r", encoding="utf-8") as arquivo:
                dados = json.load(arquivo)

            if not isinstance(dados, list):
                print("\n[ERRO] Formato inválido na base de conhecimento (esperada uma lista).")
                return False

            campos_obrigatorios = {
                "id",
                "categoria",
                "titulo",
                "palavras_chave",
                "resposta",
                "documentos",
                "onde",
                "fonte",
                "verificado_em",
            }

            for item in dados:
                if not isinstance(item, dict) or not campos_obrigatorios.issubset(item.keys()):
                    print("\n[AVISO] Registro ignorado por falta de campos obrigatórios.")
                    continue

                orientacao = Orientacao(
                    id_orientacao=int(item["id"]),
                    categoria=str(item["categoria"]),
                    titulo=str(item["titulo"]),
                    palavras_chave=list(item["palavras_chave"]),
                    resposta=str(item["resposta"]),
                    documentos=list(item["documentos"]),
                    onde=str(item["onde"]),
                    fonte=str(item["fonte"]),
                    verificado_em=str(item["verificado_em"]),
                )
                self.orientacoes.append(orientacao)

            return len(self.orientacoes) > 0

        except json.JSONDecodeError:
            print(f"\n[ERRO] O arquivo '{self.caminho}' está corrompido (JSON inválido).")
            return False
        except OSError as erro:
            print(f"\n[ERRO] Falha ao ler o arquivo '{self.caminho}': {erro}")
            return False

    def categorias(self) -> list[str]:
        """Retorna a lista de categorias únicas em ordem alfabética."""
        unicas = sorted({ori.categoria for ori in self.orientacoes})
        return unicas

    def por_categoria(self, categoria: str) -> list[Orientacao]:
        """Retorna todas as orientações pertencentes a uma categoria."""
        return [ori for ori in self.orientacoes if ori.categoria == categoria]

    def pontuar(self, pergunta_normalizada: str, orientacao: Orientacao) -> int:
        """
        Calcula a pontuação de relevância entre a pergunta e uma orientação:
        +3 pontos para cada palavra-chave que aparece na pergunta;
        +1 ponto para cada palavra da pergunta (4+ letras) que aparece no título.
        """
        pontos = 0
        palavras_pergunta = pergunta_normalizada.split()
        titulo_norm = normalizar(orientacao.titulo)
        palavras_titulo = set(titulo_norm.split())

        for kw in orientacao.palavras_chave:
            kw_norm = normalizar(kw)
            if kw_norm and kw_norm in pergunta_normalizada:
                pontos += 3

        for palavra in set(palavras_pergunta):
            if len(palavra) >= 4 and palavra in palavras_titulo:
                pontos += 1

        return pontos

    def buscar(self, pergunta: str) -> list[tuple[int, Orientacao]]:
        """
        Retorna uma lista de tuplas (pontos, orientacao) ordenada da maior
        para a menor pontuação (apenas itens com pontos > 0).
        """
        pergunta_norm = normalizar(pergunta)
        if not pergunta_norm:
            return []

        resultados: list[tuple[int, Orientacao]] = []
        for orientacao in self.orientacoes:
            pts = self.pontuar(pergunta_norm, orientacao)
            if pts > 0:
                resultados.append((pts, orientacao))

        resultados.sort(key=lambda item: (item[0], -item[1].id), reverse=True)
        return resultados