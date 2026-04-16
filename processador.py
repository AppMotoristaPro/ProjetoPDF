import os
import re
import shutil
import logging
from datetime import datetime
from pypdf import PdfReader, PdfWriter

# Configuração básica do logger para registrar no arquivo
logging.basicConfig(
    filename="debug_log.txt",
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
        pasta_base = os.path.join(os.environ['USERPROFILE'], 'Downloads')
        data_hoje = datetime.now().strftime("%d-%m-%Y")
        pasta_destino = os.path.join(pasta_base, f"Holerites_{nome_operacao}", data_hoje)
        os.makedirs(pasta_destino, exist_ok=True)
        logging.info(f"Pasta de destino preparada: {pasta_destino}")
        return pasta_destino
    except Exception as e:
        logging.error(f"Erro ao criar pasta: {e}")
        raise

def processar_holerite_unico(caminho_pdf, nome_operacao):
    logging.info(f"Iniciando MÓDULO MASSA para: {caminho_pdf}")
    pasta_destino = get_pasta_destino(nome_operacao)
    
    try:
        reader = PdfReader(caminho_pdf)
        for i, pagina in enumerate(reader.pages):
            texto = pagina.extract_text()
            nome_bruto = extrair_nome_da_pagina(texto)
            nome_final = limpar_nome(nome_bruto) if nome_bruto else f"FUNC_DESCONHECIDO_PAG_{i+1}"

            writer = PdfWriter()
            writer.add_page(pagina)
            
            caminho_arquivo = os.path.join(pasta_destino, f"{nome_final}.pdf")
            with open(caminho_arquivo, "wb") as f:
                writer.write(f)
            logging.info(f"Página {i+1} fatiada para: {nome_final}.pdf")
                
        return True, pasta_destino
    except Exception as e:
        logging.error(f"Erro no processamento massa: {e}")
        return False, str(e)

def processar_holerites_unitarios(lista_caminhos, nome_operacao):
    logging.info(f"Iniciando MÓDULO UNITÁRIO para {len(lista_caminhos)} arquivos")
    pasta_destino = get_pasta_destino(nome_operacao)
    
    try:
        for i, caminho_pdf in enumerate(lista_caminhos):
            reader = PdfReader(caminho_pdf)
            texto = reader.pages[0].extract_text()
            nome_bruto = extrair_nome_da_pagina(texto)
            nome_final = limpar_nome(nome_bruto) if nome_bruto else f"FUNC_DESCONHECIDO_ARQ_{i+1}"
            
            caminho_arquivo = os.path.join(pasta_destino, f"{nome_final}.pdf")
            shutil.copy2(caminho_pdf, caminho_arquivo)
            logging.info(f"Arquivo renomeado: {nome_final}.pdf")
            
        return True, pasta_destino
    except Exception as e:
        logging.error(f"Erro no processamento unitário: {e}")
        return False, str(e)

