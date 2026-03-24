import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Análise ENEM GO vs Brasil",
    page_icon="📊",
    layout="wide"
)

@st.cache_data
def carregar_dados():
    df = pd.read_csv("notebooks/comparacao_go_br.csv")

    mapa = {
        "NU_NOTA_LC": "Linguagens",
        "NU_NOTA_MT": "Matemática",
        "NU_NOTA_CH": "Ciências Humanas",
        "NU_NOTA_CN": "Ciências da Natureza",
        "NU_NOTA_REDACAO": "Redação"
    }

    if "index" in df.columns:
        df["Disciplina"] = df["index"].map(mapa)
    else:
        df["Disciplina"] = df.iloc[:, 0].map(mapa)

    return df

df = carregar_dados()

st.title("📊 Análise ENEM 2024: Goiás vs Brasil")
st.markdown("""
Este painel apresenta uma comparação das médias do ENEM 2024 entre Goiás e o Brasil,
considerando as cinco áreas avaliadas.
""")

st.subheader("Visão geral da comparação")
st.dataframe(
    df[["Disciplina", "Média_GO", "Média_BR", "Diferença", "Diferença_%"]],
    use_container_width=True
)

melhor_go = df.loc[df["Diferença"].idxmax()]
pior_go = df.loc[df["Diferença"].idxmin()]

col1, col2 = st.columns(2)
col1.metric("Maior vantagem de Goiás", melhor_go["Disciplina"], f'{melhor_go["Diferença"]:.2f} pontos')
col2.metric("Maior desvantagem de Goiás", pior_go["Disciplina"], f'{pior_go["Diferença"]:.2f} pontos')

st.markdown("---")
st.subheader("Comparação por disciplina")

disciplina = st.selectbox("Escolha a disciplina", df["Disciplina"].tolist())

linha = df[df["Disciplina"] == disciplina].iloc[0]

col1, col2, col3 = st.columns(3)
col1.metric("Média Goiás", f'{linha["Média_GO"]:.2f}')
col2.metric("Média Brasil", f'{linha["Média_BR"]:.2f}')
col3.metric("Diferença", f'{linha["Diferença"]:.2f}', f'{linha["Diferença_%"]:.2f}%')

fig, ax = plt.subplots(figsize=(7, 4))
ax.bar(["Goiás", "Brasil"], [linha["Média_GO"], linha["Média_BR"]])
ax.set_title(f"Comparação das médias - {disciplina}")
ax.set_ylabel("Nota média")
st.pyplot(fig)

st.markdown("### Interpretação automática")
if linha["Diferença"] > 0:
    st.success(
        f"Em {disciplina}, Goiás ficou acima da média nacional em "
        f'{linha["Diferença"]:.2f} pontos ({linha["Diferença_%"]:.2f}%).'
    )
else:
    st.warning(
        f"Em {disciplina}, Goiás ficou abaixo da média nacional em "
        f'{abs(linha["Diferença"]):.2f} pontos ({abs(linha["Diferença_%"]):.2f}%).'
    )

st.markdown("---")
st.subheader("Comparação geral entre todas as disciplinas")

fig2, ax2 = plt.subplots(figsize=(10, 5))
x = range(len(df))
largura = 0.35

ax2.bar([i - largura/2 for i in x], df["Média_GO"], width=largura, label="Goiás")
ax2.bar([i + largura/2 for i in x], df["Média_BR"], width=largura, label="Brasil")

ax2.set_xticks(list(x))
ax2.set_xticklabels(df["Disciplina"], rotation=15)
ax2.set_ylabel("Nota média")
ax2.set_title("Médias por disciplina: Goiás vs Brasil")
ax2.legend()

st.pyplot(fig2)

st.markdown("### Principais conclusões")
st.write(
    f"Goiás teve seu melhor resultado relativo em **{melhor_go['Disciplina']}**, "
    f"com diferença de **{melhor_go['Diferença']:.2f} pontos** em relação ao Brasil."
)
st.write(
    f"A maior desvantagem apareceu em **{pior_go['Disciplina']}**, "
    f"com diferença de **{pior_go['Diferença']:.2f} pontos**."
)
st.write(
    "Pelos dados analisados, o principal destaque positivo de Goiás está em Redação, "
    "enquanto em algumas áreas a diferença para a média nacional é pequena, mostrando um comportamento relativamente próximo ao cenário brasileiro."
)

st.markdown("---")
st.subheader("🏆 Ranking das disciplinas (diferença GO vs Brasil)")

df_sorted = df.sort_values("Diferença", ascending=False)

st.dataframe(df_sorted[["Disciplina", "Diferença"]])
