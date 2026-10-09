def filtrar(corpos, tipo=None, temp_min=None, temp_max=None):
    resultado = []

    for c in corpos:
        if tipo and c["bodyType"] != tipo:
            continue

        if temp_min is not None or temp_max is not None:
            if c["avgTemp"] is None:
                continue
            if temp_min is not None and c["avgTemp"] < temp_min:
                continue
            if temp_max is not None and c["avgTemp"] > temp_max:
                continue

        resultado.append(c)

    return resultado