import re
import io
import zipfile
from datetime import datetime
from pypdf import PdfReader, PdfWriter

def limpar_nome(nome):
    """Garante que o nome do arquivo seja aceito pelo sistema."""
    nome_limpo = re.sub(r'[^a-zA-ZÀ-ÿ\s]', '', nome).strip()
    return nome_limpo.upper()

def extrair_nome_da_pagina(texto):
    """Busca a âncora e extrai o nome do funcionário."""
    linhas = texto.split('\n')
    for i, linha in enumerate(linhas):
        if "Nome do Funcionário" in linha:
            return linhas[i-1].strip()
    return None

def processar_holerite_massa_zip(arquivo_upload, nome_operacao):
    """Recebe o PDF gigante, fatia e devolve um arquivo .zip na memória."""
    zip_buffer = io.BytesIO() # Cria um espaço na memória para o ZIP
    data_hoje = datetime.now().strftime("%d-%m-%Y")
    pasta_base = f"Holerites_{nome_operacao}_{data_hoje}/"

    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
        reader = PdfReader(arquivo_upload)
        for i, pagina in enumerate(reader.pages):
            texto = pagina.extract_text()
            nome_bruto = extrair_nome_da_pagina(texto)
            nome_final = limpar_nome(nome_bruto) if nome_bruto else f"DESCONHECIDO_PAG_{i+1}"

            writer = PdfWriter()
            writer.add_page(pagina)

            # Escreve a nova página em um PDF na memória
            pdf_buffer = io.BytesIO()
            writer.write(pdf_buffer)

            # Adiciona o PDF virtual para dentro do ZIP
            zip_file.writestr(f"{pasta_base}{nome_final}.pdf", pdf_buffer.getvalue())

    zip_buffer.seek(0)
    return zip_buffer

def processar_holerites_unitarios_zip(lista_uploads, nome_operacao):
    """Recebe vários PDFs individuais, lê os nomes e devolve um .zip organizado."""
    zip_buffer = io.BytesIO()
    data_hoje = datetime.now().strftime("%d-%m-%Y")
    pasta_base = f"Holerites_{nome_operacao}_{data_hoje}/"

    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
        for i, arquivo in enumerate(lista_uploads):
            reader = PdfReader(arquivo)
            texto = reader.pages[0].extract_text()
            nome_bruto = extrair_nome_da_pagina(texto)
            nome_final = limpar_nome(nome_bruto) if nome_bruto else f"DESCONHECIDO_ARQ_{i+1}"

            # Reseta o cursor do arquivo e salva o original com o novo nome no ZIP
            arquivo.seek(0)
            zip_file.writestr(f"{pasta_base}{nome_final}.pdf", arquivo.read())

    zip_buffer.seek(0)
    return zip_buffer

