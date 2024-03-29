import streamlit as st
import PyPDF2
from io import BytesIO

st.set_page_config(page_title='Zaszyfruj pdf', page_icon='🔒')

def encrypt_pdf(input_file, password):
    try:
        pdf_reader = PyPDF2.PdfReader(input_file)
        pdf_writer = PyPDF2.PdfWriter()
        
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            pdf_writer.add_page(page)
        
        pdf_writer.encrypt(password)
        
        output = BytesIO()
        pdf_writer.write(output)
        output.seek(0)
        return output, None
    except PyPDF2.errors.FileNotDecryptedError:
        return None, "Nie można zaszyfrować już zaszyfrowanego pliku! Wgraj dokument niezabezpieczony hasłem."

st.title('Zaszyfruj pdf')

uploaded_file = st.file_uploader("Wybierz plik PDF", type="pdf")
password = st.text_input("Wprowadź hasło:", type="password")

if uploaded_file is not None and password:
    encrypted_pdf, error_msg = encrypt_pdf(uploaded_file, password)
    if encrypted_pdf:
        st.success("Dokument zaszyfrowany. Kliknij poniższy przycisk aby pobrać zaszyfrowany plik.")
        
        st.download_button(label="Pobierz zaszyfrowany dokument",
                        data=encrypted_pdf,
                        file_name=f"zaszyfrowany_{uploaded_file.name}",
                        mime="application/pdf")
    else:
        st.error(error_msg)


# Add a footer
st.markdown("""
    <style>
    .reportview-container .main .block-container{
        padding-bottom: 100px;
    }
    footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: white;
        color: black;
        text-align: center;
        padding: 0px;
    }
    </style>
    <footer>
        Autor: Grzegorz Piątek © 2024 | Kontakt: grzegorzadampiatek@gmail.com | Wersja: 0.3
    </footer>
    """, unsafe_allow_html=True)
