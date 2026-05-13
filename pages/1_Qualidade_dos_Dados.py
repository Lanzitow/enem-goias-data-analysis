import streamlit as st
import pandas as pd
import plotly.express as px

st.title("📊 Qualidade dos Dados")

# -----------------------------
# NÚMEROS OFICIAIS DO PROCESSO
# -----------------------------
base_original = 4_332_944
base_final_limpa = 2_990_093

removidos_total = base_original - base_final_limpa

nulos_antes = {
    "UF": 0,
    "Linguagens": 1_164_989,
    "Matemática": 1_327_963,
    "Ciências Humanas": 1_164_989,
    "Ciências da Natureza": 1_327_963,
    "Redação": 1_164_989
}

nulos_depois = {
    "UF": 0,
    "Linguagens": 0,
    "Matemática": 0,
    "Ciências Humanas": 0,
    "Ciências da Natureza": 0,
    "Redação": 0
}

# -----------------------------
# TAMANHO DAS BASES
# -----------------------------
st.subheader("📌 Tamanho das bases")

c1, c2 = st.columns(2)

c1.metric(
    "Base original",
    f"{base_original:,}".replace(",", ".")
)

c2.metric(
    "Base final limpa",
    f"{base_final_limpa:,}".replace(",", ".")
)

st.write(
    f"Total de registros removidos por valores ausentes (NaN): "
    f"**{removidos_total:,}**".replace(",", ".")
)

st.markdown("---")

# -----------------------------
# FLUXO DA LIMPEZA
# -----------------------------
st.subheader("🧹 Processo de tratamento dos dados")

etapas = pd.DataFrame({
    "Etapa": [
        "Base original",
        "Após remoção de valores ausentes (NaN)"
    ],
    "Quantidade": [
        base_original,
        base_final_limpa
    ]
})

st.dataframe(etapas, use_container_width=True)

# gráfico
fig = px.bar(
    etapas,
    x="Etapa",
    y="Quantidade",
    text="Quantidade",
    title="Quantidade de registros após o tratamento"
)

fig.update_traces(texttemplate='%{text:,}', textposition='outside')

st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# -----------------------------
# DUPLICADOS
# -----------------------------
st.subheader("🔁 Registros duplicados")

st.write("""
Nenhum registro foi removido por duplicidade.

Participantes diferentes podem possuir exatamente as mesmas notas
e características analisadas. Portanto, os registros foram mantidos
para preservar a distribuição real dos dados.
""")

st.markdown("---")

# -----------------------------
# VALORES AUSENTES
# -----------------------------
st.subheader("❌ Valores ausentes (NaN)")

df_nulos = pd.DataFrame({
    "Variável": list(nulos_antes.keys()),
    "Antes da limpeza": list(nulos_antes.values()),
    "Após limpeza": list(nulos_depois.values())
})

st.dataframe(df_nulos, use_container_width=True)

st.write("""
Os valores ausentes (NaN) representam participantes sem nota válida
em uma ou mais áreas do ENEM.

Esses registros foram removidos para garantir consistência estatística
nas análises descritivas, distribuições e comparações entre Goiás e Brasil.
""")

st.markdown("---")

# -----------------------------
# NOTAS ZERADAS
# -----------------------------
st.subheader("🚫 Notas zeradas")

st.write("""
As notas zeradas não foram removidas da análise.

Nota 0 representa desempenho real do participante, enquanto valores NaN
representam ausência de informação.
""")

st.markdown("---")

# -----------------------------
# VARIÁVEIS UTILIZADAS
# -----------------------------
st.subheader("🧾 Variáveis utilizadas")

colunas = pd.DataFrame({
    "Coluna original": [
        "SG_UF_PROVA",
        "NU_NOTA_LC",
        "NU_NOTA_MT",
        "NU_NOTA_CH",
        "NU_NOTA_CN",
        "NU_NOTA_REDACAO"
    ],
    "Nome utilizado": [
        "UF",
        "Linguagens",
        "Matemática",
        "Ciências Humanas",
        "Ciências da Natureza",
        "Redação"
    ]
})

st.dataframe(colunas, use_container_width=True)

st.markdown("---")

# -----------------------------
# IMPACTO DA LIMPEZA
# -----------------------------
st.subheader("📈 Impacto do tratamento dos dados")

st.write("""
O tratamento dos dados foi essencial para garantir maior confiabilidade
às análises estatísticas realizadas no projeto.

A limpeza consistiu na remoção apenas de registros com valores ausentes (NaN),
mantendo registros válidos mesmo quando participantes possuíam notas iguais.

Com isso, a base final preserva de forma mais fiel a distribuição real
do desempenho dos participantes do ENEM 2024.
""")