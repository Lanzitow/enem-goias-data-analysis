import streamlit as st
import pandas as pd
import plotly.express as px
from utils.load_data import carregar_microdados

st.title("📊 Comparações: Goiás vs Brasil")

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

# Mantive sua lógica
df_go = df[df["Local"] == "Goiás"].copy()
df_br = df[df["Local"] == "Brasil"].copy()

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

# 🔥 GRÁFICO INTERATIVO
fig = px.bar(
    x=["Goiás", "Brasil"],
    y=[linha["Média_GO"], linha["Média_BR"]],
    labels={"x": "Local", "y": "Nota média"},
    title=f"Comparação das médias - {disciplina_escolhida}"
)

st.plotly_chart(fig, use_container_width=True)

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

# 🔥 GRÁFICO INTERATIVO GERAL
fig2 = px.bar(
    comparacao,
    x="Disciplina",
    y=["Média_GO", "Média_BR"],
    barmode="group",
    title="Médias por disciplina: Goiás vs Brasil"
)

st.plotly_chart(fig2, use_container_width=True)

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