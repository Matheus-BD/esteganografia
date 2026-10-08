from pyscript import document
from cifra import cifrar, decifrar

def executar_processamento(modo):
    texto_input = document.querySelector("#texto").value
    chave_val = document.querySelector("#chave").value
    chave_input = int(chave_val) if chave_val else 0

    if modo == "codificar":
        resultado = cifrar(texto_input, chave_input)
    else:
        resultado = decifrar(texto_input, chave_input)

    document.querySelector("#saida").innerText = resultado

def processar_codificar(event):
    executar_processamento("codificar")

def processar_decodificar(event):
    executar_processamento("decodificar")

