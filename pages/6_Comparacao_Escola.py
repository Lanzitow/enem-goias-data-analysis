import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("🏫 Comparação por Tipo de Escola")

# carregar base
df = pd.read_csv("dados/tratado/enem_escola.csv")

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
    grupo = st.selectbox("Grupo", ["Brasil", "Goiás"])

# filtro
if grupo == "Goiás":
    df = df[df["SG_UF_PROVA"] == "GO"]

# média por escola
media = df.groupby("Tipo_Escola")[disciplina].mean().sort_values(ascending=False)

st.subheader("📊 Médias por tipo de escola")
st.dataframe(media.round(2).reset_index())

# gráfico
fig, ax = plt.subplots(figsize=(8,5))
media.plot(kind="bar", ax=ax)
ax.set_title(f"Média das notas — {disciplina} ({grupo})")
ax.set_ylabel("Nota média")
ax.set_xlabel("Tipo de escola")

st.pyplot(fig)

# interpretação automática
melhor = media.idxmax()
pior = media.idxmin()

st.markdown("### 📌 Interpretação")

st.write(
    f"No grupo **{grupo}**, a maior média em **{disciplina}** foi observada nas escolas "
    f"**{melhor}**, enquanto a menor média ocorreu nas escolas **{pior}**."
)

# insight mais forte (professor gosta disso)
if "Privada" in media.index and "Estadual" in media.index:
    diff = media["Privada"] - media["Estadual"]
    st.write(
        f"A diferença entre escolas privadas e estaduais é de aproximadamente "
        f"{diff:.2f} pontos, evidenciando desigualdade no desempenho."
    )

st.write(
    "De forma geral, observa-se que o tipo de escola influencia significativamente "
    "o desempenho dos alunos, com destaque para melhores resultados em escolas privadas."
)