import streamlit as st
import pandas as pd
import plotly.express as px

st.title("🏫 Comparação por Tipo de Escola")

# -----------------------------
# CARREGAMENTO
# -----------------------------
df = pd.read_csv(
    "dados/tratado/enem_escola_sample.csv"
)

# -----------------------------
# CLASSIFICAÇÃO GO vs BR
# -----------------------------
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
# FILTRO
# -----------------------------
disciplina = st.selectbox(
    "Disciplina",
    disciplinas
)

# -----------------------------
# MÉDIAS
# -----------------------------
media = (
    df.groupby(
        ["Local", "Tipo_Escola"]
    )[disciplina]
    .mean()
    .reset_index()
)

media[disciplina] = media[
    disciplina
].round(2)

# -----------------------------
# TABELA
# -----------------------------
st.subheader(
    "📋 Médias por tipo de escola — Goiás vs Brasil"
)

st.dataframe(
    media,
    use_container_width=True
)

# -----------------------------
# GRÁFICO
# -----------------------------
fig = px.bar(
    media,
    x="Tipo_Escola",
    y=disciplina,
    color="Local",
    barmode="group",
    title=f"Média das notas em {disciplina} por tipo de escola"
)

fig.update_layout(
    yaxis_title="Nota média",
    xaxis_title="Tipo de escola"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# -----------------------------
# ANÁLISE GO
# -----------------------------
media_go = (
    media[
        media["Local"] == "Goiás"
    ]
    .set_index("Tipo_Escola")[disciplina]
)

melhor = media_go.idxmax()
pior = media_go.idxmin()

# -----------------------------
# INTERPRETAÇÃO
# -----------------------------
st.markdown("### 📌 Interpretação")

st.write(
    f"Em Goiás, o maior desempenho em "
    f"{disciplina} foi observado nas escolas "
    f"{melhor}, enquanto o menor desempenho "
    f"foi identificado nas escolas {pior}."
)

st.write("""
Os resultados mostram que o tipo de escola
possui forte relação com o desempenho dos
participantes no ENEM.
""")

# -----------------------------
# GAP EDUCACIONAL
# -----------------------------
if (
    "Privada" in media_go.index
    and
    "Estadual" in media_go.index
):

    gap_go = (
        media_go["Privada"]
        - media_go["Estadual"]
    )

    st.write(
        f"Em Goiás, a diferença entre escolas "
        f"privadas e estaduais foi de "
        f"{gap_go:.2f} pontos."
    )

# -----------------------------
# COMPARAÇÃO GO vs BR
# -----------------------------
pivot = media.pivot(
    index="Tipo_Escola",
    columns="Local",
    values=disciplina
)

for escola in pivot.index:

    goias = pivot.loc[escola, "Goiás"]
    brasil = pivot.loc[escola, "Brasil"]

    diferenca = goias - brasil

    st.write(
        f"No tipo de escola {escola}, Goiás apresentou "
        f"diferença de {diferenca:.2f} pontos em relação "
        f"à média nacional."
    )

# -----------------------------
# CONCLUSÃO
# -----------------------------
st.write("""
De forma geral, escolas privadas apresentaram
as maiores médias, enquanto redes públicas
obtiveram desempenho inferior em praticamente
todas as disciplinas analisadas.
""")

st.write("""
Essa diferença sugere influência de fatores
estruturais, econômicos e sociais no desempenho
educacional dos participantes.
""")