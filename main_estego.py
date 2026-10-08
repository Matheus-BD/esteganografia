from pyscript import document, window
from js import ImageData, Uint8ClampedArray
from pyodide.ffi import create_proxy
from esteganografia import texto_para_binario, aplicar_lsb, extrair_lsb, DELIMITADOR


def processar_ocultar(event):
    texto = document.querySelector("#textoOculto").value
    input_file = document.querySelector("#imagemInput")
    saida = document.querySelector("#saida")
    container_download = document.querySelector("#downloadContainer")

    if not input_file.files.length:
        saida.innerText = "Selecione uma imagem primeiro."
        return

    if not texto:
        saida.innerText = "Digite uma mensagem para esconder."
        return

    canvas = document.querySelector("#canvasPreview")
    ctx = canvas.getContext("2d")

    if canvas.width == 0 or canvas.height == 0:
        saida.innerText = "Aguarde o carregamento completo da imagem."
        return

    image_data = ctx.getImageData(0, 0, canvas.width, canvas.height)
    pixels = list(image_data.data)

    bits = texto_para_binario(texto + DELIMITADOR)

    capacidade_bits = (len(pixels) // 4) * 3
    if len(bits) > capacidade_bits:
        saida.innerText = "A mensagem é grande demais para esta imagem. Use uma imagem maior ou um texto menor."
        return

    novos_pixels = aplicar_lsb(pixels, bits)

    typed_array = Uint8ClampedArray.new(novos_pixels)
    nova_image_data = ImageData.new(typed_array, canvas.width, canvas.height)
    ctx.putImageData(nova_image_data, 0, 0)

    data_url = canvas.toDataURL("image/png")

    container_download.innerHTML = (
        f'<a href="{data_url}" download="mensagem_secreta.png" class="btn-download">'
        f'Baixar imagem PNG</a>'
    )

    saida.innerText = "Mensagem escondida. Baixe a nova imagem abaixo."


def processar_revelar(event):
    input_file = document.querySelector("#imagemInput")
    saida = document.querySelector("#saida")

    if not input_file.files.length:
        saida.innerText = "Selecione a imagem PNG com a mensagem secreta."
        return

    canvas = document.querySelector("#canvasPreview")
    ctx = canvas.getContext("2d")

    image_data = ctx.getImageData(0, 0, canvas.width, canvas.height)
    pixels = list(image_data.data)

    mensagem = extrair_lsb(pixels)

    if mensagem and mensagem != "Nenhuma mensagem secreta válida encontrada.":
        saida.innerText = mensagem
    else:
        saida.innerText = "Nenhuma mensagem secreta foi encontrada nesta imagem."


def carregar_imagem_no_canvas(event):
    files = event.target.files
    saida = document.querySelector("#saida")
    document.querySelector("#downloadContainer").innerHTML = ""

    if files.length > 0:
        file = files.item(0)
        reader = window.FileReader.new()

        def on_load_file(e):
            img = window.Image.new()

            def on_load_img(e):
                canvas = document.querySelector("#canvasPreview")
                canvas.width = img.width
                canvas.height = img.height
                ctx = canvas.getContext("2d")
                ctx.drawImage(img, 0, 0)
                saida.innerText = "Imagem carregada. Escolha Esconder ou Revelar."

            img.onload = create_proxy(on_load_img)
            img.src = e.target.result

        reader.onload = create_proxy(on_load_file)
        reader.readAsDataURL(file)


document.querySelector("#imagemInput").addEventListener(
    "change", create_proxy(carregar_imagem_no_canvas)
)