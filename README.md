# Crônicas do Espaço (Parte 1)

Sistema de consulta e planejamento de missões espaciais com dados reais do Sistema Solar. Usa uma **Trie** implementada do zero e um **algoritmo guloso** de seleção de destinos.

## Como executar

Requer Python 3.10 ou superior e a biblioteca `requests`.

```
pip install requests
python main.py
```

## Estrutura do projeto

```
main.py                  menu do programa
api.py                   busca e organiza os dados da API
estruturas/trie.py       Trie
servicos/consultas.py    filtro por tipo e temperatura
servicos/formatacao.py   exibição dos dados de um corpo
servicos/missao.py       algoritmo guloso
utils/normalizacao.py    normalização de texto
dados/dados.json         cópia dos dados (opção 5 do menu)
```

## Fonte de dados

- **API:** The Solar System OpenData
- **Endereço:** https://api.le-systeme-solaire.net/rest/bodies/
- **Endpoint usado:** `GET /rest/bodies/` (devolve todos os corpos)
- **Formato:** JSON

A API tem planetas, luas, asteroides, cometas e planetas anões (554 corpos), com dados físicos e orbitais. Isso é suficiente para busca, filtros e para o problema de otimização.

Exemplo de requisição:

```python
resposta = requests.get("https://api.le-systeme-solaire.net/rest/bodies/")
corpos = resposta.json()["bodies"]
```

A resposta é um objeto com uma chave `bodies`, que contém a lista de corpos. Exemplo (Marte, só os campos usados):

```json
{
  "id": "mars",
  "englishName": "Mars",
  "isPlanet": true,
  "bodyType": "Planet",
  "gravity": 3.71,
  "meanRadius": 3389.5,
  "avgTemp": 210,
  "mass": {"massValue": 6.41712, "massExponent": 23},
  "density": 3.9341,
  "aroundPlanet": null,
  "escape": 5030.0,
  "semimajorAxis": 227939200
}
```

## Modelagem

Cada corpo é um dicionário Python com os campos filtrados em `api.py`. A lista de corpos fica em memória durante a execução, e a Trie guarda referências aos mesmos dicionários.

| Atributo | Uso |
|---|---|
| `englishName` | chave da Trie |
| `bodyType` | filtro por tipo |
| `avgTemp` | filtro por temperatura (K) |
| `aroundPlanet` | escolha dos candidatos da missão |
| `semimajorAxis` | distância (km), na missão |
| `escape` | velocidade de escape (m/s), na missão |
| `meanRadius` | benefício, na missão |

Operações do menu:

1. Buscar corpo por nome (Trie)
2. Buscar corpos por prefixo (Trie)
3. Filtrar por tipo e/ou faixa de temperatura
4. Planejar missão (guloso)
5. Salvar os dados em arquivo

Decisões de projeto:

- **Normalização:** o texto vai para minúsculas, sem acentos, e o caractere `ʻ` vira `'`. A mesma função é usada na inserção e na busca.
- **Filhos como vetor de 128 posições**, indexado por `ord(c)`. Os nomes têm letras, dígitos, espaço e símbolos como `-`, `'` e `/`, então 26 posições não bastam. O vetor também evita usar `dict` dentro da estrutura.
- **Uma referência por nó:** os 521 `englishName` são únicos, então não há chaves repetidas.
- **A Trie só indexa nomes.** O filtro por tipo e temperatura percorre a lista, porque a Trie não serve para comparação numérica.

## Estrutura de dados: Trie

**Por que a Trie:** as operações principais do sistema são buscar por nome e por prefixo. A Trie faz as duas com custo proporcional ao tamanho do texto, independente do número de corpos, e devolve os resultados por prefixo em ordem alfabética.

**Operações:**

- `inserir(nome, corpo)`
- `buscar(nome)`
- `busca_por_prefixo(prefixo)`

**Instrumentação** (contadores dentro dos métodos da Trie):

- `nos_criados`: nós criados na carga dos dados (1.895).
- `nos_visitados`: nós percorridos na última busca. Para "Mars" são 4.
- `nos_descida`: nós percorridos até chegar ao prefixo. A coleta é `nos_visitados - nos_descida`.

**Complexidade** (L = tamanho da chave, k = nós abaixo do prefixo):

| Operação | Custo       |
|---|-------------|
| `inserir` | O(L)        |
| `buscar` | O(L)        |
| `busca_por_prefixo` | O(L + 128k) |

**Integração:** o `main.py` constrói a Trie ao iniciar e as opções 1 e 2 do menu a usam, imprimindo os nós visitados.


## Algoritmo guloso: planejamento de missão

**Problema:** escolher destinos que maximizem o benefício respeitando dois orçamentos.

- **Candidatos:** corpos que orbitam o Sol, com dados disponíveis. As luas ficam de fora porque a distância delas é medida até o planeta, e não até o Sol.
- **Benefício:** área da superfície para ser explorada, 4·π·raio².
- **Recursos:** distância (`semimajorAxis`, km) e velocidade de escape (`escape`, m/s).

**Estratégia:**

1. Ordenar os candidatos por `meanRadius / semimajorAxis`, do maior para o menor.
2. Percorrer a lista e aceitar cada corpo que ainda couber nos dois orçamentos.

**Por que esse critério:** é a ideia clássica da mochila. Corpos grandes e próximos rendem mais por km gasto, então entram primeiro.

**Complexidade:** O(n log n)

**Exemplo:** com orçamento de 3.000.000.000 km e 100.000 m/s, o sistema escolhe Jupiter, Venus, Earth, Mercury, Mars e 1 Ceres, gastando 1.736.005.569 km e 91.540 m/s.

**Limitações:**

- O guloso não garante o ótimo.
- Área de superfície não mede interesse científico, e somar distâncias não representa rotas orbitais reais.

## Filtragem

`filtrar(corpos, tipo, temp_min, temp_max)` percorre a lista e descarta o corpo que falha em algum critério informado. Todos os critérios são opcionais, e o corpo precisa passar por todos os que foram informados. O custo é O(n).

O tipo deve ser digitado como a API devolve (`Moon`, `Planet`, `Asteroid`, `Comet`, `Dwarf Planet`, `Star`). A temperatura é em Kelvin.
