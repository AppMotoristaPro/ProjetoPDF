import os
import re
import shutil
from datetime import datetime
from pypdf import PdfReader, PdfWriter

def limpar_nome(nome):
    """Garante que o nome do arquivo seja aceito pelo Windows."""
    nome_limpo = re.sub(r'[^a-zA-ZÀ-ÿ\s]', '', nome).strip()
    return nome_limpo.upper()

def extrair_nome_da_pagina(texto):
    """Busca o nome do colaborador pela âncora definida."""
    linhas = texto.split('\n')
    for i, linha in enumerate(linhas):
        if "Nome do Funcionário" in linha:
            return linhas[i-1].strip()
    return None

def get_pasta_destino(nome_operacao):
    """Cria a estrutura de pastas padronizada no PC da Nexus/DHL."""
    # Usa o caminho oficial do Windows para a pasta Downloads
    pasta_base = os.path.join(os.environ['USERPROFILE'], 'Downloads')
    data_hoje = datetime.now().strftime("%d-%m-%Y")
    pasta_destino = os.path.join(pasta_base, f"Holerites_{nome_operacao}", data_hoje)
    
    os.makedirs(pasta_destino, exist_ok=True)
    return pasta_destino

def processar_holerite_unico(caminho_pdf, nome_operacao):
    """MÓDULO 1: Fatia um PDF grande em vários pedaços."""
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
                
        return True, pasta_destino
    except Exception as e:
        return False, str(e)

def processar_holerites_unitarios(lista_caminhos, nome_operacao):
    """MÓDULO 2: Lê vários PDFs separados e renomeia copiando para a pasta."""
    pasta_destino = get_pasta_destino(nome_operacao)
    
    try:
        for i, caminho_pdf in enumerate(lista_caminhos):
            reader = PdfReader(caminho_pdf)
            # Lê apenas a primeira página para extrair o nome
            texto = reader.pages[0].extract_text()
            nome_bruto = extrair_nome_da_pagina(texto)
            nome_final = limpar_nome(nome_bruto) if nome_bruto else f"FUNC_DESCONHECIDO_ARQ_{i+1}"
            
            caminho_arquivo = os.path.join(pasta_destino, f"{nome_final}.pdf")
            
            # Copia o arquivo original inteiro para o novo destino com o novo nome
            shutil.copy2(caminho_pdf, caminho_arquivo)
            
        return True, pasta_destino
    except Exception as e:
        return False, str(e)

