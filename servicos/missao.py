# Beneficio: meanRadius, quanto maior, mais area para explorar
# Recursos: semimajorAxis (distancia), escape (velocidade para sair de orbita)
# Levamos em conta que nao viajamos de corpo em corpo, e sim base perto do sol -> corpo -> base -> corpo -> ...
import math

def selecionar_candidatos(corpos):
    candidatos = []

    for c in corpos:
        if c["aroundPlanet"] is None and c["semimajorAxis"] > 0 and c["meanRadius"] > 0 and c["escape"] > 0:
            candidatos.append(c)

    return candidatos

def planejar_missao(corpos, orcamento_distancia, orcamento_escape):
    candidatos = selecionar_candidatos(corpos)

    candidatos.sort(key=lambda c: c["meanRadius"] / c["semimajorAxis"], reverse=True)

    escolhidos = []
    gasto_dist = 0
    gasto_escape = 0

    for c in candidatos:
        distancia = c["semimajorAxis"]
        escape = c["escape"]

        if gasto_dist + distancia <= orcamento_distancia and gasto_escape + escape <= orcamento_escape:
            escolhidos.append(c)
            gasto_dist += distancia
            gasto_escape += escape

    # Beneficio vai ser a area total explorada
    beneficio = sum(4 * math.pi * c["meanRadius"]**2 for c in escolhidos)
    return escolhidos, gasto_dist, gasto_escape, beneficio