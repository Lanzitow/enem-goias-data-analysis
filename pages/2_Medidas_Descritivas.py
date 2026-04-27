import streamlit as st
import pandas as pd
import plotly.express as px
from utils.load_data import carregar_microdados

st.set_page_config(page_title="Medidas Descritivas", layout="wide")

st.title("📐 Medidas Descritivas")

df = carregar_microdados()

# 🔥 NOVO: coluna GO vs BR
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

# ❌ removido seletor de grupo
with col2:
    st.write("Comparação: Goiás vs Brasil")

# 🔥 separar automaticamente
dados_go = df[df["Local"] == "Goiás"][disciplina].dropna()
dados_br = df[df["Local"] == "Brasil"][disciplina].dropna()

# 🔥 métricas separadas
media_go, media_br = dados_go.mean(), dados_br.mean()
mediana_go, mediana_br = dados_go.median(), dados_br.median()
desvio_go, desvio_br = dados_go.std(), dados_br.std()

st.subheader(f"Resumo estatístico — {disciplina} (GO vs Brasil)")

c1, c2, c3 = st.columns(3)
c1.metric("Média (GO)", f"{media_go:.2f}")
c2.metric("Média (BR)", f"{media_br:.2f}")
c3.metric("Diferença", f"{(media_go - media_br):.2f}")

c4, c5, c6 = st.columns(3)
c4.metric("Mediana (GO)", f"{mediana_go:.2f}")
c5.metric("Mediana (BR)", f"{mediana_br:.2f}")
c6.metric("Desvio (GO)", f"{desvio_go:.2f}")

# 🔥 tabela comparativa
resumo = pd.DataFrame({
    "Medida": ["Média", "Mediana", "Desvio padrão"],
    "Goiás": [media_go, mediana_go, desvio_go],
    "Brasil": [media_br, mediana_br, desvio_br]
})

st.dataframe(resumo, use_container_width=True)

st.markdown("### Histograma Interativo")

# 🔥 gráfico interativo
fig = px.histogram(
    df,
    x=disciplina,
    color="Local",
    barmode="overlay",
    nbins=30,
    title=f"Distribuição das notas — {disciplina} (GO vs Brasil)"
)

st.plotly_chart(fig, use_container_width=True)

st.markdown("### 📌 Interpretação automática")

if media_go > media_br:
    st.write(
        "A média em Goiás está acima da média do Brasil, indicando desempenho superior nesse grupo."
    )
elif media_go < media_br:
    st.write(
        "A média em Goiás está abaixo da média do Brasil."
    )
else:
    st.write(
        "As médias são semelhantes entre Goiás e Brasil."
    )

st.write(
    f"O desvio padrão em Goiás ({desvio_go:.2f}) e no Brasil ({desvio_br:.2f}) mostra o nível de dispersão das notas."
)