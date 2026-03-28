import streamlit as st
from utils.load_data import carregar_microdados

st.title("📈 Desempenho acima da média")

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
    grupo = st.selectbox("Grupo", ["Brasil", "Goiás"])

if grupo == "Goiás":
    base = df[df["UF"] == "GO"].copy()
else:
    base = df.copy()

media = base[disciplina].mean()

acima_media = base[base[disciplina] >= media]
acima_100 = base[base[disciplina] >= media + 100]
acima_200 = base[base[disciplina] >= media + 200]

total = len(base)

p1 = len(acima_media) / total * 100
p2 = len(acima_100) / total * 100
p3 = len(acima_200) / total * 100

col1, col2, col3 = st.columns(3)

col1.metric("Acima da média", f"{p1:.2f}%")
col2.metric("+100 pontos", f"{p2:.2f}%")
col3.metric("+200 pontos", f"{p3:.2f}%")

st.markdown("### 📌 Interpretação")

st.write(
    f"No grupo **{grupo}**, observa-se que apenas uma parcela dos alunos consegue atingir desempenho "
    f"significativamente acima da média em **{disciplina}**, o que indica concentração dos resultados "
    "em níveis intermediários."
)