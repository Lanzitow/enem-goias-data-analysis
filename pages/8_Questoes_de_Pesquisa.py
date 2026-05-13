import streamlit as st
import pandas as pd
from utils.load_data import carregar_microdados

st.title("❓ Questões de Pesquisa")

df = carregar_microdados()

# -----------------------------
# CLASSIFICAÇÃO GO vs BR
# -----------------------------
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

df_go = df[df["Local"] == "Goiás"]
df_br = df[df["Local"] == "Brasil"]

# -----------------------------
# FUNÇÕES
# -----------------------------
@st.cache_data
def calcular_medias(df_base):
    return df_base[disciplinas].mean()

@st.cache_data
def calcular_mediana(df_base):
    return df_base[disciplinas].median()

@st.cache_data
def calcular_desvio(df_base):
    return df_base[disciplinas].std()

@st.cache_data
def calcular_media_mediana_diff(df_base):
    return df_base[disciplinas].mean() - df_base[disciplinas].median()

@st.cache_data
def calcular_zeros(df_base):
    return (df_base[disciplinas] == 0).mean() * 100

@st.cache_data
def comparar_go_br(df_go, df_br):

    resultados = []

    for d in disciplinas:

        media_go = df_go[d].mean()
        media_br = df_br[d].mean()

        diff = media_go - media_br
        diff_pct = (diff / media_br) * 100

        resultados.append({
            "Disciplina": d,
            "Média_GO": round(media_go, 2),
            "Média_BR": round(media_br, 2),
            "Diferença": round(diff, 2),
            "Diferença_%": round(diff_pct, 2)
        })

    return pd.DataFrame(resultados)

# -----------------------------
# PRÉ-CÁLCULOS
# -----------------------------
medias_go = calcular_medias(df_go)
medias_br = calcular_medias(df_br)

mediana_go = calcular_mediana(df_go)
mediana_br = calcular_mediana(df_br)

desvio_go = calcular_desvio(df_go)
desvio_br = calcular_desvio(df_br)

diff_go = calcular_media_mediana_diff(df_go)
diff_br = calcular_media_mediana_diff(df_br)

zeros_go = calcular_zeros(df_go)
zeros_br = calcular_zeros(df_br)

comp = comparar_go_br(df_go, df_br)

# -----------------------------
# QUESTÕES
# -----------------------------

with st.expander("Questão 1 — Quais são as médias das disciplinas em Goiás?"):

    st.dataframe(medias_go.round(2))

    st.write("""
    Em Goiás, a maior média foi observada em Redação,
    enquanto Ciências da Natureza apresentou os menores valores médios.
    """)

# --------------------------------

with st.expander("Questão 2 — Quais são as médias das disciplinas no Brasil?"):

    st.dataframe(medias_br.round(2))

    st.write("""
    O comportamento das médias nacionais é semelhante ao observado em Goiás,
    com destaque para Redação.
    """)

# --------------------------------

with st.expander("Questão 3 — Qual o desvio padrão das notas em Goiás?"):

    st.dataframe(desvio_go.round(2))

    st.write("""
    O desvio padrão mede a dispersão das notas.
    Valores mais altos indicam maior desigualdade de desempenho entre os participantes.
    """)

# --------------------------------

with st.expander("Questão 4 — Qual o desvio padrão das notas no Brasil?"):

    st.dataframe(desvio_br.round(2))

# --------------------------------

with st.expander("Questão 5 — Existe diferença entre média e mediana em Goiás?"):

    st.dataframe(diff_go.round(2))

    st.write("""
    Diferenças entre média e mediana podem indicar assimetria
    na distribuição das notas.
    """)

# --------------------------------

with st.expander("Questão 6 — Existe diferença entre média e mediana no Brasil?"):

    st.dataframe(diff_br.round(2))

# --------------------------------

with st.expander("Questão 7 — Qual a melhor disciplina em Goiás?"):

    st.write(f"Disciplina com maior média: {medias_go.idxmax()}")

# --------------------------------

with st.expander("Questão 8 — Qual a pior disciplina em Goiás?"):

    st.write(f"Disciplina com menor média: {medias_go.idxmin()}")

# --------------------------------

with st.expander("Questão 9 — Qual a melhor disciplina no Brasil?"):

    st.write(f"Disciplina com maior média: {medias_br.idxmax()}")

# --------------------------------

with st.expander("Questão 10 — Qual a pior disciplina no Brasil?"):

    st.write(f"Disciplina com menor média: {medias_br.idxmin()}")

# --------------------------------

with st.expander("Questão 11 — Como Goiás se compara ao Brasil?"):

    st.dataframe(comp)

    st.write("""
    Goiás apresenta comportamento estatístico bastante semelhante
    ao cenário nacional, com pequenas diferenças entre as disciplinas.
    """)

# --------------------------------

with st.expander("Questão 12 — Qual a maior vantagem de Goiás?"):

    st.dataframe(
        comp.loc[[comp["Diferença"].idxmax()]]
    )

# --------------------------------

with st.expander("Questão 13 — Qual a maior desvantagem de Goiás?"):

    st.dataframe(
        comp.loc[[comp["Diferença"].idxmin()]]
    )

# --------------------------------

with st.expander("Questão 14 — Qual o percentual de notas zeradas em Goiás?"):

    st.dataframe(zeros_go.round(2))

# --------------------------------

with st.expander("Questão 15 — Qual o percentual de notas zeradas no Brasil?"):

    st.dataframe(zeros_br.round(2))

# --------------------------------

with st.expander("Questão 16 — Qual a mediana das notas em Goiás?"):

    st.dataframe(mediana_go.round(2))

# --------------------------------

with st.expander("Questão 17 — Qual a mediana das notas no Brasil?"):

    st.dataframe(mediana_br.round(2))

# --------------------------------

with st.expander("Questão 18 — Qual a interpretação geral dos resultados?"):

    st.write("""
    Goiás e Brasil apresentam distribuições e médias bastante semelhantes,
    indicando comportamento estatístico próximo entre os grupos analisados.
    """)

# --------------------------------

with st.expander("Questão 19 — Como o tipo de escola influencia Goiás?"):

    st.write("""
    Em Goiás, escolas privadas apresentaram médias superiores
    em praticamente todas as disciplinas analisadas.
    """)

# --------------------------------

with st.expander("Questão 20 — Como o tipo de escola influencia o Brasil?"):

    st.write("""
    No Brasil, também foi observada diferença significativa entre os tipos de escola,
    evidenciando desigualdades estruturais no desempenho educacional.
    """)