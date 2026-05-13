import streamlit as st
import pandas as pd
import plotly.express as px
from utils.load_data import carregar_microdados

st.title("📌 Conclusões da Análise")

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
# COMPARAÇÃO
# -----------------------------
resultados = []

for d in disciplinas:

    media_go = df_go[d].mean()
    media_br = df_br[d].mean()

    diff = media_go - media_br
    diff_pct = (diff / media_br) * 100

    resultados.append({
        "Disciplina": d,
        "Média GO": round(media_go, 2),
        "Média BR": round(media_br, 2),
        "Diferença": round(diff, 2),
        "Diferença %": round(diff_pct, 2)
    })

df_res = pd.DataFrame(resultados)

melhor = df_res.loc[
    df_res["Diferença"].idxmax()
]

pior = df_res.loc[
    df_res["Diferença"].idxmin()
]

# -----------------------------
# TABELA FINAL
# -----------------------------
st.subheader("📊 Comparação final das médias")

st.dataframe(
    df_res,
    use_container_width=True
)

# -----------------------------
# GRÁFICO
# -----------------------------
fig = px.bar(
    df_res,
    x="Disciplina",
    y=["Média GO", "Média BR"],
    barmode="group",
    title="Comparação final — Goiás vs Brasil"
)

fig.update_layout(
    yaxis_title="Nota média",
    xaxis_title=""
)

st.plotly_chart(fig, use_container_width=True)

# -----------------------------
# PRINCIPAIS RESULTADOS
# -----------------------------
st.markdown("---")

st.subheader("📌 Síntese dos principais resultados")

st.write(
    f"O melhor desempenho relativo de Goiás ocorreu em "
    f"{melhor['Disciplina']}, com vantagem de "
    f"{melhor['Diferença']:.2f} pontos em relação ao Brasil."
)

st.write(
    f"A maior desvantagem foi observada em "
    f"{pior['Disciplina']}, com diferença de "
    f"{abs(pior['Diferença']):.2f} pontos."
)

# -----------------------------
# INTERPRETAÇÃO
# -----------------------------
st.markdown("---")

st.subheader("📐 Interpretação estatística")

st.write("""
As análises estatísticas mostraram que Goiás e Brasil possuem
comportamentos bastante semelhantes na maior parte das disciplinas.
""")

st.write("""
As médias e medianas apresentaram valores próximos,
indicando alinhamento entre o desempenho estadual e nacional.
""")

st.write("""
Os desvios padrão evidenciaram dispersão significativa das notas,
principalmente em Matemática e Redação, indicando heterogeneidade
entre os participantes.
""")

# -----------------------------
# DISTRIBUIÇÃO
# -----------------------------
st.markdown("---")

st.subheader("📊 Distribuição das notas")

st.write("""
Os histogramas e boxplots mostraram concentração das notas
em faixas intermediárias, com presença de valores extremos
em menor proporção.
""")

st.write("""
As distribuições observadas em Goiás acompanharam o padrão
geral identificado no Brasil.
""")

# -----------------------------
# COMPARAÇÃO
# -----------------------------
st.markdown("---")

st.subheader("📈 Comparação entre Goiás e Brasil")

st.write("""
As diferenças entre Goiás e Brasil foram relativamente pequenas
na maioria das disciplinas analisadas.
""")

st.write("""
O principal destaque positivo de Goiás ocorreu em Redação,
disciplina em que o estado apresentou desempenho superior
à média nacional.
""")

# -----------------------------
# ESCOLAS
# -----------------------------
st.markdown("---")

st.subheader("🏫 Tipo de escola e desigualdade")

st.write("""
As análises mostraram diferenças importantes entre os tipos
de escola.
""")

st.write("""
Escolas privadas apresentaram desempenho superior em relação
às redes públicas, tanto em Goiás quanto no Brasil.
""")

st.write("""
Esse resultado sugere influência de fatores estruturais,
econômicos e educacionais no desempenho dos participantes.
""")

# -----------------------------
# NOTAS ZERADAS
# -----------------------------
st.markdown("---")

st.subheader("🚫 Notas zeradas")

st.write("""
As notas zeradas foram mantidas na análise por representarem
desempenho real dos participantes.
""")

st.write("""
Os resultados mostraram maior concentração de notas zeradas
em algumas disciplinas específicas, evidenciando possíveis
dificuldades de aprendizagem.
""")

# -----------------------------
# ALUNOS EM RISCO
# -----------------------------
st.markdown("---")

st.subheader("⚠️ Alunos em risco")

st.write("""
A análise de alunos com notas abaixo de 400 pontos permitiu
identificar grupos com maior vulnerabilidade acadêmica.
""")

st.write("""
Esse indicador pode auxiliar na identificação de áreas
que demandam maior atenção educacional.
""")

# -----------------------------
# CONSIDERAÇÕES FINAIS
# -----------------------------
st.markdown("---")

st.subheader("🎯 Considerações finais")

st.write("""
Conclui-se que o desempenho de Goiás no ENEM 2024 apresentou
forte proximidade com o cenário nacional.
""")

st.write("""
Apesar das diferenças observadas em algumas disciplinas,
o comportamento estatístico geral permaneceu semelhante
entre Goiás e Brasil.
""")

st.write("""
O estudo demonstrou a importância da análise estatística
na compreensão do desempenho educacional, permitindo
identificar padrões, desigualdades e possíveis desafios
do sistema de ensino.
""")