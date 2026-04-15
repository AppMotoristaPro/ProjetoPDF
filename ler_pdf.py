from pypdf import PdfReader
import re

# Coloque o nome do arquivo que você quer testar
caminho_pdf = "holerite_teste.pdf"

try:
    reader = PdfReader(caminho_pdf)
    pagina = reader.pages[0] 
    texto = pagina.extract_text()
    
    # Separando o texto linha por linha
    linhas = texto.split('\n')
    nome_encontrado = "NOME_NAO_ENCONTRADO"
    
    for i, linha in enumerate(linhas):
        # Procura a linha que contém a nossa âncora
        if "Nome do Funcionário" in linha:
            # O nome está exatamente na linha de cima (índice i - 1)
            nome_bruto = linhas[i-1].strip()
            
            # HIGIENIZAÇÃO: Remove qualquer coisa que não seja letra ou espaço
            # Isso evita que o Windows dê erro na hora de salvar o PDF
            nome_limpo = re.sub(r'[^a-zA-ZÀ-ÿ\s]', '', nome_bruto).strip()
            
            # Converte para maiúsculas para manter o padrão
            nome_encontrado = nome_limpo.upper()
            
            break # Como achou o primeiro, pode parar a busca
            
    print("\n" + "="*50)
    print(f"✅ NOME EXTRAÍDO PARA O ARQUIVO: {nome_encontrado}.pdf")
    print("="*50 + "\n")

except Exception as e:
    print(f"Erro ao tentar ler o PDF: {e}")

