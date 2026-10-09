import unicodedata

def normalizar(texto):
    texto = (texto or "").strip().lower()
    texto = texto.replace("ʻ", "'")
    texto = unicodedata.normalize("NFD", texto)
    return "".join(c for c in texto if unicodedata.category(c) != "Mn")


