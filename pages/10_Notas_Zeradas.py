import streamlit as st
import matplotlib.pyplot as plt
from utils.load_data import carregar_microdados

st.title("🚫 Notas zeradas")

df = carregar_microdados()

disciplinas = [
    "Linguagens",
    "Matemática",
    "Ciências Humanas",
    "Ciências da Natureza",
    "Redação"
]

grupo = st.selectbox("Grupo", ["Brasil", "Goiás"])

if grupo == "Goiás":
    base = df[df["UF"] == "GO"]
else:
    base = df

@st.cache_data
def calcular_zeros(df_base):
    zeros = (df_base[disciplinas] == 0).mean() * 100
    return zeros

zeros = calcular_zeros(base)

st.subheader(f"Percentual de notas zeradas — {grupo}")

st.dataframe(
    zeros.round(2).reset_index().rename(columns={
        "index": "Disciplina",
        0: "% de zeros"
    }),
    use_container_width=True
)

fig, ax = plt.subplots(figsize=(8, 4))
zeros.plot(kind="bar", ax=ax)
ax.set_ylabel("% de zeros")
ax.set_title(f"Notas zeradas por disciplina — {grupo}")
st.pyplot(fig)

st.markdown("### 📌 Interpretação")

st.write(
    f"No grupo **{grupo}**, a análise das notas zeradas permite identificar disciplinas com maior "
    "incidência de desempenho extremamente baixo."
)

st.write(
    "Percentuais mais elevados podem refletir dificuldades de aprendizagem, ausência de resposta "
    "ou maior complexidade em determinadas áreas do conhecimento."
)