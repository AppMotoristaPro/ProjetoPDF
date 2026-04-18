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

def processar_pacote_holerites(arquivos_por_operacao, modo_massa=True):
    """
    arquivos_por_operacao: Dicionário {'ITUPEVA': file, 'CABREUVA': file, ...}
    modo_massa: True se for PDF único por op, False se for lista de arquivos por op.
    """
    zip_buffer = io.BytesIO()
    data_hoje = datetime.now().strftime("%d-%m-%Y")
    
    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
        for operacao, arquivo_ou_lista in arquivos_por_operacao.items():
            if not arquivo_ou_lista:
                continue
                
            # Define a subpasta dentro do ZIP
            pasta_operacao = f"Holerites_{operacao}_{data_hoje}/"
            
            # Se for Modo Massa (PDF único com várias páginas)
            if modo_massa:
                reader = PdfReader(arquivo_ou_lista)
                for i, pagina in enumerate(reader.pages):
                    texto = pagina.extract_text()
                    nome_bruto = extrair_nome_da_pagina(texto)
                    nome_final = limpar_nome(nome_bruto) if nome_bruto else f"PAGINA_{i+1}"
                    
                    writer = PdfWriter()
                    writer.add_page(pagina)
                    pdf_out = io.BytesIO()
                    writer.write(pdf_out)
                    zip_file.writestr(f"{pasta_operacao}{nome_final}.pdf", pdf_out.getvalue())
            
            # Se for Modo Unitário (Vários arquivos individuais)
            else:
                for i, arquivo in enumerate(arquivo_ou_lista):
                    reader = PdfReader(arquivo)
                    texto = reader.pages[0].extract_text()
                    nome_bruto = extrair_nome_da_pagina(texto)
                    nome_final = limpar_nome(nome_bruto) if nome_bruto else f"ARQUIVO_{i+1}"
                    
                    arquivo.seek(0)
                    zip_file.writestr(f"{pasta_operacao}{nome_final}.pdf", arquivo.read())

    zip_buffer.seek(0)
    return zip_buffer

