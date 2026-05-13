import streamlit as st
import pandas as pd
import plotly.express as px

st.title("🏫 Comparação por Tipo de Escola")

# -----------------------------
# CARREGAMENTO
# -----------------------------
df = pd.read_csv("dados/tratado/enem_escola.csv")

# classificação GO vs BR
df["Local"] = df["SG_UF_PROVA"].apply(
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
# FILTROS
# -----------------------------
col1, col2 = st.columns(2)

with col1:
    disciplina = st.selectbox(
        "Disciplina",
        disciplinas
    )

with col2:
    st.write("Comparação: Goiás vs Brasil")

# -----------------------------
# MÉDIAS
# -----------------------------
media = (
    df.groupby(["Local", "Tipo_Escola"])[disciplina]
    .mean()
    .reset_index()
)

# -----------------------------
# TABELA
# -----------------------------
st.subheader("📋 Médias por tipo de escola")

st.dataframe(
    media.round(2),
    use_container_width=True
)

# -----------------------------
# GRÁFICO
# -----------------------------
fig = px.bar(
    media,
    x="Tipo_Escola",
    y=disciplina,
    color="Tipo_Escola",
    facet_col="Local",
    title=f"Média das notas — {disciplina}"
)

fig.update_layout(
    yaxis_title="Nota média",
    xaxis_title="Tipo de escola"
)

st.plotly_chart(fig, use_container_width=True)

# -----------------------------
# ANÁLISE GOIÁS
# -----------------------------
media_go = (
    media[media["Local"] == "Goiás"]
    .set_index("Tipo_Escola")[disciplina]
)

melhor = media_go.idxmax()
pior = media_go.idxmin()

# -----------------------------
# INTERPRETAÇÃO
# -----------------------------
st.markdown("### 📌 Interpretação")

st.write(
    f"Em Goiás, a maior média em {disciplina} foi observada nas escolas "
    f"{melhor}, enquanto a menor média ocorreu nas escolas {pior}."
)

# comparação específica
if (
    "Privada" in media_go.index
    and "Estadual" in media_go.index
):

    diff = media_go["Privada"] - media_go["Estadual"]

    st.write(
        f"A diferença entre escolas privadas e estaduais em Goiás "
        f"é de aproximadamente {diff:.2f} pontos."
    )

st.write("""
Os resultados indicam que o tipo de escola possui forte influência
no desempenho dos participantes do ENEM.

De modo geral, escolas privadas apresentaram médias superiores,
enquanto escolas públicas estaduais e municipais registraram
desempenhos mais baixos.
""")

# -----------------------------
# COMPARAÇÃO GERAL
# -----------------------------
st.markdown("---")

st.subheader("📊 Comparação geral entre os tipos de escola")

fig2 = px.box(
    df,
    x="Tipo_Escola",
    y=disciplina,
    color="Tipo_Escola",
    title=f"Distribuição das notas por tipo de escola — {disciplina}"
)

fig2.update_layout(
    yaxis_title="Nota",
    xaxis_title="Tipo de escola"
)

st.plotly_chart(fig2, use_container_width=True)

st.write("""
O boxplot permite visualizar a dispersão das notas, os quartis
e possíveis valores extremos (outliers) em cada categoria escolar.
""")