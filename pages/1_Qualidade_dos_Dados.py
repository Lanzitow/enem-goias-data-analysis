import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("📊 Qualidade dos Dados")

# -----------------------------
# NÚMEROS OFICIAIS DO PROCESSO
# -----------------------------
base_resultados_original = 4_332_944
base_participantes_original = 4_332_944

base_inicial_analise = 4_332_944   # após selecionar as 6 colunas usadas na análise
duplicados_removidos = 1_151_156
base_apos_duplicados = 3_181_788
base_final_limpa = 2_990_085

nulos_antes = {
    "SG_UF_PROVA": 0,
    "Linguagens": 14_842,
    "Matemática": 176_888,
    "Ciências Humanas": 14_842,
    "Ciências da Natureza": 176_888,
    "Redação": 14_842
}

nulos_depois = {
    "SG_UF_PROVA": 0,
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

c1, c2, c3 = st.columns(3)
c1.metric("RESULTADOS_2024 original", f"{base_resultados_original:,}".replace(",", "."))
c2.metric("Base inicial da análise", f"{base_inicial_analise:,}".replace(",", "."))
c3.metric("Base final limpa", f"{base_final_limpa:,}".replace(",", "."))

removidos_total = base_inicial_analise - base_final_limpa
st.write(f"Total de registros removidos no processo de limpeza: **{removidos_total:,}**".replace(",", "."))

st.markdown("---")

# -----------------------------
# FLUXO DA LIMPEZA
# -----------------------------
st.subheader("🧹 Etapas do tratamento dos dados")

etapas = pd.DataFrame({
    "Etapa": [
        "Base inicial da análise",
        "Após remoção de duplicados",
        "Após remoção de valores ausentes (NaN)"
    ],
    "Quantidade": [
        base_inicial_analise,
        base_apos_duplicados,
        base_final_limpa
    ]
})

st.dataframe(etapas, use_container_width=True)

fig, ax = plt.subplots(figsize=(8, 4))
ax.bar(etapas["Etapa"], etapas["Quantidade"])
ax.set_title("Evolução da quantidade de registros")
ax.set_ylabel("Quantidade")
ax.tick_params(axis="x", rotation=15)
st.pyplot(fig)

st.markdown("---")

# -----------------------------
# DUPLICADOS
# -----------------------------
st.subheader("🔁 Registros duplicados")

st.metric("Duplicados identificados e removidos", f"{duplicados_removidos:,}".replace(",", "."))

st.write(
    "A remoção de duplicados foi necessária para evitar super-representação de registros "
    "iguais nas análises estatísticas."
)

st.markdown("---")

# -----------------------------
# VALORES AUSENTES
# -----------------------------
st.subheader("❌ Valores ausentes (NaN)")

df_nulos = pd.DataFrame({
    "Disciplina/Variável": list(nulos_antes.keys()),
    "Antes da limpeza": list(nulos_antes.values()),
    "Após a limpeza": list(nulos_depois.values())
})

st.dataframe(df_nulos, use_container_width=True)

st.write(
    "Os valores ausentes foram removidos para garantir consistência nas medidas descritivas, "
    "nas distribuições e nas comparações entre Goiás e Brasil."
)

st.markdown("---")

# -----------------------------
# NOTAS ZERADAS
# -----------------------------
st.subheader("🚫 Notas zeradas")

st.write(
    "As notas zeradas **não foram removidas** na limpeza. "
    "Isso porque zero representa desempenho real do participante, e não valor ausente."
)

st.write(
    "Em outras palavras: o processo removeu valores faltantes (NaN) e duplicados, "
    "mas preservou registros com nota 0 para manter a fidelidade da análise."
)

st.markdown("---")

# -----------------------------
# COLUNAS UTILIZADAS
# -----------------------------
st.subheader("🧾 Variáveis utilizadas na análise")

colunas = pd.DataFrame({
    "Coluna original": [
        "SG_UF_PROVA",
        "NU_NOTA_LC",
        "NU_NOTA_MT",
        "NU_NOTA_CH",
        "NU_NOTA_CN",
        "NU_NOTA_REDACAO"
    ],
    "Nome utilizado no projeto": [
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
st.subheader("📈 Impacto da limpeza")

st.write(
    "A etapa de tratamento dos dados foi fundamental para garantir confiabilidade aos resultados. "
    "Foram removidos registros duplicados e observações com valores ausentes, enquanto as notas zeradas "
    "foram mantidas por representarem desempenho efetivo dos participantes."
)

st.write(
    "Com isso, a base final utilizada nas análises ficou mais consistente e adequada para comparação "
    "estatística entre Goiás e Brasil."
)