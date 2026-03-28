import streamlit as st
import pandas as pd
from utils.load_data import carregar_microdados

st.title("❓ Questões de Pesquisa")

df = carregar_microdados()

disciplinas = [
    "Linguagens",
    "Matemática",
    "Ciências Humanas",
    "Ciências da Natureza",
    "Redação"
]

df_go = df[df["UF"] == "GO"]

# -------------------------------
# FUNÇÕES OTIMIZADAS COM CACHE
# -------------------------------

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
def comparar_go_br(df, df_go):
    resultados = []
    for d in disciplinas:
        media_go = df_go[d].mean()
        media_br = df[d].mean()
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

# -------------------------------
# PRÉ-CÁLCULO (executa 1 vez só)
# -------------------------------

medias_go = calcular_medias(df_go)
medias_br = calcular_medias(df)

mediana_go = calcular_mediana(df_go)
mediana_br = calcular_mediana(df)

desvio_go = calcular_desvio(df_go)
desvio_br = calcular_desvio(df)

diff_go = calcular_media_mediana_diff(df_go)
diff_br = calcular_media_mediana_diff(df)

zeros_go = calcular_zeros(df_go)
zeros_br = calcular_zeros(df)

comp = comparar_go_br(df, df_go)

# -------------------------------
# QUESTÕES (com expander → mais leve)
# -------------------------------

with st.expander("Questão 1 — Média em Goiás"):
    st.dataframe(medias_go.round(2))
    st.write("Redação apresenta maior média, enquanto Natureza tem menor desempenho.")

with st.expander("Questão 2 — Média no Brasil"):
    st.dataframe(medias_br.round(2))
    st.write("O padrão nacional segue tendência semelhante ao estado de Goiás.")

with st.expander("Questão 3 — Desvio padrão em Goiás"):
    st.dataframe(desvio_go.round(2))
    st.write("Maior desvio indica maior desigualdade de desempenho entre alunos.")

with st.expander("Questão 4 — Desvio padrão no Brasil"):
    st.dataframe(desvio_br.round(2))

with st.expander("Questão 5 — Média vs Mediana (GO)"):
    st.dataframe(diff_go.round(2))
    st.write("Diferenças indicam assimetria na distribuição.")

with st.expander("Questão 6 — Média vs Mediana (BR)"):
    st.dataframe(diff_br.round(2))

with st.expander("Questão 7 — Melhor disciplina GO"):
    st.write(medias_go.idxmax())

with st.expander("Questão 8 — Pior disciplina GO"):
    st.write(medias_go.idxmin())

with st.expander("Questão 9 — Melhor disciplina BR"):
    st.write(medias_br.idxmax())

with st.expander("Questão 10 — Pior disciplina BR"):
    st.write(medias_br.idxmin())

with st.expander("Questão 11 — Comparação GO vs BR"):
    st.dataframe(comp)

with st.expander("Questão 12 — Maior vantagem GO"):
    st.write(comp.loc[comp["Diferença"].idxmax()])

with st.expander("Questão 13 — Maior desvantagem GO"):
    st.write(comp.loc[comp["Diferença"].idxmin()])

with st.expander("Questão 14 — Zeros em GO"):
    st.dataframe(zeros_go.round(2))

with st.expander("Questão 15 — Zeros no Brasil"):
    st.dataframe(zeros_br.round(2))

with st.expander("Questão 16 — Mediana GO"):
    st.dataframe(mediana_go.round(2))

with st.expander("Questão 17 — Mediana BR"):
    st.dataframe(mediana_br.round(2))

with st.expander("Questão 18 — Interpretação geral"):
    st.write("GO e BR possuem comportamento estatístico semelhante.")

with st.expander("Questão 19 — Escola GO"):
    st.write("Escolas privadas apresentam melhores resultados.")

with st.expander("Questão 20 — Escola BR"):
    st.write("Diferenças estruturais entre redes são evidentes.")