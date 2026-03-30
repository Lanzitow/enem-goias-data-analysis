import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("🏫 Comparação por Tipo de Escola")

# carregar base
df = pd.read_csv("dados/tratado/enem_escola_sample.csv")

disciplinas = [
    "Linguagens",
    "Matemática",
    "Ciências Humanas",
    "Ciências da Natureza",
    "Redação"
]

disciplina = st.selectbox("Disciplina", disciplinas)

# separar bases
df_br = df.copy()
df_go = df[df["SG_UF_PROVA"] == "GO"].copy()

# médias por tipo de escola
media_br = df_br.groupby("Tipo_Escola")[disciplina].mean()
media_go = df_go.groupby("Tipo_Escola")[disciplina].mean()

# juntar em uma tabela
comparacao = pd.DataFrame({
    "Brasil": media_br,
    "Goiás": media_go
}).round(2)

# ordenar pelos nomes das escolas
comparacao = comparacao.sort_index()

st.subheader("📊 Médias por tipo de escola — Brasil x Goiás")
st.dataframe(comparacao.reset_index())

# gráfico de barras agrupadas
fig, ax = plt.subplots(figsize=(10, 6))
comparacao.plot(kind="bar", ax=ax)

ax.set_title(f"Média das notas em {disciplina} por tipo de escola")
ax.set_ylabel("Nota média")
ax.set_xlabel("Tipo de escola")
ax.legend(title="Grupo")
plt.xticks(rotation=45)

st.pyplot(fig)

# interpretação automática
st.markdown("### 📌 Interpretação")

for escola in comparacao.index:
    brasil = comparacao.loc[escola, "Brasil"]
    goias = comparacao.loc[escola, "Goiás"]
    diferenca = goias - brasil

    st.write(
        f"No tipo de escola **{escola}**, a média em **{disciplina}** foi "
        f"**{brasil:.2f}** no Brasil e **{goias:.2f}** em Goiás, "
        f"com diferença de **{diferenca:.2f}** pontos."
    )

# comparação entre privada e estadual
if "Privada" in comparacao.index and "Estadual" in comparacao.index:
    gap_br = comparacao.loc["Privada", "Brasil"] - comparacao.loc["Estadual", "Brasil"]
    gap_go = comparacao.loc["Privada", "Goiás"] - comparacao.loc["Estadual", "Goiás"]

    st.write(
        f"No Brasil, a diferença entre escolas **Privadas** e **Estaduais** é de "
        f"aproximadamente **{gap_br:.2f} pontos**."
    )

    st.write(
        f"Em Goiás, essa diferença é de aproximadamente **{gap_go:.2f} pontos**."
    )

st.write(
    "De forma geral, a comparação simultânea entre Brasil e Goiás permite observar "
    "com mais clareza como o tipo de escola está associado ao desempenho dos alunos."
)
