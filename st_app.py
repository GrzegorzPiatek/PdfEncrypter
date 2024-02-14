import streamlit as st
import PyPDF2
from io import BytesIO

def encrypt_pdf(input_file, password):
    pdf_reader = PyPDF2.PdfReader(input_file)
    pdf_writer = PyPDF2.PdfWriter()
    
    for page_num in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_num]
        pdf_writer.add_page(page)
    
    pdf_writer.encrypt(password)
    
    output = BytesIO()
    pdf_writer.write(output)
    output.seek(0)
    return output

st.title('Zaszyfruj pdf')

uploaded_file = st.file_uploader("Wybierz plik PDF", type="pdf")
password = st.text_input("Wprowadź hasło:", type="password")

if uploaded_file is not None and password:
    encrypted_pdf = encrypt_pdf(uploaded_file, password)
    st.success("Dokument zaszyfrowany. Kliknij poniższy przycisk aby pobrać zaszyfrowany plik.")
    
    st.download_button(label="Pobierz zaszyfrowany dokument",
                       data=encrypted_pdf,
                       file_name=f"zaszyfrowany_{uploaded_file.name}",
                       mime="application/pdf")
