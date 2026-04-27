import streamlit as st
import plotly.express as px
from utils.load_data import carregar_microdados

st.title("🚫 Notas zeradas")

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

# 🔥 separar automaticamente
df_go = df[df["Local"] == "Goiás"]
df_br = df[df["Local"] == "Brasil"]

@st.cache_data
def calcular_zeros(df_base):
    return (df_base[disciplinas] == 0).mean() * 100

zeros_go = calcular_zeros(df_go)
zeros_br = calcular_zeros(df_br)

# 🔥 tabela comparativa
tabela = (
    zeros_go.to_frame(name="Goiás")
    .join(zeros_br.to_frame(name="Brasil"))
    .reset_index()
    .rename(columns={"index": "Disciplina"})
)

st.subheader("Percentual de notas zeradas — GO vs Brasil")

st.dataframe(tabela.round(2), use_container_width=True)

# 🔥 gráfico interativo
df_plot = tabela.melt(id_vars="Disciplina", var_name="Local", value_name="% de zeros")

fig = px.bar(
    df_plot,
    x="Disciplina",
    y="% de zeros",
    color="Local",
    barmode="group",
    title="Notas zeradas por disciplina (GO vs Brasil)"
)

st.plotly_chart(fig, use_container_width=True)

st.markdown("### 📌 Interpretação")

st.write(
    "A comparação entre Goiás e o Brasil permite identificar quais disciplinas apresentam maior "
    "incidência de notas zeradas."
)

st.write(
    "Percentuais mais elevados indicam maior dificuldade dos alunos ou possíveis problemas na "
    "resolução das provas, destacando áreas que demandam maior atenção educacional."
)