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

df_go = df[df["UF"] == "GO"].copy()

# calcular diferenças entre GO e BR
resultados = []

for d in disciplinas:
    media_go = df_go[d].mean()
    media_br = df[d].mean()
    diff = media_go - media_br

    resultados.append((d, media_go, media_br, diff))

df_res = pd.DataFrame(resultados, columns=["Disciplina", "GO", "BR", "Diferença"])

melhor = df_res.loc[df_res["Diferença"].idxmax()]
pior = df_res.loc[df_res["Diferença"].idxmin()]

st.subheader("📊 Síntese dos principais resultados")

st.write(
    f"A comparação entre Goiás e Brasil mostrou que o melhor desempenho relativo de Goiás ocorreu em "
    f"**{melhor['Disciplina']}**, com vantagem de **{melhor['Diferença']:.2f} pontos** em relação à média nacional."
)

st.write(
    f"Por outro lado, a maior desvantagem de Goiás foi observada em **{pior['Disciplina']}**, "
    f"com diferença de **{abs(pior['Diferença']):.2f} pontos** em relação ao Brasil."
)

st.markdown("---")

st.subheader("📐 Interpretação estatística")

st.write("""
A análise das medidas descritivas permitiu verificar que Goiás e Brasil apresentam comportamentos
estatísticos bastante próximos na maior parte das disciplinas avaliadas. De modo geral, as médias
e medianas mantiveram valores semelhantes, indicando um padrão relativamente alinhado entre o estado
e o cenário nacional.

Além disso, os desvios padrão mostraram que há dispersão considerável nas notas, especialmente em
Matemática e Redação. Esse resultado evidencia heterogeneidade no desempenho dos participantes,
ou seja, há diferenças expressivas entre alunos com notas mais baixas e mais altas.
""")

st.markdown("---")

st.subheader("📊 Distribuição das notas")

st.write("""
A análise das distribuições, por meio de histogramas e boxplots, mostrou que Goiás e Brasil possuem
formatos semelhantes de concentração de notas. Em geral, as maiores frequências concentram-se em faixas
intermediárias, enquanto valores extremos aparecem em menor proporção.

Esse comportamento reforça a ideia de que o desempenho dos estudantes goianos acompanha a tendência
nacional, sem apresentar rupturas muito acentuadas em relação ao padrão observado no Brasil.
""")

st.markdown("---")

st.subheader("📈 Comparação entre Goiás e Brasil")

st.write("""
A comparação direta das médias por disciplina mostrou que Goiás apresenta desempenho muito próximo
ao Brasil na maior parte das áreas do conhecimento. As diferenças observadas são, em geral, pequenas,
o que indica forte semelhança entre os dois contextos analisados.

O principal destaque positivo de Goiás encontra-se em Redação, disciplina em que o estado supera
de forma mais expressiva a média nacional. Nas demais áreas, as variações são menores, com diferenças
positivas e negativas de baixa magnitude.
""")

st.markdown("---")

st.subheader("🏫 Tipo de escola e desigualdades educacionais")

st.write("""
As análises por tipo de escola evidenciaram diferenças importantes no desempenho dos estudantes.
De forma geral, escolas privadas apresentaram médias superiores às redes públicas, tanto em Goiás
quanto no Brasil. Esse resultado sugere a presença de desigualdades estruturais no acesso a melhores
condições de aprendizagem e desempenho acadêmico.

Assim, o tipo de escola mostrou-se um fator relevante para compreender parte da variação observada
nas notas do ENEM.
""")

st.markdown("---")

st.subheader("🎯 Considerações finais")

st.write("""
Conclui-se que o desempenho dos estudantes de Goiás no ENEM 2024 apresenta forte proximidade com
o padrão nacional, com pequenas diferenças entre as disciplinas analisadas. Embora Goiás tenha se
destacado positivamente em algumas áreas, especialmente em Redação, o comportamento geral permanece
alinhado ao contexto brasileiro.

O estudo também demonstrou que a análise estatística é fundamental para compreender o desempenho
educacional de forma mais ampla, permitindo identificar padrões, níveis de dispersão, desigualdades
e possíveis pontos de atenção. Dessa forma, os resultados obtidos contribuem para uma leitura mais
consistente da realidade educacional, tanto em Goiás quanto no Brasil.
""")