# pages/1_📊_Dashboard.py
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# Configuração da página
st.set_page_config(
    page_title="Dashboard de Alunos",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# FUNÇÕES AUXILIARES
# ============================================================================

def aplicar_filtros(df, filtros):
    """Aplica filtros ao DataFrame"""
    df_filtrado = df.copy()
    
    if filtros['docente'] != "Todos":
        df_filtrado = df_filtrado[df_filtrado['Docente'] == filtros['docente']]
    
    if filtros['turma'] != "Todas":
        df_filtrado = df_filtrado[df_filtrado['Turma'] == filtros['turma']]
    
    if filtros['turno'] != "Todos":
        df_filtrado = df_filtrado[df_filtrado['Turno'] == filtros['turno']]
    
    return df_filtrado

def calcular_metricas(df):
    """Calcula métricas principais do dashboard"""
    total_alunos = len(df)
    
    metricas = {
        'total_alunos': total_alunos,
        'taxa_conclusao': 0,
        'frequencia_media': 0,
        'media_notas': 0
    }
    
    if total_alunos > 0:
        if 'Nota Final' in df.columns:
            alunos_com_nota = df['Nota Final'].dropna().count()
            metricas['taxa_conclusao'] = (alunos_com_nota / total_alunos) * 100
            
            if alunos_com_nota > 0:
                metricas['media_notas'] = df['Nota Final'].mean()
        
        if 'Frequência' in df.columns:
            metricas['frequencia_media'] = df['Frequência'].mean()
    
    return metricas

def criar_grafico_pizza(df, coluna, altura=400):
    """Cria gráfico de pizza/donut otimizado para dark mode"""
    contagem = df[coluna].value_counts()
    
    if contagem.empty:
        return None
    
    # Cores que funcionam bem no dark mode
    cores_dark = [
        '#636efa', '#ef553b', '#00cc96', '#ab63fa', '#ffa15a',
        '#19d3f3', '#ff6692', '#b6e880', '#ff97ff', '#fecb52'
    ]
    
    fig = px.pie(
        values=contagem.values,
        names=contagem.index,
        hole=0.4,
        color_discrete_sequence=cores_dark
    )
    
    fig.update_traces(
        textposition='outside',
        textinfo='percent+label',
        textfont_size=11,
        textfont_color='white',
        marker=dict(line=dict(color='#2d2d2d', width=1.5))
    )
    
    fig.update_layout(
        height=altura,
        showlegend=False,
        margin=dict(t=30, b=30, l=30, r=30),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font_color='white'
    )
    
    return fig

def criar_grafico_barras(df, coluna, horizontal=False, top_n=None, altura=400):
    """Cria gráfico de barras otimizado para dark mode"""
    contagem = df[coluna].value_counts()
    
    if top_n:
        contagem = contagem.head(top_n)
    
    if contagem.empty:
        return None
    
    # Cores para dark mode
    cor_barras = '#4CC9F0'  # Azul ciano que fica bem no dark
    cor_texto = 'white'
    
    if horizontal:
        fig = px.bar(
            x=contagem.values,
            y=contagem.index,
            orientation='h',
            color_discrete_sequence=[cor_barras],
            text=contagem.values
        )
        
        fig.update_layout(
            yaxis={'categoryorder': 'total ascending'},
            xaxis_title="Quantidade",
            yaxis_title=coluna
        )
    else:
        fig = px.bar(
            x=contagem.index,
            y=contagem.values,
            color_discrete_sequence=[cor_barras],
            text=contagem.values
        )
        
        fig.update_layout(
            xaxis_title=coluna,
            yaxis_title="Quantidade"
        )
    
    fig.update_traces(
        textposition='outside',
        texttemplate='<b>%{text}</b>',
        textfont_size=11,
        textfont_color=cor_texto,
        marker=dict(
            line=dict(color='#2d2d2d', width=1),
            opacity=0.85
        ),
        hovertemplate="<b>%{x}</b><br>Quantidade: %{y}"
    )
    
    fig.update_layout(
        height=altura,
        showlegend=False,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='white',
        xaxis=dict(
            gridcolor='rgba(128,128,128,0.2)',
            linecolor='rgba(128,128,128,0.2)',
            tickfont_color='white'
        ),
        yaxis=dict(
            gridcolor='rgba(128,128,128,0.2)',
            linecolor='rgba(128,128,128,0.2)',
            tickfont_color='white'
        ),
        margin=dict(t=30, b=50, l=50, r=30)
    )
    
    return fig

# ============================================================================
# CSS PARA DARK MODE
# ============================================================================

st.markdown("""
<style>
    /* Estilos gerais para dark mode */
    .main {
        background-color: #0E1117;
    }
    
    .stApp {
        background-color: #0E1117;
    }
    
    /* KPIs - Cards com fundo escuro e bordas coloridas */
    div[data-testid="stMetric"] {
        background-color: #1E1E1E;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #4CC9F0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
        transition: transform 0.2s;
    }
    
    div[data-testid="stMetric"]:hover {
        transform: translateY(-3px);
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.4);
    }
    
    div[data-testid="stMetric"] label {
        font-weight: bold !important;
        color: #FFFFFF !important;
        font-size: 14px !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    div[data-testid="stMetricValue"] {
        font-size: 32px !important;
        font-weight: bold !important;
        color: #FFFFFF !important;
    }
    
    /* Títulos */
    h1, h2, h3 {
        color: #FFFFFF !important;
    }
    
    /* Sidebar */
    .css-1d391kg {
        background-color: #1E1E1E;
    }
    
    .stSidebar {
        background-color: #1E1E1E;
    }
    
    /* Select boxes e inputs */
    .stSelectbox label, .stNumberInput label {
        color: #FFFFFF !important;
        font-weight: bold;
    }
    
    /* Separadores */
    hr {
        margin: 1.5rem 0;
        border: none;
        height: 1px;
        background: linear-gradient(90deg, #4CC9F0, #F72585);
    }
    
    /* Dataframe */
    .dataframe {
        background-color: #1E1E1E;
        color: white;
    }
    
    /* Botões */
    .stDownloadButton button {
        background-color: #4CC9F0;
        color: black;
        font-weight: bold;
        border: none;
    }
    
    .stDownloadButton button:hover {
        background-color: #3AB8D9;
    }
    
    /* Cards de informações */
    .info-box {
        background-color: #2D2D2D;
        padding: 12px;
        border-radius: 8px;
        margin: 8px 0;
        border-left: 4px solid #4CC9F0;
    }
    
    /* Expandable containers */
    .streamlit-expanderHeader {
        background-color: #2D2D2D;
        color: white !important;
    }
    
    /* Alertas e mensagens */
    .stAlert {
        background-color: #2D2D2D;
        border-left: 4px solid;
    }
    
    .stAlert [data-testid="stMarkdownContainer"] {
        color: white;
    }
    
    /* Tabelas */
    .stDataFrame {
        border: 1px solid #444;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# VERIFICAÇÃO DE DADOS CARREGADOS
# ============================================================================

st.title("Dashboard das Turmas")

# Verificar se os dados foram carregados
if 'df_principal' not in st.session_state or st.session_state.df_principal is None:
    st.warning("⚠️ Nenhum dado encontrado. Por favor, carregue um arquivo na página de Upload.")
    if st.button("📤 Ir para a página de Upload"):
        st.switch_page("Upload.py")
    st.stop()

# Obter dados do session state
df = st.session_state.df_principal
nome_arquivo = st.session_state.get('nome_arquivo', 'Arquivo Carregado')

# Mostrar informações do arquivo
st.sidebar.markdown(f"""
<div class="info-box">
<strong>📁 Arquivo Atual:</strong><br>
<small>{nome_arquivo}</small><br>
<strong>📈 Registros:</strong> {len(df):,}<br>
<strong>📋 Colunas:</strong> {len(df.columns)}
</div>
""", unsafe_allow_html=True)

# ============================================================================
# SIDEBAR - FILTROS
# ============================================================================

st.sidebar.header("🔍 Filtros")

# Verificar se as colunas necessárias existem
colunas_necessarias = ['Docente', 'Turma', 'Turno']
colunas_faltando = [col for col in colunas_necessarias if col not in df.columns]

if colunas_faltando:
    st.sidebar.warning(f"⚠️ Colunas faltando: {', '.join(colunas_faltando)}")

# Filtro de Docente
if 'Docente' in df.columns:
    docentes = ["Todos"] + sorted(df['Docente'].dropna().unique().tolist())
    docente_selecionado = st.sidebar.selectbox("Docente", docentes, key="filtro_docente")
else:
    docente_selecionado = "Todos"

# Filtrar turmas baseado no docente
if docente_selecionado == "Todos":
    df_turmas = df
else:
    df_turmas = df[df['Docente'] == docente_selecionado]

# Filtro de Turma
if 'Turma' in df_turmas.columns:
    turmas = ["Todas"] + sorted(df_turmas['Turma'].dropna().unique().tolist())
    turma_selecionada = st.sidebar.selectbox("Turma", turmas, key="filtro_turma")
else:
    turma_selecionada = "Todas"

# Filtrar turnos baseado no docente e turma
df_turnos = df_turmas.copy()
if turma_selecionada != "Todas" and 'Turma' in df_turnos.columns:
    df_turnos = df_turnos[df_turnos['Turma'] == turma_selecionada]

# Filtro de Turno
if 'Turno' in df_turnos.columns:
    turnos = ["Todos"] + sorted(df_turnos['Turno'].dropna().unique().tolist())
    turno_selecionado = st.sidebar.selectbox("Turno", turnos, key="filtro_turno")
else:
    turno_selecionado = "Todos"

# Coletar filtros
filtros = {
    'docente': docente_selecionado,
    'turma': turma_selecionada,
    'turno': turno_selecionado
}

# Aplicar filtros
df_filtrado = aplicar_filtros(df, filtros)

# ============================================================================
# KPIs PRINCIPAIS
# ============================================================================

st.sidebar.markdown("---")
st.sidebar.subheader("📊 Resumo")
st.sidebar.metric("Alunos Filtrados", len(df_filtrado))

metricas = calcular_metricas(df_filtrado)

# Métricas principais
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("👥 Total de Alunos", metricas['total_alunos'])

with col2:
    st.metric("✅ Conclusão", f"{metricas['taxa_conclusao']:.1f}%")

with col3:
    st.metric("📈 Frequência Média", f"{metricas['frequencia_media']:.1f}%")

with col4:
    valor_nota = f"{metricas['media_notas']:.1f}" if metricas['media_notas'] > 0 else "N/A"
    st.metric("🎯 Média de Notas", valor_nota)

st.markdown("---")

# ============================================================================
# GRÁFICOS PRINCIPAIS
# ============================================================================

# Primeira linha - Situação e Resultado
col1, col2 = st.columns(2)

with col1:
    st.subheader("📋 Situação dos Alunos")
    if 'Situação do Aluno' in df_filtrado.columns:
        fig_situacao = criar_grafico_pizza(df_filtrado, 'Situação do Aluno', 450)
        if fig_situacao:
            st.plotly_chart(fig_situacao, use_container_width=True)
        else:
            st.info("Sem dados para exibir")
    else:
        st.warning("Coluna 'Situação do Aluno' não encontrada")

with col2:
    st.subheader("🎓 Resultado Final")
    if 'Resultado Final' in df_filtrado.columns:
        fig_resultado = criar_grafico_barras(df_filtrado, 'Resultado Final', False, None, 450)
        if fig_resultado:
            st.plotly_chart(fig_resultado, use_container_width=True)
        else:
            st.info("Sem dados para exibir")
    else:
        st.warning("Coluna 'Resultado Final' não encontrada")

st.markdown("---")

# Segunda linha - Turno e Cursos
col1, col2 = st.columns(2)

with col1:
    st.subheader("Alunos por Turno")
    if 'Turno' in df_filtrado.columns:
        fig_turno = criar_grafico_barras(df_filtrado, 'Turno', False, None, 400)
        if fig_turno:
            st.plotly_chart(fig_turno, use_container_width=True)
        else:
            st.info("Sem dados para exibir")
    else:
        st.warning("Coluna 'Turno' não encontrada")

with col2:
    st.subheader("Alunos por Curso")
    if 'Curso' in df_filtrado.columns:
        fig_curso = criar_grafico_barras(df_filtrado, 'Curso', True, 10, 400)
        if fig_curso:
            st.plotly_chart(fig_curso, use_container_width=True)
        else:
            st.info("Sem dados para exibir")
    else:
        st.warning("Coluna 'Curso' não encontrada")

st.markdown("---")

# ============================================================================
# TABELA DE DADOS
# ============================================================================

st.subheader("Relatório de Alunos")

if not df_filtrado.empty:
    # Selecionar e formatar colunas para exibição
    colunas_exibicao = ['Nome', 'Turma', 'Curso', 'Docente', 'Turno', 
                       'Frequência', 'Nota Final', 'Resultado Final', 'Situação do Aluno']
    
    # Filtrar colunas existentes
    colunas_disponiveis = [col for col in colunas_exibicao if col in df_filtrado.columns]
    
    if colunas_disponiveis:
        df_exibir = df_filtrado[colunas_disponiveis].copy()
        
        # Formatar valores numéricos
        if 'Frequência' in df_exibir.columns:
            df_exibir['Frequência'] = df_exibir['Frequência'].apply(lambda x: f"{x:.1f}%" if pd.notnull(x) else "-")
        
        if 'Nota Final' in df_exibir.columns:
            df_exibir['Nota Final'] = df_exibir['Nota Final'].apply(lambda x: f"{x:.1f}" if pd.notnull(x) else "-")
        
        # Exibir tabela
        st.dataframe(
            df_exibir,
            use_container_width=True,
            height=350,
            hide_index=True
        )
        
        # Botão de download
        csv = df_exibir.to_csv(index=False).encode('utf-8')
        
        nome_arquivo = f"dados_alunos_{datetime.now().strftime('%Y%m%d_%H%M')}"
        if docente_selecionado != "Todos":
            nome_arquivo += f"_{docente_selecionado.replace(' ', '_')}"
        if turma_selecionada != "Todas":
            nome_arquivo += f"_{turma_selecionada.replace(' ', '_')}"
        
        nome_arquivo += ".csv"
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.download_button(
                label="📥 Download CSV",
                data=csv,
                file_name=nome_arquivo,
                mime="text/csv",
                use_container_width=True
            )
    else:
        st.warning("Nenhuma coluna disponível para exibição")
else:
    st.info("Nenhum dado encontrado com os filtros atuais")

# ============================================================================
# BOTÃO PARA VOLTAR AO UPLOAD
# ============================================================================

st.sidebar.markdown("---")
if st.sidebar.button("📁 Carregar Novo Arquivo", type="primary"):
    st.session_state.df_principal = None
    st.session_state.nome_arquivo = ''
    st.switch_page("pages/0_📤_Upload.py")

# ============================================================================
# RODAPÉ
# ============================================================================

st.markdown("---")
st.markdown(
    f"""
    <div style='text-align: center; color: #888; padding: 20px; font-size: 14px;'>
        Dashboard Educacional • Arquivo: {nome_arquivo} • 
        Dados atualizados em {datetime.now().strftime("%d/%m/%Y %H:%M")}
    </div>
    """,
    unsafe_allow_html=True
)