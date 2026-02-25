import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime

st.set_page_config(page_title="Sistema de Despesas", layout="wide")

st.title("💰 Sistema de Lançamento de Despesas")

# -------------------------------
# CONEXÃO GOOGLE SHEETS
# -------------------------------

scope = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

credentials = Credentials.from_service_account_info(
    st.secrets["gcp_service_account"],
    scopes=scope
)

client = gspread.authorize(credentials)

# 👇 NOME EXATO DA SUA PLANILHA
SPREADSHEET_NAME = "BASE_DESPESAS_EMPRESA"

sheet = client.open(SPREADSHEET_NAME).sheet1

# -------------------------------
# FORMULÁRIO
# -------------------------------

st.subheader("Novo Lançamento")

col1, col2 = st.columns(2)

with col1:
    data = st.date_input("Data", datetime.today())

with col2:
    categoria = st.selectbox("Categoria", [
        "Combustível",
        "Impostos",
        "Manutenção",
        "Fornecedor",
        "Pessoal",
        "Outros"
    ])

descricao = st.text_input("Despesa")
valor = st.number_input("Valor", min_value=0.0, format="%.2f")

if st.button("Salvar Lançamento"):

    nova_linha = [
        str(data),
        categoria,
        descricao,
        float(valor)
    ]

    sheet.append_row(nova_linha)

    st.success("✅ Lançamento salvo no Google Sheets com sucesso!")
