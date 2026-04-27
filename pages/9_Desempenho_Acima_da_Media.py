import streamlit as st
from utils.load_data import carregar_microdados

st.title("📈 Desempenho acima da média")

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
    disciplina = st.selectbox("Escolha a disciplina", disciplinas)

with col2:
    st.write("Comparação: Goiás vs Brasil")

# 🔥 separar automaticamente
df_go = df[df["Local"] == "Goiás"]
df_br = df[df["Local"] == "Brasil"]

def calcular_percentuais(base):
    media = base[disciplina].mean()

    acima_media = base[base[disciplina] >= media]
    acima_100 = base[base[disciplina] >= media + 100]
    acima_200 = base[base[disciplina] >= media + 200]

    total = len(base)

    p1 = len(acima_media) / total * 100
    p2 = len(acima_100) / total * 100
    p3 = len(acima_200) / total * 100

    return p1, p2, p3

# 🔥 calcular GO e BR
p1_go, p2_go, p3_go = calcular_percentuais(df_go)
p1_br, p2_br, p3_br = calcular_percentuais(df_br)

st.subheader(f"Comparação — {disciplina}")

col1, col2, col3 = st.columns(3)

col1.metric("Acima da média", f"{p1_go:.2f}% (GO)", f"{p1_br:.2f}% (BR)")
col2.metric("+100 pontos", f"{p2_go:.2f}% (GO)", f"{p2_br:.2f}% (BR)")
col3.metric("+200 pontos", f"{p3_go:.2f}% (GO)", f"{p3_br:.2f}% (BR)")

st.markdown("### 📌 Interpretação")

st.write(
    f"A comparação entre Goiás e Brasil mostra a proporção de alunos que atingem níveis de desempenho "
    f"acima da média em **{disciplina}**. Observa-se que apenas uma parcela dos estudantes consegue "
    "alcançar resultados significativamente superiores, indicando concentração das notas em níveis intermediários."
)