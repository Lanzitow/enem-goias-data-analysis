import streamlit as st
import pandas as pd
import plotly.express as px
from utils.load_data import carregar_microdados

st.title("⚠️ Alunos em Risco")

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

# -----------------------------
# FILTROS
# -----------------------------
col1, col2 = st.columns(2)

with col1:
    disciplina = st.selectbox(
        "Disciplina",
        disciplinas
    )

with col2:
    st.write("Comparação: Goiás vs Brasil")

# -----------------------------
# DADOS
# -----------------------------
df_go = df[df["Local"] == "Goiás"]
df_br = df[df["Local"] == "Brasil"]

# limite de risco
limite = 400

# -----------------------------
# FUNÇÃO
# -----------------------------
def calcular_risco(base):

    df_risco = base[
        base[disciplina] < limite
    ]

    percentual = (
        len(df_risco) / len(base)
    ) * 100

    return round(percentual, 2)

# -----------------------------
# CÁLCULOS
# -----------------------------
risco_go = calcular_risco(df_go)
risco_br = calcular_risco(df_br)

# -----------------------------
# MÉTRICAS
# -----------------------------
st.subheader(f"📊 Alunos em risco — {disciplina}")

c1, c2 = st.columns(2)

c1.metric(
    "Goiás",
    f"{risco_go:.2f}%"
)

c2.metric(
    "Brasil",
    f"{risco_br:.2f}%"
)

# -----------------------------
# TABELA
# -----------------------------
tabela = pd.DataFrame({
    "Local": ["Goiás", "Brasil"],
    "Percentual em risco": [
        risco_go,
        risco_br
    ]
})

st.dataframe(
    tabela,
    use_container_width=True
)

# -----------------------------
# GRÁFICO
# -----------------------------
fig = px.bar(
    tabela,
    x="Local",
    y="Percentual em risco",
    color="Local",
    title=f"Percentual de alunos em risco — {disciplina}"
)

fig.update_layout(
    yaxis_title="Percentual (%)",
    xaxis_title=""
)

st.plotly_chart(fig, use_container_width=True)

# -----------------------------
# INTERPRETAÇÃO
# -----------------------------
st.markdown("### 📌 Interpretação")

st.write(
    f"Foram considerados em situação de risco os participantes "
    f"com nota inferior a {limite} pontos em {disciplina}."
)

st.write("""
Percentuais mais elevados indicam maior concentração de alunos
com baixo desempenho, sugerindo necessidade de maior atenção
educacional nessa área.
""")

if risco_go > risco_br:

    st.write(
        "Goiás apresentou percentual de alunos em risco acima da média nacional."
    )

elif risco_go < risco_br:

    st.write(
        "Goiás apresentou percentual de alunos em risco abaixo da média nacional."
    )

else:

    st.write(
        "Os percentuais de Goiás e Brasil foram semelhantes."
    )

st.write("""
Essa análise permite identificar áreas com maior vulnerabilidade
acadêmica e auxilia na compreensão das dificuldades educacionais
dos participantes.
""")