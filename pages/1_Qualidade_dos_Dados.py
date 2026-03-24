import streamlit as st

st.title("🧹 Qualidade dos Dados")

base_inicial = 4332944
duplicados = 1151156
apos_limpeza = 2990085

col1, col2, col3 = st.columns(3)

col1.metric("Base inicial", f"{base_inicial:,}".replace(",", "."))
col2.metric("Duplicados removidos", f"{duplicados:,}".replace(",", "."))
col3.metric("Base final", f"{apos_limpeza:,}".replace(",", "."))

st.markdown("### 📌 Interpretação")

st.write("""
A base de dados original continha mais de 4,3 milhões de registros.
Após a limpeza, foram removidos mais de 1,1 milhão de registros duplicados,
além de valores ausentes, resultando em uma base mais confiável para análise.

Essa etapa é essencial para garantir a validade estatística dos resultados apresentados.
        
Inicialmente, realizamos a limpeza dos dados, removendo duplicados e valores inconsistentes, reduzindo a base para aproximadamente 3 milhões de registros válidos.
Em seguida, comparamos as médias entre Goiás e o Brasil, observando que o estado apresentou desempenho superior principalmente em Redação, enquanto nas demais áreas manteve resultados próximos da média nacional.
""")