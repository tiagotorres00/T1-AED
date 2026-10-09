def _fmt(valor, unidade=""):
    """Devolve o valor formatado, ou 'N/D' se for None."""
    if valor is None:
        return "N/D"
    return f"{valor} {unidade}".strip()


def _fmt_massa(massa):
    if not massa or massa.get("massValue") is None:
        return "N/D"
    return f"{massa['massValue']} x 10^{massa['massExponent']} kg"


def _fmt_orbita(around):
    if not around:
        return "Nenhum (orbita o Sol)"
    return around.get("planet") or "N/D"


def exibir_corpo(corpo):
    print("=" * 40)
    print(f"  {corpo['englishName']}")
    print("=" * 40)
    print(f"Tipo:                {_fmt(corpo['bodyType'])}")
    print(f"É planeta:           {'Sim' if corpo['isPlanet'] else 'Não'}")
    print(f"Orbita:              {_fmt_orbita(corpo['aroundPlanet'])}")
    print(f"Massa:               {_fmt_massa(corpo['mass'])}")
    print(f"Raio médio:          {_fmt(corpo['meanRadius'], 'km')}")
    print(f"Gravidade:           {_fmt(corpo['gravity'], 'm/s²')}")
    print(f"Densidade:           {_fmt(corpo['density'], 'g/cm³')}")
    print(f"Vel. de escape:      {_fmt(corpo['escape'], 'm/s')}")
    print(f"Temperatura média:   {_fmt(corpo['avgTemp'], 'K')}")
    print(f"Descoberto por:      {_fmt(corpo['discoveredBy'] or None)}")
    print(f"Data de descoberta:  {_fmt(corpo['discoveryDate'] or None)}")
    print("")