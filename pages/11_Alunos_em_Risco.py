import streamlit as st
from utils.load_data import carregar_microdados

st.title("⚠️ Alunos em risco")

df = carregar_microdados()

# 🔥 NOVO
df["Local"] = df["UF"].apply(lambda x: "Goiás" if x == "GO" else "Brasil")

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

# 🔥 separar automaticamente
df_go = df[df["Local"] == "Goiás"]
df_br = df[df["Local"] == "Brasil"]

limite = 400

def calcular_risco(base):
    df_risco = base[base[disciplina] < limite]
    percentual = len(df_risco) / len(base) * 100
    return percentual

# 🔥 calcular GO e BR
risco_go = calcular_risco(df_go)
risco_br = calcular_risco(df_br)

st.subheader(f"Alunos em risco — {disciplina}")

col1, col2 = st.columns(2)

col1.metric("Goiás", f"{risco_go:.2f}%")
col2.metric("Brasil", f"{risco_br:.2f}%")

st.markdown("### 📌 Interpretação")

st.write(
    f"A comparação entre Goiás e o Brasil mostra a proporção de alunos com notas abaixo de {limite} "
    f"em **{disciplina}**, caracterizando situação de risco educacional."
)

st.write(
    "Percentuais mais elevados indicam maior concentração de alunos com baixo desempenho, "
    "sugerindo necessidade de intervenções educacionais."
)