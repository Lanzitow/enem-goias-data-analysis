import streamlit as st
import pandas as pd
import plotly.express as px
from utils.load_data import carregar_microdados

st.title("📈 Desempenho Acima da Média")

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
# FILTRO
# -----------------------------
col1, col2 = st.columns(2)

with col1:
    disciplina = st.selectbox(
        "Escolha a disciplina",
        disciplinas
    )

with col2:
    st.write("Comparação: Goiás vs Brasil")

# -----------------------------
# DADOS
# -----------------------------
df_go = df[df["Local"] == "Goiás"]
df_br = df[df["Local"] == "Brasil"]

# -----------------------------
# FUNÇÃO
# -----------------------------
def calcular_percentuais(base):

    media = base[disciplina].mean()

    acima_media = base[
        base[disciplina] >= media
    ]

    acima_100 = base[
        base[disciplina] >= media + 100
    ]

    acima_200 = base[
        base[disciplina] >= media + 200
    ]

    total = len(base)

    p1 = len(acima_media) / total * 100
    p2 = len(acima_100) / total * 100
    p3 = len(acima_200) / total * 100

    return (
        round(p1, 2),
        round(p2, 2),
        round(p3, 2),
        round(media, 2)
    )

# -----------------------------
# CÁLCULOS
# -----------------------------
p1_go, p2_go, p3_go, media_go = calcular_percentuais(df_go)
p1_br, p2_br, p3_br, media_br = calcular_percentuais(df_br)

# -----------------------------
# MÉTRICAS
# -----------------------------
st.subheader(f"📊 Comparação — {disciplina}")

c1, c2, c3 = st.columns(3)

c1.metric(
    "Acima da média",
    f"{p1_go:.2f}% (GO)",
    f"{p1_br:.2f}% (BR)"
)

c2.metric(
    "+100 pontos",
    f"{p2_go:.2f}% (GO)",
    f"{p2_br:.2f}% (BR)"
)

c3.metric(
    "+200 pontos",
    f"{p3_go:.2f}% (GO)",
    f"{p3_br:.2f}% (BR)"
)

# -----------------------------
# TABELA
# -----------------------------
dados = pd.DataFrame({
    "Faixa": [
        "Acima da média",
        "+100 pontos",
        "+200 pontos"
    ],
    "Goiás (%)": [
        p1_go,
        p2_go,
        p3_go
    ],
    "Brasil (%)": [
        p1_br,
        p2_br,
        p3_br
    ]
})

st.dataframe(
    dados,
    use_container_width=True
)

# -----------------------------
# GRÁFICO
# -----------------------------
fig = px.bar(
    dados,
    x="Faixa",
    y=["Goiás (%)", "Brasil (%)"],
    barmode="group",
    title=f"Percentual de alunos acima da média — {disciplina}"
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
    f"A média de Goiás em {disciplina} foi de {media_go:.2f} pontos, "
    f"enquanto a média nacional foi de {media_br:.2f} pontos."
)

st.write("""
A análise mostra o percentual de estudantes que conseguiram
atingir desempenho acima da média, além de faixas mais elevadas
(+100 e +200 pontos).

Observa-se que apenas uma parcela menor dos participantes
atinge níveis muito superiores à média, indicando concentração
das notas em faixas intermediárias.
""")

st.write("""
Essa análise ajuda a identificar o nível de excelência acadêmica
dos participantes e permite comparar o desempenho relativo entre
Goiás e o cenário nacional.
""")