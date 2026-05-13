import streamlit as st
import pandas as pd
import plotly.express as px
from utils.load_data import carregar_microdados

st.title("🚫 Notas Zeradas")

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
# DADOS
# -----------------------------
df_go = df[df["Local"] == "Goiás"]
df_br = df[df["Local"] == "Brasil"]

# -----------------------------
# FUNÇÃO
# -----------------------------
@st.cache_data
def calcular_zeros(df_base):

    return (
        (df_base[disciplinas] == 0)
        .mean()
        * 100
    )

zeros_go = calcular_zeros(df_go)
zeros_br = calcular_zeros(df_br)

# -----------------------------
# TABELA
# -----------------------------
tabela = (
    zeros_go.to_frame(name="Goiás")
    .join(
        zeros_br.to_frame(name="Brasil")
    )
    .reset_index()
    .rename(columns={
        "index": "Disciplina"
    })
)

st.subheader("📋 Percentual de notas zeradas — GO vs Brasil")

st.dataframe(
    tabela.round(2),
    use_container_width=True
)

# -----------------------------
# GRÁFICO
# -----------------------------
df_plot = tabela.melt(
    id_vars="Disciplina",
    var_name="Local",
    value_name="% de zeros"
)

fig = px.bar(
    df_plot,
    x="Disciplina",
    y="% de zeros",
    color="Local",
    barmode="group",
    title="Percentual de notas zeradas por disciplina"
)

fig.update_layout(
    yaxis_title="Percentual (%)",
    xaxis_title=""
)

st.plotly_chart(fig, use_container_width=True)

# -----------------------------
# MAIOR E MENOR
# -----------------------------
maior_go = zeros_go.idxmax()
menor_go = zeros_go.idxmin()

# -----------------------------
# INTERPRETAÇÃO
# -----------------------------
st.markdown("### 📌 Interpretação")

st.write(
    f"Em Goiás, a disciplina com maior percentual de notas zeradas foi "
    f"{maior_go}, enquanto {menor_go} apresentou o menor percentual."
)

st.write("""
Percentuais mais elevados de notas zeradas podem indicar maior dificuldade
dos participantes em determinadas áreas do conhecimento.
""")

st.write("""
As notas zeradas foram mantidas na análise por representarem desempenho real
dos candidatos, e não ausência de informação.
""")

st.write("""
A comparação entre Goiás e Brasil permite identificar padrões de desempenho
e possíveis diferenças educacionais entre os grupos analisados.
""")