import os
import re
import shutil
import logging
import sys
from datetime import datetime
from pypdf import PdfReader, PdfWriter

# LÓGICA PARA ACHAR A PASTA DO .EXE
if getattr(sys, 'frozen', False):
    # Se estiver rodando como .exe
    diretorio_atual = os.path.dirname(sys.executable)
else:
    # Se estiver rodando como script (Termux)
    diretorio_atual = os.path.dirname(os.path.abspath(__file__))

caminho_log = os.path.join(diretorio_atual, "debug_log.txt")

logging.basicConfig(
    filename=caminho_log,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    encoding="utf-8"
)

def limpar_nome(nome):
    nome_limpo = re.sub(r'[^a-zA-ZÀ-ÿ\s]', '', nome).strip()
    return nome_limpo.upper()

def extrair_nome_da_pagina(texto):
    linhas = texto.split('\n')
    for i, linha in enumerate(linhas):
        if "Nome do Funcionário" in linha:
            return linhas[i-1].strip()
    return None

def get_pasta_destino(nome_operacao):
    try:
        # No Windows, salva na pasta Downloads do usuário
        pasta_base = os.path.join(os.environ['USERPROFILE'], 'Downloads')
        data_hoje = datetime.now().strftime("%d-%m-%Y")
        pasta_destino = os.path.join(pasta_base, f"Holerites_{nome_operacao}", data_hoje)
        os.makedirs(pasta_destino, exist_ok=True)
        return pasta_destino
    except Exception as e:
        logging.error(f"Erro ao criar pasta: {e}")
        raise

def processar_holerite_unico(caminho_pdf, nome_operacao):
    logging.info(f"Iniciando Módulo Massa: {caminho_pdf}")
    try:
        pasta_destino = get_pasta_destino(nome_operacao)
        reader = PdfReader(caminho_pdf)
        for i, pagina in enumerate(reader.pages):
            texto = pagina.extract_text()
            nome_bruto = extrair_nome_da_pagina(texto)
            nome_final = limpar_nome(nome_bruto) if nome_bruto else f"DESCONHECIDO_{i+1}"
            
            writer = PdfWriter()
            writer.add_page(pagina)
            with open(os.path.join(pasta_destino, f"{nome_final}.pdf"), "wb") as f:
                writer.write(f)
        return True, pasta_destino
    except Exception as e:
        logging.error(f"Falha no Módulo Massa: {e}")
        return False, str(e)

def processar_holerites_unitarios(lista_caminhos, nome_operacao):
    logging.info(f"Iniciando Módulo Unitário: {len(lista_caminhos)} arquivos")
    try:
        pasta_destino = get_pasta_destino(nome_operacao)
        for i, caminho_pdf in enumerate(lista_caminhos):
            reader = PdfReader(caminho_pdf)
            texto = reader.pages[0].extract_text()
            nome_bruto = extrair_nome_da_pagina(texto)
            nome_final = limpar_nome(nome_bruto) if nome_bruto else f"ARQUIVO_{i+1}"
            shutil.copy2(caminho_pdf, os.path.join(pasta_destino, f"{nome_final}.pdf"))
        return True, pasta_destino
    except Exception as e:
        logging.error(f"Falha no Módulo Unitário: {e}")
        return False, str(e)

