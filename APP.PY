import streamlit as st
import pandas as pd
import os

st.set_page_config(
    page_title="Sistema de Despesas",
    page_icon="💰",
    layout="wide"
)

# --------------------------
# CSS MODERNO
# --------------------------
st.markdown("""
<style>
.main {
    background-color: #f5f7fa;
}
.block-container {
    padding-top: 2rem;
}
.stButton>button {
    background-color: #1f4e79;
    color: white;
    border-radius: 8px;
    height: 3em;
    width: 100%;
    font-weight: 600;
}
.stButton>button:hover {
    background-color: #163a5c;
}
.card {
    background-color: white;
    padding: 20px;
    border-radius: 12px;
    box-shadow: 0px 4px 15px rgba(0,0,0,0.08);
    margin-bottom: 20px;
}
</style>
""", unsafe_allow_html=True)

st.title("💰 Sistema de Lançamento de Despesas")

# --------------------------
# SESSION STATE
# --------------------------
if "lancamentos" not in st.session_state:
    st.session_state.lancamentos = []

if "data_demanda" not in st.session_state:
    st.session_state.data_demanda = None

if "quantidade_total" not in st.session_state:
    st.session_state.quantidade_total = 0


# --------------------------
# CONFIGURAÇÃO DA DEMANDA
# --------------------------
st.markdown('<div class="card">', unsafe_allow_html=True)
st.subheader("📅 Configuração da Demanda")

col1, col2 = st.columns(2)

with col1:
    data_demanda = st.date_input("Data da Demanda")

with col2:
    quantidade = st.number_input("Quantidade de lançamentos", min_value=1, step=1)

if st.button("🚀 Iniciar Demanda"):
    st.session_state.data_demanda = data_demanda
    st.session_state.quantidade_total = quantidade
    st.session_state.lancamentos = []
    st.success("Demanda iniciada com sucesso!")

st.markdown('</div>', unsafe_allow_html=True)


# --------------------------
# FORMULÁRIO
# --------------------------
if st.session_state.data_demanda:

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("📝 Novo Lançamento")

    categorias = [
        "Impostos", "Aluguel", "Luz", "13º Salário",
        "Acordo Judicial", "Água", "Almoço", "Alvará",
        "Antecipação Salarial", "Auxílio Transporte",
        "Borracharia", "Café Escritório", "Café Rota"
    ]

    col1, col2, col3 = st.columns(3)

    with col1:
        categoria = st.selectbox("Categoria", categorias)

    with col2:
        despesa = st.text_input("Descrição da Despesa")

    with col3:
        valor = st.number_input("Valor (R$)", min_value=0.0, format="%.2f")

    if st.button("➕ Adicionar Lançamento"):
        if len(st.session_state.lancamentos) >= st.session_state.quantidade_total:
            st.error("Limite de lançamentos atingido!")
        else:
            st.session_state.lancamentos.append({
                "Data": st.session_state.data_demanda,
                "Categoria": categoria,
                "Despesa": despesa,
                "Valor": valor
            })
            st.success("Lançamento adicionado!")

    st.markdown('</div>', unsafe_allow_html=True)

    # --------------------------
    # RESUMO
    # --------------------------
    st.markdown('<div class="card">', unsafe_allow_html=True)

    st.subheader("📊 Resumo da Demanda")

    st.write(
        f"Lançamentos: {len(st.session_state.lancamentos)} / {st.session_state.quantidade_total}"
    )

    if st.session_state.lancamentos:
        df_preview = pd.DataFrame(st.session_state.lancamentos)
        total = df_preview["Valor"].sum()

        st.dataframe(df_preview, use_container_width=True)

        st.markdown(f"### 💵 Total da Demanda: R$ {total:,.2f}")

    st.markdown('</div>', unsafe_allow_html=True)

    # --------------------------
    # SALVAR
    # --------------------------
    if len(st.session_state.lancamentos) == st.session_state.quantidade_total:
        if st.button("💾 Salvar Lote em Excel"):
            df_novo = pd.DataFrame(st.session_state.lancamentos)

            arquivo = "base_despesas.xlsx"

            if os.path.exists(arquivo):
                df_existente = pd.read_excel(arquivo)
                df_final = pd.concat([df_existente, df_novo], ignore_index=True)
            else:
                df_final = df_novo

            df_final.to_excel(arquivo, index=False)

            st.success("Dados salvos com sucesso!")

            st.session_state.lancamentos = []
            st.session_state.data_demanda = None
            st.session_state.quantidade_total = 0
            st.experimental_rerun()