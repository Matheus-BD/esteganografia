DELIMITADOR = "###END###"

def texto_para_binario(texto: str) -> str:
    return ''.join(format(ord(char), '08b') for char in texto)

def binario_para_texto(binario: str) -> str:
    bytes_list = [binario[i:i+8] for i in range(0, len(binario), 8)]
    caracteres = []
    for byte in bytes_list:
        if len(byte) == 8:
            caracteres.append(chr(int(byte, 2)))
    return ''.join(caracteres)

def aplicar_lsb(pixels: list, bits_mensagem: str) -> list:
    """Aplica LSB apenas nos canais R, G, B, pulando o canal Alpha."""
    novos_pixels = list(pixels)
    idx_bit = 0
    total_bits = len(bits_mensagem)

    for i in range(len(novos_pixels)):
        if idx_bit >= total_bits:
            break

        # A cada 4 valores (R, G, B, A), a posição i % 4 == 3 é o canal Alpha.
        # Nós PULAMOS o canal Alpha para não corromper a imagem.
        if i % 4 == 3:
            continue

        valor_pixel = int(novos_pixels[i])
        bit_atual = int(bits_mensagem[idx_bit])
        novos_pixels[i] = (valor_pixel & ~1) | bit_atual
        idx_bit += 1

    return novos_pixels

def extrair_lsb(pixels: list) -> str:
    """Extrai LSB apenas dos canais R, G, B, pulando o canal Alpha."""
    bits = []
    texto_acumulado = ""

    for i in range(len(pixels)):
        # Pula o canal Alpha na leitura também
        if i % 4 == 3:
            continue

        val = int(pixels[i])
        bits.append(str(val & 1))

        if len(bits) % 8 == 0:
            byte_atual = ''.join(bits[-8:])
            char_atual = chr(int(byte_atual, 2))
            texto_acumulado += char_atual

            if texto_acumulado.endswith(DELIMITADOR):
                return texto_acumulado[:-len(DELIMITADOR)]

    return "Nenhuma mensagem secreta válida encontrada."