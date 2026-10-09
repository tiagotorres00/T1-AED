from utils.normalizacao import normalizar
class No:

    def __init__(self):
        self.filhos = [None] * 128
        self.fim_de_palavra = False
        self.corpo = None


class Trie:

    def __init__(self):
        self.raiz = No()
        self.nos_visitados = 0
        self.nos_descida = 0
        self.nos_criados = 0

    def inserir(self, nome, corpo):
        nome = normalizar(nome)
        no_atual = self.raiz

        for caractere in nome:
            indice = ord(caractere)
            if no_atual.filhos[indice] is None:
                no_atual.filhos[indice] = No()
                self.nos_criados += 1
            no_atual = no_atual.filhos[indice]

        no_atual.fim_de_palavra = True
        no_atual.corpo = corpo


    def buscar(self, nome):
        self.nos_visitados = 0
        nome = normalizar(nome)
        no_atual = self.raiz

        for caractere in nome:
            indice = ord(caractere)
            if no_atual.filhos[indice] is None:
                return None

            no_atual = no_atual.filhos[indice]
            self.nos_visitados += 1

        return no_atual.corpo

    def busca_por_prefixo(self, prefixo):
        resultados = []
        prefixo = normalizar(prefixo)
        no_atual = self.raiz
        self.nos_visitados = 0
        self.nos_descida = 0

        for caractere in prefixo:
            indice = ord(caractere)
            if no_atual.filhos[indice] is None:
                return resultados

            no_atual = no_atual.filhos[indice]
            self.nos_visitados += 1

        self.nos_descida = self.nos_visitados

        def _dfs(no):
            if no.fim_de_palavra:
                resultados.append(no.corpo)

            for filho in no.filhos:
                if filho is not None:
                    self.nos_visitados += 1
                    _dfs(filho)

        _dfs(no_atual)
        return resultados