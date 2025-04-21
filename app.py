import streamlit as st
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from io import BytesIO
from datetime import datetime

st.set_page_config(
    page_title="Gerador de Nota Fiscal",
    page_icon="./img/Logo.png",
) 




def gerar_nota_fiscal(dados_empresa, dados_cliente, produtos):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    # Cabeçalho
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, height - 50, "NOTA FISCAL FICTÍCIA ")

    # Dados da empresa
    c.setFont("Helvetica", 10)
    c.drawString(50, height - 80, f"Empresa: {dados_empresa['nome']}")
    c.drawString(50, height - 95, f"CNPJ: {dados_empresa['cnpj']}")
    c.drawString(50, height - 110, f"Endereço: {dados_empresa['endereco']}")

    # Dados do cliente
    c.drawString(50, height - 140, f"Cliente: {dados_cliente['nome']}")
    c.drawString(50, height - 155, f"CPF: {dados_cliente['cpf']}")
    c.drawString(50, height - 170, f"Endereço: {dados_cliente['endereco']}")

    # Tabela de produtos
    y = height - 200
    c.setFont("Helvetica-Bold", 10)
    c.drawString(50, y, "Descrição")
    c.drawString(250, y, "Qtd")
    c.drawString(300, y, "Valor Unit.")
    c.drawString(400, y, "Total")

    c.setFont("Helvetica", 10)
    total_geral = 0
    y -= 20

    for item in produtos:
        total_item = item["quantidade"] * item["valor_unitario"]
        total_geral += total_item

        c.drawString(50, y, item["descricao"]) 
        c.drawString(250, y, str(item["quantidade"]))
        c.drawString(300, y, f"R$ {item['valor_unitario']:.2f}")
        c.drawString(400, y, f"R$ {total_item:.2f}")
        y -= 20

    # Total
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y - 10, f"Total da Nota: R$ {total_geral:.2f}")
    c.setFont("Helvetica", 10)
    c.drawString(50, y - 30, f"Data de Emissão: {datetime.today().strftime('%d/%m/%Y')}")

    c.save()
    buffer.seek(0)
    return buffer

# Streamlit App
st.title("Gerador de Nota Fiscal Fictícia 📄")

with st.form("form_nf"):
    st.subheader("Dados da Empresa")
    nome_empresa = st.text_input("Nome da Empresa", "Empresa Exemplo Ltda")
    cnpj_empresa = st.text_input("CNPJ", "00.000.000/0001-00")
    endereco_empresa = st.text_input("Endereço da Empresa", "Rua Exemplo, 123 - Cidade")

    st.subheader("Dados do Cliente")
    nome_cliente = st.text_input("Nome do Cliente", "João da Silva")
    cpf_cliente = st.text_input("CPF", "000.000.000-00")
    endereco_cliente = st.text_input("Endereço do Cliente", "Av. Cliente, 456 - Cidade")

    st.subheader("Produtos/Serviços")
    produtos = []
    for i in range(3):
        col1, col2, col3 = st.columns([2, 1, 1])
        with col1:
            descricao = st.text_input(f"Descrição {i+1}", f"Produto {i+1}")
        with col2:
            quantidade = st.number_input(f"Qtd {i+1}", min_value=1, value=1, step=1)
        with col3:
            valor_unitario = st.number_input(f"Valor Unit. {i+1}", min_value=0.0, value=10.0, step=0.01)

        produtos.append({
            "descricao": descricao,
            "quantidade": quantidade,
            "valor_unitario": valor_unitario
        })

    gerar = st.form_submit_button("Gerar Nota Fiscal")

if gerar:
    dados_empresa = {
        "nome": nome_empresa,
        "cnpj": cnpj_empresa,
        "endereco": endereco_empresa
    }

    dados_cliente = {
        "nome": nome_cliente,
        "cpf": cpf_cliente,
        "endereco": endereco_cliente
    }

    pdf_buffer = gerar_nota_fiscal(dados_empresa, dados_cliente, produtos)
    st.success("Nota fiscal gerada com sucesso!")

    st.download_button(
        label="📄 Baixar PDF da Nota Fiscal",
        data=pdf_buffer,
        file_name="nota_fiscal_ficticia.pdf",
        mime="application/pdf"
    )
