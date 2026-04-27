import streamlit as st
import plotly.express as px
from utils.load_data import carregar_microdados

st.title("📊 Distribuição das Notas")

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

disciplina = st.selectbox("Escolha a disciplina", disciplinas)

# 🔥 não separar mais manualmente
dados_go = df[df["Local"] == "Goiás"][disciplina].dropna()
dados_br = df[df["Local"] == "Brasil"][disciplina].dropna()

st.subheader(f"Histograma — {disciplina}")

# 🔥 gráfico interativo
fig = px.histogram(
    df,
    x=disciplina,
    color="Local",
    barmode="overlay",
    nbins=30,
    title=f"Distribuição das notas de {disciplina}"
)

st.plotly_chart(fig, use_container_width=True)

st.subheader("Boxplot comparativo")

# 🔥 boxplot interativo
fig2 = px.box(
    df,
    x="Local",
    y=disciplina,
    color="Local",
    title=f"Boxplot — {disciplina}"
)

st.plotly_chart(fig2, use_container_width=True)

# métricas continuam iguais
media_go = dados_go.mean()
media_br = dados_br.mean()
mediana_go = dados_go.median()
mediana_br = dados_br.median()

st.markdown("### 📌 Interpretação automática")

if media_go > media_br:
    st.write(
        f"Em {disciplina}, Goiás apresenta média superior ao Brasil "
        f"({media_go:.2f} contra {media_br:.2f})."
    )
else:
    st.write(
        f"Em {disciplina}, Goiás apresenta média inferior ao Brasil "
        f"({media_go:.2f} contra {media_br:.2f})."
    )

st.write(
    f"A mediana de Goiás é {mediana_go:.2f}, enquanto a mediana do Brasil é {mediana_br:.2f}."
)

st.write(
    "O histograma interativo permite observar a distribuição das notas, enquanto o boxplot "
    "mostra a dispersão e possíveis diferenças entre Goiás e o Brasil."
)