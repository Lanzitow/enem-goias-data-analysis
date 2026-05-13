import streamlit as st
import plotly.express as px
from utils.load_data import carregar_microdados

st.title("📊 Distribuição das Notas")

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
# FILTRO
# -----------------------------
disciplina = st.selectbox(
    "Escolha a disciplina",
    disciplinas
)

# -----------------------------
# DADOS
# -----------------------------
dados_go = df[df["Local"] == "Goiás"][disciplina]
dados_br = df[df["Local"] == "Brasil"][disciplina]

# -----------------------------
# HISTOGRAMA
# -----------------------------
st.subheader(f"📈 Histograma — {disciplina}")

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
# BOXPLOT
# -----------------------------
st.subheader("📦 Boxplot comparativo")

fig2 = px.box(
    df,
    x="Local",
    y=disciplina,
    color="Local",
    title=f"Boxplot — {disciplina}"
)

fig2.update_layout(
    yaxis_title="Nota",
    xaxis_title=""
)

st.plotly_chart(fig2, use_container_width=True)

# -----------------------------
# MÉTRICAS
# -----------------------------
media_go = dados_go.mean()
media_br = dados_br.mean()

mediana_go = dados_go.median()
mediana_br = dados_br.median()

# -----------------------------
# INTERPRETAÇÃO
# -----------------------------
st.markdown("### 📌 Interpretação automática")

if media_go > media_br:
    st.write(
        f"Em {disciplina}, Goiás apresenta média superior ao Brasil "
        f"({media_go:.2f} contra {media_br:.2f})."
    )

elif media_go < media_br:
    st.write(
        f"Em {disciplina}, Goiás apresenta média inferior ao Brasil "
        f"({media_go:.2f} contra {media_br:.2f})."
    )

else:
    st.write(
        f"As médias de Goiás e Brasil são muito semelhantes em {disciplina}."
    )

st.write(
    f"A mediana de Goiás é {mediana_go:.2f}, enquanto a mediana "
    f"do Brasil é {mediana_br:.2f}."
)

st.write("""
O histograma foi normalizado em percentual para permitir comparação proporcional
entre Goiás e Brasil, evitando distorções causadas pela diferença no tamanho das amostras.
""")

st.write("""
O boxplot permite observar a dispersão das notas, os quartis e possíveis valores extremos
(outliers), auxiliando na compreensão da distribuição dos dados.
""")