# pages/0_📤_Upload.py
import streamlit as st
import pandas as pd

st.set_page_config(page_title="Upload de Dados", page_icon="📤")

st.title("📤 Carregar Dados")
st.markdown("Faça o upload do arquivo Excel com os dados dos alunos para começar.")

# Inicializar a variável de sessão se não existir[citation:2]
if 'df_principal' not in st.session_state:
    st.session_state.df_principal = None

# Widget de upload[citation:3]
uploaded_file = st.file_uploader(
    "Escolha um arquivo Excel",
    type=['xlsx', 'xls'],  # Aceita .xlsx e .xls[citation:3]
    key="uploader_global"
)

if uploaded_file is not None:
    try:
        # Ler o arquivo Excel[citation:1]
        df = pd.read_excel(uploaded_file)
        
        # Salvar no session state[citation:2][citation:7]
        st.session_state.df_principal = df
        st.session_state.nome_arquivo = uploaded_file.name
        
        st.success(f"✅ Arquivo **{uploaded_file.name}** carregado com sucesso!")
        st.info(f"📊 **{len(df)}** registros e **{len(df.columns)}** colunas importadas.")
        
        # Botão para ir para a dashboard
        if st.button("🚀 Ir para a Dashboard", type="primary"):
            st.switch_page("pages/0_📊_Dashboard.py")
            
    except Exception as e:
        st.error(f"❌ Erro ao ler o arquivo: {str(e)}")
        
elif st.session_state.df_principal is not None:
    st.info(f"📁 Um arquivo já está carregado: **{st.session_state.nome_arquivo}**")
    if st.button("🔄 Carregar um novo arquivo"):
        st.session_state.df_principal = None
        st.rerun()
    if st.button("📊 Ir para a Dashboard", type="secondary"):
        st.switch_page("pages/0_📊_Dashboard.py")