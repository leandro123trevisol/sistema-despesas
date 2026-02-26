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

SPREADSHEET_NAME = "BASE_DESPESAS_EMPRESA"
sheet = client.open(SPREADSHEET_NAME).sheet1

# -------------------------------
# CONFIGURAÇÃO DA DEMANDA
# -------------------------------

st.header("📋 Configuração da Demanda")

col1, col2 = st.columns(2)

with col1:
    data_demanda = st.date_input("Data da Demanda", datetime.today())

with col2:
    qtd_lancamentos = st.number_input(
        "Quantidade de lançamentos",
        min_value=1,
        max_value=50,
        value=1
    )

if st.button("🚀 Iniciar Demanda"):
    st.session_state.iniciar_demanda = True
    st.session_state.qtd = qtd_lancamentos
    st.session_state.data = data_demanda

# -------------------------------
# FORMULÁRIO DINÂMICO
# -------------------------------

if "iniciar_demanda" in st.session_state and st.session_state.iniciar_demanda:

    st.header("📝 Lançamentos")

    total_demanda = 0

    for i in range(st.session_state.qtd):

        st.subheader(f"Lançamento {i+1}")

        col1, col2 = st.columns(2)

        with col1:
            categoria = st.selectbox(
                f"Categoria",
                [
                    "Combustível - Diesel",
                    "Combustível - Gasolina",
                    "Impostos",
                    "Aluguel",
                    "Luz",
                    "13° Salário",
                    "Acordo Judicial",
                    "Aferição de Tacógrafo/GuiasInmetro",
                    "Água",
                    "Almoço",
                    "Alvará",
                    "Antecipação Salarial",
                    "ASO - Admissinal",
                    "ASO - Demissional",
                    "Auxílio Trasnporte",
                    "Avarias/Pagamentos de Produtos em Rota",
                    "Borracharia",
                    "Café Escritório",
                    "Café Rota",
                    "Cartão Crédito Empresa",
                    "Cartório",
                    "Cesta Básica",
                    "Conserto Celular",
                    "Conserto Chave",
                    "Conserto Sider",
                    "Contribuição Sindical",
                    "Descarga/Empilhadeira",
                    "Despachante",
                    "Doação",
                    "Documentos Caminhões",
                    "Elétrica",
                    "Empréstimos",
                    "Energia",
                    "EPI - Equipamento de Proteção Individual",
                    "Exame Toxicológico",
                    "F1 - Cobrança de Produtos/FEMSA",
                    "Férias",
                    "Filmes/Plástico/Strech",
                    "Financiamento",
                    "Folha de Pagamento",
                    "Fretes",
                    "Gás Empilhadeira",
                    "Guincho",
                    "Honorários Advocatícios",
                    "Honorários Contabilidade",
                    "Imposto",
                    "Internet/Telefonia",
                    "Investimentos",
                    "Janta/Rota",
                    "Lavação",
                    "Licença - Estrada do Mar",
                    "Limpeza Galpão",
                    "Mecânica",
                    "Mecânica - Empilhadeira",
                    "Multa de Trânsito",
                    "Multa de Recisória",
                    "Peças de Caminhão",
                    "Pedágio",
                    "Pensão Alimentícia",
                    "Perícias",
                    "Pneu",
                    "Prêmio Verão",
                    "Presentes Endomarketing",
                    "Produto Limpeza",
                    "Pró Labore",
                    "Relógio Ponto"
                    "Revisão",
                    "Segurança do Trabalho/eSocial",
                    "Seguros",
                    "Serviços Financeiros",
                    "Serviços Informática",
                    "Serviços Patrimoniais",
                    "Termo de Recisão de Contrato de Trabalho - TRCT",
                    "Teste de Fuligem",
                    "Uniformes",
                    "Vale Alimentação",
                    "Vale Refeição",
                    "Vales",
                    "Verbas Advocatícias",
                    "Vigilância",
                    "Vistoria Inmetro"
                ],
                key=f"categoria_{i}"
            )

        with col2:
            valor = st.number_input(
                f"Valor",
                min_value=0.0,
                format="%.2f",
                key=f"valor_{i}"
            )

        descricao = st.text_input(
            f"Despesa",
            key=f"descricao_{i}"
        )

        total_demanda += valor

    st.markdown(f"### 💵 Total da Demanda: R$ {total_demanda:,.2f}")

    if st.button("💾 Salvar Todos os Lançamentos"):

        for i in range(st.session_state.qtd):

            categoria = st.session_state[f"categoria_{i}"]
            valor = st.session_state[f"valor_{i}"]
            descricao = st.session_state[f"descricao_{i}"]

            nova_linha = [
                str(st.session_state.data),
                categoria,
                descricao,
                float(valor)
            ]

            sheet.append_row(nova_linha)

        st.success("✅ Todos os lançamentos foram salvos com sucesso!")

        st.session_state.iniciar_demanda = False
        st.rerun()


