import streamlit as st
import pandas as pd
import plotly.express as px
from utils.load_data import carregar_microdados

st.set_page_config(page_title="Medidas Descritivas", layout="wide")

st.title("📐 Medidas Descritivas")

df = carregar_microdados()

# classificação GO vs BR
df["Local"] = df["UF"].apply(
    lambda x: "Goiás" if x == "GO" else "Brasil"
)

disciplinas = [
    "Linguagens",
    "Matemática",
    "Ciências Humanas",
    "Ciências da Natureza",
    "Redação"
]

# -----------------------------
# FILTROS
# -----------------------------
col1, col2 = st.columns(2)

with col1:
    disciplina = st.selectbox(
        "Escolha a disciplina",
        disciplinas
    )

with col2:
    st.write("Comparação: Goiás vs Brasil")

# -----------------------------
# DADOS
# -----------------------------
dados_go = df[df["Local"] == "Goiás"][disciplina]
dados_br = df[df["Local"] == "Brasil"][disciplina]

# -----------------------------
# MEDIDAS
# -----------------------------
media_go = dados_go.mean()
media_br = dados_br.mean()

mediana_go = dados_go.median()
mediana_br = dados_br.median()

desvio_go = dados_go.std()
desvio_br = dados_br.std()

# -----------------------------
# MÉTRICAS
# -----------------------------
st.subheader(f"Resumo estatístico — {disciplina}")

c1, c2, c3 = st.columns(3)

c1.metric("Média (GO)", f"{media_go:.2f}")
c2.metric("Média (BR)", f"{media_br:.2f}")
c3.metric("Diferença", f"{(media_go - media_br):.2f}")

c4, c5, c6 = st.columns(3)

c4.metric("Mediana (GO)", f"{mediana_go:.2f}")
c5.metric("Mediana (BR)", f"{mediana_br:.2f}")
c6.metric("Desvio padrão (GO)", f"{desvio_go:.2f}")

# -----------------------------
# TABELA
# -----------------------------
resumo = pd.DataFrame({
    "Medida": [
        "Média",
        "Mediana",
        "Desvio padrão"
    ],
    "Goiás": [
        round(media_go, 2),
        round(mediana_go, 2),
        round(desvio_go, 2)
    ],
    "Brasil": [
        round(media_br, 2),
        round(mediana_br, 2),
        round(desvio_br, 2)
    ]
})

st.dataframe(resumo, use_container_width=True)

# -----------------------------
# HISTOGRAMA
# -----------------------------
st.markdown("### 📊 Distribuição das notas")

fig = px.histogram(
    df,
    x=disciplina,
    color="Local",
    histnorm="percent",
    barmode="overlay",
    nbins=30,
    opacity=0.6,
    title=f"Distribuição percentual das notas — {disciplina}"
)

fig.update_layout(
    yaxis_title="Percentual (%)",
    xaxis_title="Nota"
)

st.plotly_chart(fig, use_container_width=True)

# -----------------------------
# INTERPRETAÇÃO
# -----------------------------
st.markdown("### 📌 Interpretação automática")

if media_go > media_br:
    st.write(
        f"A média de Goiás ({media_go:.2f}) está acima da média nacional "
        f"({media_br:.2f}), indicando desempenho superior nessa disciplina."
    )

elif media_go < media_br:
    st.write(
        f"A média de Goiás ({media_go:.2f}) está abaixo da média nacional "
        f"({media_br:.2f})."
    )

else:
    st.write(
        "As médias de Goiás e Brasil são praticamente equivalentes."
    )

st.write(
    f"O desvio padrão em Goiás ({desvio_go:.2f}) indica o nível de dispersão "
    f"das notas em relação à média."
)

st.write("""
Os histogramas foram normalizados em percentual para permitir comparação
proporcional entre Goiás e Brasil, evitando distorções causadas pela
diferença de tamanho das amostras.
""")