import streamlit as st
from utils.load_data import carregar_microdados

st.title("⚠️ Alunos em risco")

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
    disciplina = st.selectbox("Disciplina", disciplinas)

with col2:
    grupo = st.selectbox("Grupo", ["Brasil", "Goiás"])

if grupo == "Goiás":
    base = df[df["UF"] == "GO"]
else:
    base = df

limite = 400

df_risco = base[base[disciplina] < limite]

percentual = len(df_risco) / len(base) * 100

st.metric("Alunos em risco", f"{percentual:.2f}%")

st.markdown("### 📌 Interpretação")

st.write(
    f"No grupo **{grupo}**, considerando notas abaixo de {limite}, observa-se que uma parcela "
    f"dos alunos encontra-se em situação de risco em **{disciplina}**, indicando necessidade "
    "de intervenções educacionais."
)