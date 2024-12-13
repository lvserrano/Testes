import streamlit as st


# Função para calcular o preço de venda
def calcular_preco_venda(preco_minimo, markdown):
    try:
        # Verifica se a margem é 100%
        if markdown == 100:
            return "🚨 **Erro:** Uma margem de 100% resulta em preço de venda infinito."

        # Verifica se a margem é maior que 100% e exibe um aviso
        if markdown > 100:
            aviso = "⚠️ **Aviso:** A margem objetiva é maior que 100%. O cálculo será feito normalmente."
        else:
            aviso = ""

        # Calcula o preço de venda
        preco_venda = preco_minimo / (1 - markdown / 100)
        lucro_liquido = preco_venda - preco_minimo

        # Exibindo os resultados com formatação
        resultado = f"""
        {aviso}
        
        **Preço de Venda:**
        🏷️ R$ {preco_venda:,.2f}
        
        **Lucro Líquido:**
        💰 R$ {lucro_liquido:,.2f}
        """
        return resultado

    except ValueError:
        return "❌ **Erro:** Verifique se os valores digitados são numéricos."
    except Exception as e:
        return f"⚠️ **Erro:** Ocorreu um problema ao calcular o preço de venda. Detalhes: {str(e)}"


# Interface com o Streamlit
def app():
    st.title("Calculadora de Preço de Venda")

    # Entrada para o preço mínimo (Pmz)
    preco_minimo = st.number_input("Preço Mínimo (Pmz):", min_value=0.0, format="%.2f")

    # Entrada para a margem objetiva (Markdown)
    markdown = st.number_input(
        "Margem Objetiva (Markdown) %:", min_value=0.0, max_value=100.0, format="%.2f"
    )

    # Botão para calcular o preço de venda
    if st.button("Calcular"):
        resultado = calcular_preco_venda(preco_minimo, markdown)
        st.markdown(resultado)


if __name__ == "__main__":
    app()
