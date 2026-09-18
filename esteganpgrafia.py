from PIL import Image

DELIMITADOR = '00000000'

def texto_para_binario(texto: str):
    bist_lista = [format(ord(char), '08b') for char in texto] # ord(char) descobre o número em formato ascii format pega ele e trasnforma em binario
    return ''.join(bist_lista)

def binario_para_texto(sequecia_binaria: str):
    bytes_lista = [
        sequecia_binaria[i : i + 8] for i in range(0, len(sequecia_binaria), 8) #dividi o a sequecia binaria em pares de 8
    ]
    caracteres = []
    for b in bytes_lista:
        caracteres.append(chr(int(b, 2)))
    # for b in bytes_lista:
    #     if chr(int(b, 2)) == ' ':
    #         caracteres.append('-')
    #     else:
    #         caracteres.append(chr(int(b, 2)))
    return "".join(caracteres)

def ocultar_texto(binario: str, imagem: str):
    img = Image.open(imagem).convert("RGB")
    largura, altura = img.size

    texto_com_fim = binario + DELIMITADOR
    
    bits = [int(bit) for bit in texto_com_fim]

    total_de_bits = len(bits)
    indice_bits = 0
    pixels = img.load()

    for y in range(altura):
        for x in range(largura):
            if indice_bits >= total_de_bits:
                break

            r, g, b = pixels[x, y]
            canais = [r, g, b]

            for i in range(3):
                if indice_bits < total_de_bits:
                    canais[i] = (canais[i] & 254) | bits[indice_bits]
                    indice_bits += 1

            pixels[x, y] = tuple(canais)

        if indice_bits >= total_de_bits:
            break
        
    img.save('imagem_oculta.png')

def revelar_texto(imagem: str):
    img = Image.open(imagem).convert("RGB")
    largura, altura = img.size
    pixels = img.load()

    bits_extraidos = []

    for y in range(altura):
        for x in range(largura):
            r, g, b = pixels[x, y]

            for canal in (r, g, b):
                # Extrai o LSB e adiciona à lista
                bits_extraidos.append(str(canal & 1))

                # Apenas quando acumular um byte completo (multiplo de 8)
                if len(bits_extraidos) % 8 == 0:
                    # Pega o último byte montado
                    ultimo_byte = "".join(bits_extraidos[-8:])

                    # Verifica se o byte é o delimitador
                    if ultimo_byte == DELIMITADOR:
                        # Pega todos os bits anteriores ao delimitador
                        bits_mensagem = "".join(bits_extraidos[:-8])
                        return binario_para_texto(bits_mensagem)

    return "Nenhuma mensagem oculta encontrada."