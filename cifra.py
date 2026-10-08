ALFABETO = (
    "abcdefghijklmnopqrstuvwxyz"
    "áàâãéèêíìîóòôõúùûç"
    "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    "ÁÀÂÃÉÈÊÍÌÎÓÒÔÕÚÙÛÇ"
)

def cifrar(texto: str, chave: int) -> str:
    """Criptografa um texto deslocando os caracteres conforme a chave."""
    resultado = ""
    tamanho_alfabeto = len(ALFABETO)

    for caracter in texto:
        if caracter in ALFABETO:
            indice_atual = ALFABETO.index(caracter)
            novo_indice = (indice_atual + chave) % tamanho_alfabeto
            resultado += ALFABETO[novo_indice]
        else:
            # Mantém espaços, pontuações e números sem alterar
            resultado += caracter

    return resultado


def decifrar(texto: str, chave: int) -> str:
    """Descriptografa um texto aplicando o deslocamento inverso da chave."""
    return cifrar(texto, -chave)