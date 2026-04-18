import streamlit as st
from datetime import datetime
from processador import processar_holerite_massa_zip, processar_holerites_unitarios_zip

# Configuração da página (deve ser a primeira linha do Streamlit)
st.set_page_config(page_title="Central de Holerites", page_icon="📄", layout="centered")

# Cabeçalho
st.title("📄 Central de Holerites - DHL")
st.write("Ferramenta de processamento e organização de PDF.")
st.divider()

# Escolha da ferramenta e operação
modo = st.radio("Escolha a ferramenta:", ["PDF ÚNICO EM MASSA (Fatiador)", "VÁRIOS PDFs INDIVIDUAIS (Renomeador)"])
operacao = st.selectbox("Selecione a Operação:", ["ITUPEVA", "CABREUVA", "EMBU DAS ARTES"])

# Lógica da Interface
if modo == "PDF ÚNICO EM MASSA (Fatiador)":
    st.info("Faça o upload do arquivo PDF gigante contendo todos os holerites juntos.")
    arquivo = st.file_uploader("Arraste ou selecione o PDF", type=["pdf"], accept_multiple_files=False)

    if arquivo:
        if st.button("Processar e Fatiar", type="primary"):
            with st.spinner("Trabalhando... Isso pode levar alguns segundos."):
                try:
                    # Roda o processador e recebe o ZIP em memória
                    zip_pronto = processar_holerite_massa_zip(arquivo, operacao)
                    st.success("✅ Holerites separados e organizados com sucesso!")
                    
                    # Botão nativo para baixar o ZIP
                    st.download_button(
                        label="⬇️ Baixar Pasta de Holerites (ZIP)",
                        data=zip_pronto,
                        file_name=f"Holerites_{operacao}_{datetime.now().strftime('%d-%m-%Y')}.zip",
                        mime="application/zip"
                    )
                except Exception as e:
                    st.error(f"Erro ao processar arquivo: {e}")

else:
    st.info("Faça o upload de vários PDFs individuais. Você pode selecionar dezenas de uma vez.")
    arquivos = st.file_uploader("Arraste ou selecione os PDFs", type=["pdf"], accept_multiple_files=True)

    if arquivos:
        if st.button("Renomear e Organizar", type="primary"):
            with st.spinner(f"Renomeando {len(arquivos)} arquivos..."):
                try:
                    # Roda o processador unitário e recebe o ZIP em memória
                    zip_pronto = processar_holerites_unitarios_zip(arquivos, operacao)
                    st.success("✅ Holerites renomeados com sucesso!")
                    
                    st.download_button(
                        label="⬇️ Baixar Pasta de Holerites (ZIP)",
                        data=zip_pronto,
                        file_name=f"Holerites_{operacao}_{datetime.now().strftime('%d-%m-%Y')}.zip",
                        mime="application/zip"
                    )
                except Exception as e:
                    st.error(f"Erro ao processar arquivos: {e}")

st.divider()
st.caption("Nexus - Sistema Seguro. Nenhum arquivo fica salvo no servidor após o processamento.")

