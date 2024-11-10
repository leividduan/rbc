import csv
from difflib import SequenceMatcher


# Função para carregar casos de um arquivo CSV
def carregar_casos_csv(arquivo_csv):
    base_de_casos = []
    with open(arquivo_csv, mode="r", encoding="utf-8") as file:
        leitor_csv = csv.DictReader(file)
        for linha in leitor_csv:
            caso = {
                "problema": linha["Problema"],
                "sintomas": linha["Sintomas"].split(", "),
                "solucao": linha["Solução"],
            }
            base_de_casos.append(caso)
    return base_de_casos


# Função de similaridade
def calcular_similaridade(sintomas_atual, sintomas_caso):
    sintomas_atual = " ".join(sintomas_atual)
    sintomas_caso = " ".join(sintomas_caso)
    return SequenceMatcher(None, sintomas_atual, sintomas_caso).ratio()


# Função para encontrar o caso mais similar
def recuperar_caso(sintomas_problema_atual, base_de_casos):
    caso_mais_similar = None
    maior_similaridade = 0

    for caso in base_de_casos:
        similaridade = calcular_similaridade(sintomas_problema_atual, caso["sintomas"])
        if similaridade > maior_similaridade:
            maior_similaridade = similaridade
            caso_mais_similar = caso

    return caso_mais_similar, maior_similaridade


# Função principal que implementa o ciclo RBC
def rbc_resolver_problema(sintomas_problema_atual, base_de_casos):
    # Etapa 1: Recuperação
    caso, similaridade = recuperar_caso(sintomas_problema_atual, base_de_casos)

    if caso and similaridade > 0.5:  # Define um limiar de similaridade de 50%
        # Etapa 2: Reutilização
        print(f"Problema identificado como similar ao caso: '{caso['problema']}'")
        print(f"Solução sugerida: {caso['solucao']}")

        # Simula a Etapa 3: Revisão - Pedindo feedback do usuário
        sucesso = input("A solução resolveu o problema? (s/n): ").strip().lower() == "s"

        if sucesso:
            print("Problema resolvido e caso registrado.")
        else:
            print("Necessário ajuste na solução.")

        # Etapa 4: Retenção - Adiciona o novo caso à base de dados se necessário
        if not sucesso:
            nova_solucao = input("Insira a nova solução aplicada: ").strip()
            novo_caso = {
                "problema": "Novo caso baseado em feedback",
                "sintomas": sintomas_problema_atual,
                "solucao": nova_solucao,
            }
            base_de_casos.append(novo_caso)
            print("Novo caso adicionado à base de dados.")
    else:
        print("Nenhum caso similar encontrado. Registre manualmente uma nova solução.")
        nova_solucao = input("Insira a nova solução aplicada: ").strip()
        novo_caso = {
            "problema": "Novo caso registrado manualmente",
            "sintomas": sintomas_problema_atual,
            "solucao": nova_solucao,
        }
        base_de_casos.append(novo_caso)
        print("Novo caso adicionado à base de dados.")


# Carregar a base de casos do arquivo CSV
base_de_casos = carregar_casos_csv("csv.csv")

# Teste do sistema RBC com entrada do usuário
print("### Bem-vindo ao Sistema de Suporte RBC ###")
sintomas_problema_atual = (
    input("Descreva os sintomas do problema atual: ").strip().lower().split(", ")
)
rbc_resolver_problema(sintomas_problema_atual, base_de_casos)
