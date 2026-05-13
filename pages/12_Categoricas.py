import streamlit as st
import pandas as pd
import plotly.express as px
from utils.load_data import carregar_microdados

st.title("📊 Análise de Variáveis Categóricas")

df = carregar_microdados()

# -----------------------------
# CLASSIFICAÇÃO GO vs BR
# -----------------------------
df["Local"] = df["UF"].apply(
    lambda x: "Goiás" if x == "GO" else "Brasil"
)

disciplinas = [
    "Linguagens",
    "Matemática",
    "Ciências Humanas",
    "Ciências da Natureza",
    "Redação"
]

# -----------------------------
# FILTRO
# -----------------------------
disciplina = st.selectbox(
    "Escolha a disciplina",
    disciplinas
)

# -----------------------------
# CRIAÇÃO DAS FAIXAS
# -----------------------------
df["Faixa"] = pd.cut(
    df[disciplina],
    bins=[0, 400, 600, 800, 1000],
    labels=[
        "Baixo",
        "Médio",
        "Alto",
        "Muito Alto"
    ]
)

# remover nulos
df = df[df["Faixa"].notna()]

# -----------------------------
# TABELA DE CONTINGÊNCIA
# -----------------------------
st.subheader("📋 Tabela de contingência (%)")

tabela = pd.crosstab(
    df["Local"],
    df["Faixa"]
)

tabela_pct = (
    tabela.div(
        tabela.sum(axis=1),
        axis=0
    ) * 100
)

st.dataframe(
    tabela_pct.round(2),
    use_container_width=True
)

# -----------------------------
# GRÁFICO PRINCIPAL
# -----------------------------
df_plot = (
    df.groupby(["Local", "Faixa"])
    .size()
    .reset_index(name="Quantidade")
)

df_plot["Percentual"] = (
    df_plot.groupby("Local")["Quantidade"]
    .transform(lambda x: x / x.sum() * 100)
)

fig = px.bar(
    df_plot,
    x="Local",
    y="Percentual",
    color="Faixa",
    barmode="stack",
    title=f"Distribuição percentual das faixas de nota — {disciplina}"
)

fig.update_layout(
    yaxis_title="Percentual (%)",
    xaxis_title=""
)

st.plotly_chart(fig, use_container_width=True)

# -----------------------------
# INTERPRETAÇÃO
# -----------------------------
st.markdown("### 📌 Interpretação")

st.write("""
A análise relaciona duas variáveis categóricas:
o local (Goiás ou Brasil) e a faixa de desempenho dos participantes.
""")

st.write("""
As faixas foram divididas em:
- Baixo: até 400 pontos
- Médio: entre 400 e 600
- Alto: entre 600 e 800
- Muito Alto: acima de 800 pontos
""")

st.write("""
Essa categorização permite identificar diferenças na distribuição
de desempenho entre Goiás e o cenário nacional.
""")

st.markdown("---")

# -----------------------------
# COMPARAÇÃO POR DISCIPLINA
# -----------------------------
st.subheader("📊 Comparação de faixas por disciplina")

df_melt = df.melt(
    id_vars=["Local"],
    value_vars=disciplinas,
    var_name="Disciplina",
    value_name="Nota"
)

# criação das faixas
df_melt["Faixa"] = pd.cut(
    df_melt["Nota"],
    bins=[0, 400, 600, 800, 1000],
    labels=[
        "Baixo",
        "Médio",
        "Alto",
        "Muito Alto"
    ]
)

df_melt = df_melt[
    df_melt["Faixa"].notna()
]

# agrupamento
df_plot2 = (
    df_melt.groupby(
        ["Local", "Disciplina", "Faixa"]
    )
    .size()
    .reset_index(name="Quantidade")
)

df_plot2["Percentual"] = (
    df_plot2.groupby(
        ["Local", "Disciplina"]
    )["Quantidade"]
    .transform(lambda x: x / x.sum() * 100)
)

# -----------------------------
# GRÁFICO GERAL
# -----------------------------
fig2 = px.bar(
    df_plot2,
    x="Disciplina",
    y="Percentual",
    color="Faixa",
    barmode="stack",
    facet_col="Local",
    title="Distribuição percentual das faixas de desempenho"
)

fig2.update_layout(
    yaxis_title="Percentual (%)",
    xaxis_title=""
)

st.plotly_chart(fig2, use_container_width=True)

# -----------------------------
# INTERPRETAÇÃO FINAL
# -----------------------------
st.markdown("### 📌 Interpretação adicional")

st.write("""
A distribuição percentual permite comparar como os participantes
de Goiás e do Brasil se concentram nas diferentes faixas de desempenho.
""")

st.write("""
As disciplinas apresentam padrões distintos de distribuição,
permitindo identificar áreas com maior concentração de notas baixas
ou maiores proporções de desempenho elevado.
""")

st.write("""
Essa abordagem é útil para análises categóricas e estudos de associação
entre grupos e níveis de desempenho educacional.
""")