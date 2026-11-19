# GS26-2Pensamento-Computacional-e-Automa-o-com-Python

# assistência do cidadão — Assistente Digital de Orientação ao Cidadão

## Integrante:
- **Nome:** Rubens Henrique Cordeiro dos Santos
- **RM:** 572667
- **Turma:** 1CCPG

## Público e Problema Escolhidos
- **Público-alvo:** Jovens no primeiro emprego e estudantes.
- **Problema:** Muitos jovens enfrentam dificuldades para emitir seus primeiros documentos civis e trabalhistas (como Carteira de Trabalho Digital, Título de Eleitor, Alistamento Militar, CIN e CadÚnico) devido à fragmentação das informações e linguagem burocrática. A **assistência do cidadão** centraliza orientações verificadas em linguagem simples, indicando documentos necessários, canais oficiais e data de verificação, sem coletar dados pessoais.

## ODS Relacionados
- **ODS 8 (Trabalho Decente e Crescimento Econômico):** Facilita o acesso do jovem ao primeiro emprego formal e programas de aprendizagem.
- **ODS 10 (Redução das Desigualdades):** Democratiza o acesso à informação pública e benefícios sociais como CadÚnico e ID Jovem.
- **ODS 16 (Paz, Justiça e Instituições Eficazes):** Promove acesso transparente à informação e documentação básica para o exercício da cidadania.

## Como Executar
1. Ter o Python 3.10+ instalado.
2. Clone o repositório e acesse a pasta do projeto:

   git clone (https://github.com/pudim231/GS26-2Pensamento-Computacional-e-Automa-o-com-Python.git)
   cd citizen-assist-ai
   ou iniciar uma simulação pelo play

##Regra de Pontuação Usada
A busca normaliza a pergunta, as palavras-chave e os títulos (letras minúsculas, sem acentos e sem pontuação) e pontua cada orientação:

+3 pontos: para cada palavra_chave da orientação encontrada na pergunta.

+1 ponto: para cada palavra da pergunta (com 4 ou mais letras) presente no titulo da orientação.

Níveis de Confiança:

ALTA: 6 pontos ou mais.

MÉDIA: 3 a 5 pontos.

Não encontrada: abaixo de 3 pontos (exibe dicas de palavras-chave e lista de categorias).

##Fontes Consultadas
Portal Gov.br — Carteira de Identidade Nacional: https://www.gov.br/governodigital/pt-br/identidade

Tribunal Superior Eleitoral (TSE): https://www.tse.jus.br/servicos-eleitorais/autoatendimento-eleitoral

Exército Brasileiro — Alistamento Online: https://alistamento.eb.mil.br

Receita Federal — Meu CPF: https://www.gov.br/receitafederal/pt-br/assuntos/meu-cpf

Ministério do Trabalho e Emprego — CTPS Digital e Aprendizagem: https://www.gov.br/pt-br/servicos/obter-a-carteira-de-trabalho

Ministério do Desenvolvimento Social — CadÚnico: https://www.gov.br/mds/pt-br/acoes-e-programas/cadastro-unico

Ministério da Saúde — Cartão SUS: https://www.gov.br/saude/pt-br/acesso-a-informacao/acoes-e-programas/cns

Secretaria-Geral da Presidência — ID Jovem: https://www.gov.br/secretariageral/pt-br/assuntos/juventude/id-jovem

##Resultado do Teste com Usuários
(Realizado com 3 pessoas externas, totalizando 10 atendimentos, sem coleta de dados pessoais)

Total de atendimentos: 10

Resposta encontrada (%): [Ex: 90.0%]

Tempo médio para encontrar: [Ex: 6.4 s]

Facilidade de uso (1 a 5): [Ex: 5 / 5]

Taxa de acerto — ajudou (%): [Ex: 90.0%]

Tentativas por atendimento: [Ex: 1.10]

Dúvidas sem solução observadas: [Ex: "como tirar carteira de reservista" antes do ajuste]

Melhoria implementada após os testes: Inclusão da palavra-chave "reservista" e "cam" na orientação ID 3 (Alistamento Militar), fazendo com que a dúvida passasse a ser encontrada com confiança média/alta.

##Limitações
O assistente depende exclusivamente de correspondência lexical por regras (não interpreta sinônimos fora das palavras-chave cadastradas nem erros graves de digitação).

Não realiza agendamentos nem consultas em tempo real aos sistemas governamentais.
