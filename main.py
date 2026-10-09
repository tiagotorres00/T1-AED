from api import obter_corpos, salvar_dados
from servicos.formatacao import exibir_corpo
from servicos.missao import planejar_missao
from servicos.consultas import filtrar
from estruturas.trie import Trie

def busca_por_nome(trie):
    nome = input("Nome: ")
    corpo = trie.buscar(nome)

    if corpo:
        exibir_corpo(corpo)
        print("Nos visitados: ", trie.nos_visitados, "\n")
    else:
        print("Corpo nao encontrado\n")

def busca_por_prefixo(trie):
    prefixo = input("Prefixo: ")
    resultados = trie.busca_por_prefixo(prefixo)

    if len(resultados) == 0:
        print("Nenhum corpo encontrado")
    else:
        for i in range(len(resultados)):
            print(i+1, "-", resultados[i]["englishName"], "(", resultados[i]["bodyType"], ")")

        escolha = input("Escolha um corpo para ver detalhes (Enter para voltar): ")

        if escolha.isdigit() and 1 <= int(escolha) <= len(resultados):
            exibir_corpo(resultados[int(escolha)-1])

        print("Nos na descida: ", trie.nos_descida, "\n")
        print("Nos na coleta: ", trie.nos_visitados - trie.nos_descida, "\n")

def filtro():
    tipo = input("Tipo (Enter para ignorar): ")
    temp_min = input("Temperatura minima em K (Enter para ignorar): ")
    temp_max = input("Temperatura maxima em K (Enter para ignorar): ")

    temp_min = float(temp_min) if temp_min.strip() else None
    temp_max = float(temp_max) if temp_max.strip() else None

    resultado = filtrar(corpos, tipo, temp_min, temp_max)

    for corpo in resultado:
        exibir_corpo(corpo)

    print(len(resultado), "corpos encontrados\n")

def missao():
    dist = float(input("Orcamento de distancia (km): "))
    esc = float(input("Orcamento de escape (m/s): "))

    escolhidos, gasto_dist, gasto_esc, beneficio = planejar_missao(corpos, dist, esc)

    print("\nDestinos escolhidos:")
    for c in escolhidos:
        print(c["englishName"], "| raio:", c["meanRadius"], "| distancia:", c["semimajorAxis"], "| razao:", c["meanRadius"] / c["semimajorAxis"],"| escape:", c["escape"])
    print("\nDistasncia gasta:", gasto_dist, "/", dist)
    print("Escape gasto:", gasto_esc, "/", esc)
    print("Area total explorada: ", beneficio, "km²\n")

if __name__ == '__main__':
    print("Carregando dados da API\n")
    corpos = obter_corpos()

    trie = Trie()

    for corpo in corpos:
        if corpo["englishName"]:
            trie.inserir(corpo["englishName"], corpo)

    print(len(corpos), "corpos carregados")
    print("Nos criados na trie: ", trie.nos_criados, "\n")

    while True:
        print("1 - Buscar corpo por nome")
        print("2 - Buscar por prefixo")
        print("3 - Filtrar por tipo ou temperatura")
        print("4 - Planejar missao")
        print("5 - Salvar dados em arquivo")
        print("0 - Sair")
        opcao = input("Opcao: ")

        match opcao:
            case "1":
                busca_por_nome(trie)
            case "2":
                busca_por_prefixo(trie)
            case "3":
                filtro()
            case "4":
                missao()
            case "5":
                salvar_dados(corpos)
            case "0":
                print("Saindo")
                break
            case _:
                print("Opcao invalida")