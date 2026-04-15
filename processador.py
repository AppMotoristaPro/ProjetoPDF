import os
import re
import platform
from datetime import datetime
from pypdf import PdfReader, PdfWriter

def limpar_nome(nome):
    nome_limpo = re.sub(r'[^a-zA-ZÀ-ÿ\s]', '', nome).strip()
    return nome_limpo.upper()

def extrair_nome_da_pagina(texto):
    linhas = texto.split('\n')
    for i, linha in enumerate(linhas):
        if "Nome do Funcionário" in linha:
            return linhas[i-1].strip()
    return None

def processar_holerites(caminho_pdf, nome_operacao):
    # Identifica se está no Windows (PC dela) ou Android (Seu teste)
    if platform.system() == "Windows":
        pasta_base = os.path.join(os.environ['USERPROFILE'], 'Downloads')
    else:
        # Caminho para o seu teste no Termux
        pasta_base = os.path.expanduser("~/storage/downloads")

    # Estrutura: Downloads / Holerites_NOME_OPERACAO / DATA_ATUAL
    data_hoje = datetime.now().strftime("%d-%m-%Y")
    pasta_destino = os.path.join(pasta_base, f"Holerites_{nome_operacao}", data_hoje)
    
    os.makedirs(pasta_destino, exist_ok=True)

    try:
        reader = PdfReader(caminho_pdf)
        for i, pagina in enumerate(reader.pages):
            texto = pagina.extract_text()
            nome_bruto = extrair_nome_da_pagina(texto)
            nome_final = limpar_nome(nome_bruto) if nome_bruto else f"FUNC_DESCONHECIDO_{i+1}"

            writer = PdfWriter()
            writer.add_page(pagina)
            
            caminho_arquivo = os.path.join(pasta_destino, f"{nome_final}.pdf")
            with open(caminho_arquivo, "wb") as f:
                writer.write(f)
        
        return True, pasta_destino
    except Exception as e:
        return False, str(e)

