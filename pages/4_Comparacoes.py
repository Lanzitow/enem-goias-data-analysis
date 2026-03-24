import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from utils.load_data import carregar_microdados

st.title("📊 Comparações: Goiás vs Brasil")

df = carregar_microdados()

disciplinas = [
    "Linguagens",
    "Matemática",
    "Ciências Humanas",
    "Ciências da Natureza",
    "Redação"
]

# Separando bases
df_go = df[df["UF"] == "GO"].copy()
df_br = df.copy()

# Montando tabela comparativa
resultados = []

for disciplina in disciplinas:
    media_go = df_go[disciplina].mean()
    media_br = df_br[disciplina].mean()
    diferenca = media_go - media_br
    diferenca_pct = (diferenca / media_br) * 100

    resultados.append({
        "Disciplina": disciplina,
        "Média_GO": media_go,
        "Média_BR": media_br,
        "Diferença": diferenca,
        "Diferença_%": diferenca_pct
    })

comparacao = pd.DataFrame(resultados)

st.subheader("Tabela comparativa")
st.dataframe(
    comparacao.style.format({
        "Média_GO": "{:.2f}",
        "Média_BR": "{:.2f}",
        "Diferença": "{:.2f}",
        "Diferença_%": "{:.2f}"
    }),
    use_container_width=True
)

# Destaques
melhor = comparacao.loc[comparacao["Diferença"].idxmax()]
pior = comparacao.loc[comparacao["Diferença"].idxmin()]

col1, col2 = st.columns(2)
col1.metric(
    "Maior vantagem de Goiás",
    melhor["Disciplina"],
    f'{melhor["Diferença"]:.2f} pontos'
)
col2.metric(
    "Maior desvantagem de Goiás",
    pior["Disciplina"],
    f'{pior["Diferença"]:.2f} pontos'
)

st.markdown("---")
st.subheader("Comparação por disciplina")

disciplina_escolhida = st.selectbox("Escolha a disciplina", disciplinas)

linha = comparacao[comparacao["Disciplina"] == disciplina_escolhida].iloc[0]

c1, c2, c3 = st.columns(3)
c1.metric("Média Goiás", f'{linha["Média_GO"]:.2f}')
c2.metric("Média Brasil", f'{linha["Média_BR"]:.2f}')
c3.metric("Diferença", f'{linha["Diferença"]:.2f}', f'{linha["Diferença_%"]:.2f}%')

fig, ax = plt.subplots(figsize=(7, 4))
ax.bar(["Goiás", "Brasil"], [linha["Média_GO"], linha["Média_BR"]])
ax.set_title(f"Comparação das médias - {disciplina_escolhida}")
ax.set_ylabel("Nota média")
st.pyplot(fig)

st.markdown("### 📌 Interpretação automática")

if linha["Diferença"] > 0:
    st.success(
        f"Em {disciplina_escolhida}, Goiás ficou acima da média nacional em "
        f'{linha["Diferença"]:.2f} pontos ({linha["Diferença_%"]:.2f}%).'
    )
else:
    st.warning(
        f"Em {disciplina_escolhida}, Goiás ficou abaixo da média nacional em "
        f'{abs(linha["Diferença"]):.2f} pontos ({abs(linha["Diferença_%"]):.2f}%).'
    )

st.markdown("---")
st.subheader("Comparação geral entre todas as disciplinas")

fig2, ax2 = plt.subplots(figsize=(10, 5))
x = range(len(comparacao))
largura = 0.35

ax2.bar([i - largura/2 for i in x], comparacao["Média_GO"], width=largura, label="Goiás")
ax2.bar([i + largura/2 for i in x], comparacao["Média_BR"], width=largura, label="Brasil")

ax2.set_xticks(list(x))
ax2.set_xticklabels(comparacao["Disciplina"], rotation=15)
ax2.set_ylabel("Nota média")
ax2.set_title("Médias por disciplina: Goiás vs Brasil")
ax2.legend()

st.pyplot(fig2)

st.markdown("### Ranking das disciplinas por diferença")

ranking = comparacao.sort_values("Diferença", ascending=False).reset_index(drop=True)
ranking.index = ranking.index + 1

st.dataframe(
    ranking[["Disciplina", "Diferença", "Diferença_%"]].style.format({
        "Diferença": "{:.2f}",
        "Diferença_%": "{:.2f}"
    }),
    use_container_width=True
)