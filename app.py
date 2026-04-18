import streamlit as st
from datetime import datetime
from processador import processar_pacote_holerites

# Configuração da página e Estilo Visual
st.set_page_config(page_title="Organização de Holerites", page_icon="📑", layout="wide")

# CSS para melhorar a aparência
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stButton>button { width: 100%; border-radius: 10px; height: 3em; font-weight: bold; }
    .stHeader { color: #1e3a8a; }
    .upload-box { border: 2px dashed #cbd5e1; padding: 20px; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

st.title("📑 Organização de Holerites - Thaynara")
st.write("Selecione os arquivos de cada operação para gerar um pacote único organizado.")
st.divider()

# Menu lateral para trocar de ferramenta
st.sidebar.header("Ferramentas")
modo = st.sidebar.radio("Escolha o tipo de entrada:", 
                       ["PDF ÚNICO POR OPERAÇÃO", "VÁRIOS PDFs POR OPERAÇÃO"])

# Estrutura de Colunas para as 3 operações
st.subheader("📥 Upload dos Arquivos")
col1, col2, col3 = st.columns(3)

arquivos_input = {}

with col1:
    st.markdown("### 🏢 ITUPEVA")
    if modo == "PDF ÚNICO POR OPERAÇÃO":
        arquivos_input["ITUPEVA"] = st.file_uploader("PDF Massa Itupeva", type=["pdf"], key="it_massa")
    else:
        arquivos_input["ITUPEVA"] = st.file_uploader("Arquivos Itupeva", type=["pdf"], accept_multiple_files=True, key="it_unit")

with col2:
    st.markdown("### 🏢 CABREÚVA")
    if modo == "PDF ÚNICO POR OPERAÇÃO":
        arquivos_input["CABREUVA"] = st.file_uploader("PDF Massa Cabreúva", type=["pdf"], key="cb_massa")
    else:
        arquivos_input["CABREUVA"] = st.file_uploader("Arquivos Cabreúva", type=["pdf"], accept_multiple_files=True, key="cb_unit")

with col3:
    st.markdown("### 🏢 EMBU DAS ARTES")
    if modo == "PDF ÚNICO POR OPERAÇÃO":
        arquivos_input["EMBU"] = st.file_uploader("PDF Massa Embu", type=["pdf"], key="eb_massa")
    else:
        arquivos_input["EMBU"] = st.file_uploader("Arquivos Embu", type=["pdf"], accept_multiple_files=True, key="eb_unit")

st.divider()

# Botão de Processamento Centralizado
tem_arquivo = any(arquivos_input.values())

if tem_arquivo:
    st.subheader("⚙️ Processamento")
    if st.button("🚀 PROCESSAR TODOS E GERAR PACOTE ÚNICO", type="primary"):
        with st.spinner("Organizando arquivos por operação..."):
            try:
                is_massa = (modo == "PDF ÚNICO POR OPERAÇÃO")
                zip_pronto = processar_pacote_holerites(arquivos_input, modo_massa=is_massa)
                
                st.success("✅ Tudo pronto! O arquivo abaixo contém as pastas organizadas.")
                
                st.download_button(
                    label="⬇️ BAIXAR TUDO ORGANIZADO (.ZIP)",
                    data=zip_pronto,
                    file_name=f"Holerites_Organizados_{datetime.now().strftime('%d-%m-%Y')}.zip",
                    mime="application/zip"
                )
            except Exception as e:
                st.error(f"Ocorreu um erro no processamento: {e}")
else:
    st.warning("Aguardando o upload de pelo menos um arquivo para iniciar.")

st.divider()
st.caption("🛡️ Por segurança, nenhum arquivo fica salvo após o processamento.")

