import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")

# Carrega o DataFrame
df = pd.read_csv("levantamento.csv", sep=";", decimal=",")

# Remove espaços extras dos nomes das colunas
df.columns = df.columns.str.strip()

# Ordena o DataFrame por Status
df = df.sort_values(by="Status")

# Adiciona os filtros na barra lateral
status = st.sidebar.selectbox("Selecione o Status", ["Todos"] + list(df["Status"].unique()))
transportadora = st.sidebar.selectbox("Selecione a Transportadora", ["Todos"] + list(df["Transportadora"].unique()))

# Aplica os filtros apenas se necessário
if status != "Todos":
    df = df[df["Status"] == status]

if transportadora != "Todos":
    df = df[df["Transportadora"] == transportadora]

# Exibe o DataFrame filtrado
st.dataframe(df)

# Criação dos gráficos
col1,  = st.columns(1)
col2,  = st.columns(1)

# Converte a coluna "NFe - Vlr" para numérico (separador decimal ajustado para vírgula)
df["NFe - Vlr"] = df["NFe - Vlr"].str.replace(".", "").str.replace(",", ".").astype(float)

# Calcula o total de faturamento
total_faturamento = df["NFe - Vlr"].sum()

# Atualiza o gráfico com o título contendo o total
fig_prod = px.bar(
    df,
    x="UF Origem",
    y="NFe - Vlr",
    color="Canal",
    title=f"Faturamento por Origem e Canal (Total: R$ {total_faturamento:,.2f})",
    orientation="v",
    barmode="stack"
)
col1.plotly_chart(fig_prod, key="fig_prod")


fig_transportadora = px.pie(
    df,
    names="Transportadora",
    values="NFe - Vlr",
    title="Participação no Faturamento por Transportadora",
    hole=0.4  # Torna o gráfico um doughnut (opcional)
)
col2.plotly_chart(fig_transportadora, key="fig_transportadora")