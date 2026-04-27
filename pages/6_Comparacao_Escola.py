import streamlit as st
import pandas as pd
import plotly.express as px

st.title("🏫 Comparação por Tipo de Escola")

# carregar base
df = pd.read_csv("dados/tratado/enem_escola_sample.csv")

# 🔥 NOVO: GO vs BR juntos
df["Local"] = df["SG_UF_PROVA"].apply(lambda x: "Goiás" if x == "GO" else "Brasil")

disciplinas = [
    "Linguagens",
    "Matemática",
    "Ciências Humanas",
    "Ciências da Natureza",
    "Redação"
]

col1, col2 = st.columns(2)

with col1:
    disciplina = st.selectbox("Disciplina", disciplinas)

with col2:
    st.write("Comparação: Goiás vs Brasil")

# 🔥 média por escola + local
media = df.groupby(["Local", "Tipo_Escola"])[disciplina].mean().reset_index()

st.subheader("📊 Médias por tipo de escola")

st.dataframe(media.round(2), use_container_width=True)

# 🔥 gráfico interativo
fig = px.bar(
    media,
    x="Tipo_Escola",
    y=disciplina,
    color="Tipo_Escola",
    facet_col="Local",
    title=f"Média das notas — {disciplina} (GO vs Brasil)"
)

st.plotly_chart(fig, use_container_width=True)

# 🔥 interpretação (usando GO como referência principal)
media_go = media[media["Local"] == "Goiás"].set_index("Tipo_Escola")[disciplina]

melhor = media_go.idxmax()
pior = media_go.idxmin()

st.markdown("### 📌 Interpretação")

st.write(
    f"Em **Goiás**, a maior média em **{disciplina}** foi observada nas escolas "
    f"**{melhor}**, enquanto a menor média ocorreu nas escolas **{pior}**."
)

# insight mais forte
if "Privada" in media_go.index and "Estadual" in media_go.index:
    diff = media_go["Privada"] - media_go["Estadual"]
    st.write(
        f"A diferença entre escolas privadas e estaduais em Goiás é de aproximadamente "
        f"{diff:.2f} pontos, evidenciando desigualdade no desempenho."
    )

st.write(
    "De forma geral, observa-se que o tipo de escola influencia significativamente "
    "o desempenho dos alunos, com destaque para melhores resultados em escolas privadas."
)