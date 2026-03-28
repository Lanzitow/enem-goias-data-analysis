import streamlit as st

st.set_page_config(
    page_title="ENEM GO vs Brasil",
    layout="wide"
)

# -----------------------------
# TÍTULO
# -----------------------------
st.title("📊 Análise do ENEM 2024: Goiás vs Brasil")

# -----------------------------
# INTRODUÇÃO
# -----------------------------
st.header("📌 Introdução")

st.write("""
O Exame Nacional do Ensino Médio (ENEM) é uma das principais formas de avaliação
educacional no Brasil, sendo utilizado como critério de acesso ao ensino superior.

Este projeto tem como objetivo analisar os dados do ENEM 2024, comparando o desempenho
dos participantes do estado de Goiás com o cenário nacional.
""")

# -----------------------------
# OBJETIVO
# -----------------------------
st.header("🎯 Objetivo")

st.write("""
O objetivo deste estudo é aplicar técnicas de análise de dados para:

- Avaliar o desempenho médio dos participantes por área do conhecimento
- Comparar os resultados entre Goiás e o Brasil
- Analisar a distribuição das notas
- Investigar diferenças por tipo de escola e outros fatores
- Identificar padrões e possíveis desigualdades educacionais
""")

# -----------------------------
# METODOLOGIA
# -----------------------------
st.header("🧹 Metodologia")

st.write("""
A análise foi realizada a partir dos microdados do ENEM 2024, disponibilizados pelo INEP.

As principais etapas do projeto foram:

- Seleção das variáveis relevantes
- Tratamento dos dados (remoção de duplicados e valores ausentes)
- Padronização das variáveis
- Cálculo de medidas estatísticas (média, mediana, desvio padrão)
- Análise comparativa entre Goiás e Brasil
- Construção de visualizações interativas com Streamlit
""")

# -----------------------------
# SOBRE O DASHBOARD
# -----------------------------
st.header("🧭 Navegação do Dashboard")

st.write("""
Utilize o menu lateral para acessar as diferentes análises disponíveis:

- 📊 Qualidade dos Dados
- 📐 Medidas Descritivas
- 📊 Distribuição das Notas
- 📊 Comparações Goiás vs Brasil
- 🏫 Tipo de Escola
- 👨 Comparação por Sexo
- ❓ Questões de Pesquisa
- 📈 Desempenho acima da média
- 🚫 Notas zeradas
- ⚠️ Alunos em risco
- 📌 Conclusões

Cada seção apresenta resultados específicos, acompanhados de interpretações
para facilitar a compreensão dos dados.
""")

# -----------------------------
# FECHAMENTO
# -----------------------------
st.markdown("---")

st.write(
    "Este dashboard foi desenvolvido como parte de um projeto acadêmico, com o objetivo de aplicar "
    "conceitos de análise de dados na interpretação de indicadores educacionais."
)