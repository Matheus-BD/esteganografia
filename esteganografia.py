DELIMITADOR = "###END###"


def texto_para_binario(texto: str) -> str:
    """Converte o texto em bits usando UTF-8 (aceita acentos, emoji e aspas curvas)."""
    return ''.join(format(b, '08b') for b in texto.encode('utf-8'))


def binario_para_texto(binario: str) -> str:
    dados = bytes(int(binario[i:i + 8], 2) for i in range(0, len(binario) - 7, 8))
    return dados.decode('utf-8', errors='replace')


def aplicar_lsb(pixels: list, bits_mensagem: str) -> list:
    """Aplica LSB apenas nos canais R, G, B, pulando o canal Alpha."""
    novos_pixels = list(pixels)
    idx_bit = 0
    total_bits = len(bits_mensagem)

    for i in range(len(novos_pixels)):
        if idx_bit >= total_bits:
            break
        if i % 4 == 3:  # canal Alpha
            continue
        valor_pixel = int(novos_pixels[i])
        bit_atual = int(bits_mensagem[idx_bit])
        novos_pixels[i] = (valor_pixel & ~1) | bit_atual
        idx_bit += 1

    return novos_pixels


def extrair_lsb(pixels: list) -> str:
    """Extrai LSB dos canais R, G, B até encontrar o delimitador."""
    delimitador = DELIMITADOR.encode('utf-8')
    dados = bytearray()
    byte_atual = 0
    qtd_bits = 0

    for i in range(len(pixels)):
        if i % 4 == 3:
            continue
        byte_atual = (byte_atual << 1) | (int(pixels[i]) & 1)
        qtd_bits += 1

        if qtd_bits == 8:
            dados.append(byte_atual)
            byte_atual = 0
            qtd_bits = 0
            if dados.endswith(delimitador):
                return bytes(dados[:-len(delimitador)]).decode('utf-8', errors='replace')

    return "Nenhuma mensagem secreta válida encontrada."