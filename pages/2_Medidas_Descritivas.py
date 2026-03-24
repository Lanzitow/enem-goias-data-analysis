import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from utils.load_data import carregar_microdados

st.set_page_config(page_title="Medidas Descritivas", layout="wide")

st.title("📐 Medidas Descritivas")

df = carregar_microdados()

disciplinas = [
    "Linguagens",
    "Matemática",
    "Ciências Humanas",
    "Ciências da Natureza",
    "Redação"
]

col1, col2 = st.columns(2)

with col1:
    disciplina = st.selectbox("Escolha a disciplina", disciplinas)

with col2:
    grupo = st.selectbox("Grupo analisado", ["Brasil", "Goiás"])

if grupo == "Goiás":
    dados = df[df["UF"] == "GO"][disciplina].dropna()
else:
    dados = df[disciplina].dropna()

media = dados.mean()
mediana = dados.median()
desvio = dados.std()
minimo = dados.min()
maximo = dados.max()
q1 = dados.quantile(0.25)
q3 = dados.quantile(0.75)

st.subheader(f"Resumo estatístico — {disciplina} ({grupo})")

c1, c2, c3 = st.columns(3)
c1.metric("Média", f"{media:.2f}")
c2.metric("Mediana", f"{mediana:.2f}")
c3.metric("Desvio padrão", f"{desvio:.2f}")

c4, c5, c6, c7 = st.columns(4)
c4.metric("Mínimo", f"{minimo:.2f}")
c5.metric("Q1 (25%)", f"{q1:.2f}")
c6.metric("Q3 (75%)", f"{q3:.2f}")
c7.metric("Máximo", f"{maximo:.2f}")

resumo = pd.DataFrame({
    "Medida": [
        "Média",
        "Mediana",
        "Desvio padrão",
        "Mínimo",
        "1º quartil (Q1)",
        "3º quartil (Q3)",
        "Máximo"
    ],
    "Valor": [media, mediana, desvio, minimo, q1, q3, maximo]
})

st.dataframe(resumo, use_container_width=True)

st.markdown("### Histograma")

fig, ax = plt.subplots(figsize=(9, 4))
ax.hist(dados, bins=30)
ax.set_title(f"Distribuição das notas — {disciplina} ({grupo})")
ax.set_xlabel("Nota")
ax.set_ylabel("Frequência")
st.pyplot(fig)

st.markdown("### 📌 Interpretação automática")

if media > mediana:
    st.write(
        "A média está acima da mediana, sugerindo assimetria à direita. "
        "Isso indica que algumas notas mais altas podem estar puxando a média para cima."
    )
elif media < mediana:
    st.write(
        "A média está abaixo da mediana, sugerindo assimetria à esquerda."
    )
else:
    st.write(
        "A média e a mediana são praticamente iguais, indicando uma distribuição mais equilibrada."
    )

st.write(
    f"O desvio padrão de {desvio:.2f} mostra o nível de dispersão das notas em torno da média."
)