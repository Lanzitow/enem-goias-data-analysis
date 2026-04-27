import streamlit as st
import pandas as pd
import plotly.express as px
from utils.load_data import carregar_microdados

st.title("📊 Análise de Variáveis Categóricas")

df = carregar_microdados()

# 🔥 já existente
df["Local"] = df["UF"].apply(lambda x: "Goiás" if x == "GO" else "Brasil")

# 🔥 NOVA variável categórica (faixa de nota)
disciplina = st.selectbox("Escolha a disciplina", [
    "Linguagens",
    "Matemática",
    "Ciências Humanas",
    "Ciências da Natureza",
    "Redação"
])

# criar faixas
df["Faixa"] = pd.cut(
    df[disciplina],
    bins=[0, 400, 600, 800, 1000],
    labels=["Baixo", "Médio", "Alto", "Muito Alto"]
)

# remover nulos
df = df[df["Faixa"].notna()]

# -------------------
# TABELA
# -------------------
st.subheader("Tabela de Contingência (%)")

tabela = pd.crosstab(df["Local"], df["Faixa"])
tabela_pct = tabela.div(tabela.sum(axis=1), axis=0) * 100

st.dataframe(tabela_pct.round(2), use_container_width=True)

# -------------------
# GRÁFICO
# -------------------
df_plot = df.groupby(["Local", "Faixa"]).size().reset_index(name="qtd")
df_plot["Percentual"] = df_plot.groupby("Local")["qtd"].transform(lambda x: x / x.sum() * 100)

fig = px.bar(
    df_plot,
    x="Local",
    y="Percentual",
    color="Faixa",
    barmode="stack",
    title="Distribuição percentual das faixas de nota (GO vs Brasil)"
)

st.plotly_chart(fig, use_container_width=True)

# -------------------
# INTERPRETAÇÃO
# -------------------
st.markdown("### 📌 Interpretação")

st.write(
    "A análise relaciona duas variáveis categóricas: localização (Goiás/Brasil) e faixa de desempenho. "
    "Isso permite identificar diferenças na distribuição de desempenho entre os grupos."
)

st.markdown("---")
st.subheader("📊 Comparação de Faixas por Disciplina (GO vs Brasil)")

df_melt = df.melt(
    id_vars=["Local"],
    value_vars=[
        "Linguagens",
        "Matemática",
        "Ciências Humanas",
        "Ciências da Natureza",
        "Redação"
    ],
    var_name="Disciplina",
    value_name="Nota"
)

# criar faixa categórica
df_melt["Faixa"] = pd.cut(
    df_melt["Nota"],
    bins=[0, 400, 600, 800, 1000],
    labels=["Baixo", "Médio", "Alto", "Muito Alto"]
)

df_melt = df_melt[df_melt["Faixa"].notna()]

# agrupar com LOCAL
df_plot2 = df_melt.groupby(["Local", "Disciplina", "Faixa"]).size().reset_index(name="qtd")

df_plot2["Percentual"] = df_plot2.groupby(["Local", "Disciplina"])["qtd"] \
    .transform(lambda x: x / x.sum() * 100)

# 🔥 gráfico correto (com GO vs BR)
fig2 = px.bar(
    df_plot2,
    x="Disciplina",
    y="Percentual",
    color="Faixa",
    barmode="stack",
    facet_col="Local",
    title="Distribuição de desempenho por disciplina (GO vs Brasil)"
)

st.plotly_chart(fig2, use_container_width=True)

st.markdown("### 📌 Interpretação adicional")

st.write(
    "A análise permite comparar a distribuição de desempenho entre Goiás e o Brasil em cada disciplina. "
    "Observa-se como as faixas de nota se distribuem dentro de cada grupo, evidenciando possíveis diferenças "
    "entre o desempenho estadual e nacional."
)