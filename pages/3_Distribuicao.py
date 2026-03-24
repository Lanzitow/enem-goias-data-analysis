import streamlit as st
import matplotlib.pyplot as plt
from utils.load_data import carregar_microdados

st.title("📊 Distribuição das Notas")

df = carregar_microdados()

disciplinas = [
    "Linguagens",
    "Matemática",
    "Ciências Humanas",
    "Ciências da Natureza",
    "Redação"
]

disciplina = st.selectbox("Escolha a disciplina", disciplinas)

col1, col2 = st.columns(2)

with col1:
    dados_go = df[df["UF"] == "GO"][disciplina].dropna()

with col2:
    dados_br = df[disciplina].dropna()

st.subheader(f"Histograma — {disciplina}")

fig, ax = plt.subplots(figsize=(10, 5))
ax.hist(dados_br, bins=30, alpha=0.6, label="Brasil")
ax.hist(dados_go, bins=30, alpha=0.6, label="Goiás")
ax.set_title(f"Distribuição das notas de {disciplina}")
ax.set_xlabel("Nota")
ax.set_ylabel("Frequência")
ax.legend()

st.pyplot(fig)

st.subheader("Boxplot comparativo")

fig2, ax2 = plt.subplots(figsize=(8, 5))
ax2.boxplot([dados_go, dados_br], labels=["Goiás", "Brasil"])
ax2.set_title(f"Boxplot — {disciplina}")
ax2.set_ylabel("Nota")

st.pyplot(fig2)

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
    "O histograma permite observar a concentração das notas, enquanto o boxplot ajuda a visualizar "
    "dispersão, amplitude e possíveis diferenças na distribuição entre Goiás e Brasil."
)