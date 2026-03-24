import streamlit as st
import pandas as pd
from utils.load_data import carregar_microdados

st.title("📌 Conclusões da Análise")

df = carregar_microdados()

disciplinas = [
    "Linguagens",
    "Matemática",
    "Ciências Humanas",
    "Ciências da Natureza",
    "Redação"
]

df_go = df[df["UF"] == "GO"]

# calcular diferenças
resultados = []

for d in disciplinas:
    media_go = df_go[d].mean()
    media_br = df[d].mean()
    diff = media_go - media_br

    resultados.append((d, media_go, media_br, diff))

df_res = pd.DataFrame(resultados, columns=["Disciplina", "GO", "BR", "Diferença"])

melhor = df_res.loc[df_res["Diferença"].idxmax()]
pior = df_res.loc[df_res["Diferença"].idxmin()]

st.subheader("📊 Principais resultados")

st.write(
    f"O estado de Goiás apresentou seu melhor desempenho relativo em **{melhor['Disciplina']}**, "
    f"com diferença de **{melhor['Diferença']:.2f} pontos** em relação à média nacional."
)

st.write(
    f"A maior desvantagem foi observada em **{pior['Disciplina']}**, "
    f"com diferença de **{pior['Diferença']:.2f} pontos**."
)

st.markdown("---")

st.subheader("📐 Interpretação estatística")

st.write("""
A análise das medidas descritivas demonstrou que as distribuições das notas em Goiás e no Brasil
são bastante semelhantes, com médias e medianas próximas na maioria das disciplinas.

Os valores de desvio padrão indicam uma dispersão significativa nas notas, especialmente em Matemática
e Redação, evidenciando grande variabilidade no desempenho dos participantes.
""")

st.markdown("---")

st.subheader("📊 Distribuição das notas")

st.write("""
A análise gráfica por meio de histogramas e boxplots mostrou que as distribuições das notas apresentam
comportamento semelhante entre Goiás e o Brasil.

Observa-se concentração de valores em faixas intermediárias, com presença de valores extremos
(outliers), especialmente nas notas mais altas.
""")

st.markdown("---")

st.subheader("📈 Comparação Goiás vs Brasil")

st.write("""
De modo geral, Goiás apresenta desempenho muito próximo ao cenário nacional.
As diferenças entre as médias são pequenas na maioria das áreas, indicando comportamento semelhante.

O destaque positivo é a Redação, onde Goiás apresenta vantagem mais expressiva,
enquanto nas demais disciplinas as diferenças são menos significativas.
""")

st.markdown("---")

st.subheader("🎯 Considerações finais")

st.write("""
A análise evidenciou que o desempenho dos estudantes de Goiás no ENEM 2024 está alinhado ao padrão nacional,
com pequenas variações entre as áreas do conhecimento.

Os resultados indicam que fatores estruturais e educacionais apresentam impacto semelhante tanto no estado
quanto no Brasil como um todo.

Este estudo reforça a importância da análise estatística como ferramenta para compreensão do desempenho educacional,
permitindo identificar padrões, desigualdades e oportunidades de melhoria no sistema de ensino.
""")