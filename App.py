import streamlit as st
from datetime import datetime
from docx import Document
from docx2pdf import convert
import os

st.set_page_config(page_title="Gerador de Comprovante", layout="centered")

st.title("📄 Gerador de Comprovante PIX")

# memória simples
if "chave_pix" not in st.session_state:
    st.session_state.chave_pix = ""

# upload da imagem
imagem = st.file_uploader("📷 Envie a imagem do comprovante", type=["png","jpg","jpeg"])

# inputs
pagador_nome = st.text_input("Nome do pagador")
pagador_cpf = st.text_input("CPF do pagador")
valor = st.text_input("Valor (ex: 1290,00)")

chave_pix = st.text_input("Chave Pix", value=st.session_state.chave_pix)

if chave_pix:
    st.session_state.chave_pix = chave_pix

# simulação OCR (depois dá pra melhorar)
recebedor_nome = "Recebedor da Imagem"
recebedor_doc = "***.000.000-**"
banco = "MERCADO PAGO IP LTDA."

# gerar PDF
if st.button("🚀 Gerar PDF"):
    if not pagador_nome or not pagador_cpf or not valor:
        st.warning("Preencha todos os campos")
    else:
        doc = Document("modelo.docx")

        agora = datetime.now()
        data_formatada = agora.strftime("%d/%m/%Y - %H:%M:%S")
        data_transacao = agora.strftime("%d/%m/%Y %H:%M:%S")

        for p in doc.paragraphs:
            p.text = p.text.replace("{{pagador_nome}}", pagador_nome)
            p.text = p.text.replace("{{pagador_cpf}}", pagador_cpf)
            p.text = p.text.replace("{{valor}}", valor)
            p.text = p.text.replace("{{chave_pix}}", chave_pix)
            p.text = p.text.replace("{{recebedor_nome}}", recebedor_nome)
            p.text = p.text.replace("{{recebedor_doc}}", recebedor_doc)
            p.text = p.text.replace("{{banco}}", banco)
            p.text = p.text.replace("{{data_hora}}", data_formatada)
            p.text = p.text.replace("{{data_transacao}}", data_transacao)

        arquivo_docx = "saida.docx"
        arquivo_pdf = "saida.pdf"

        doc.save(arquivo_docx)
        convert(arquivo_docx, arquivo_pdf)

        with open(arquivo_pdf, "rb") as f:
            st.success("✅ PDF gerado!")
            st.download_button("⬇️ Baixar PDF", f, file_name="comprovante.pdf")
